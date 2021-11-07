# SPDX-FileCopyrightText: 2021 The deoplete-plugins Authors
# SPDX-License-Identifier: MIT

import os
import re
from typing import Tuple

from deoplete.base.source import Base
from deoplete.util import load_external_module, error, getlines
from deoplete.util import Nvim, UserContext, Candidates

try:
    load_external_module(__file__, "")
    import clang.cindex as clang

    load_external_module(__file__, "source/deoplete_cgo")
    from cx_cursor import CXCursor
except ImportError as e:
    raise e


class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super(Source, self).__init__(vim)

        self.name = "cgo"
        self.mark = "[cgo]"
        self.filetypes = ["go"]
        self.input_pattern = r"[^\W\d]*C\."
        self.rank = 500
        self.is_volatile = True
        self.is_debug_enabled = False

        self.cgo_options = dict()
        self.libclang_library_path = None
        self.clang_index = None

        self.cgo_cache = dict()
        self.cgo_inline_source = None

    def on_init(self, context: UserContext) -> None:
        vars = self.vim.vars

        self.libclang_library_path = vars.get(
            "deoplete#sources#cgo#libclang_library_path", ""
        )
        if self.libclang_library_path == "":
            error(self.vim, "self.libclang_library_path is empty")

        self.cgo_options = {
            "std": vars.get(
                "deoplete#sources#cgo#std",
                {
                    "c": "c11",
                    "cpp": "c++17",
                },
            ),
            "sort_algo": vars.get("deoplete#sources#cgo#sort_algo", None),
        }

        if (
            not clang.Config.loaded
            and clang.Config.library_path != self.libclang_library_path
        ):
            clang.Config.set_library_file(self.libclang_library_path)
            clang.Config.set_compatibility_check(False)

        self.clang_index = clang.Index.create()

    def on_event(self, context: UserContext) -> None:
        pass

    def get_complete_position(self, context: UserContext) -> int:
        m = re.search("(?:" + context["keyword_pattern"] + ")$|$", context["input"])
        return m.start() if m else -1

    def gather_candidates(self, context: UserContext) -> Candidates:
        buffer = getlines(self.vim)
        return self.cgo_completion(buffer)

    def cgo_completion(self, buffer) -> Candidates:
        # No include header
        if self.get_inline_source(buffer)[0] == 0:
            return

        line_count, inline_source = self.get_inline_source(buffer)

        # exists 'self.cgo_inline_source', same inline sources and
        # already cached cgo complete candidates
        if (
            self.cgo_inline_source is not None
            and self.cgo_inline_source == inline_source
            and self.cgo_cache[self.cgo_inline_source]
        ):
            # Use in-memory(self.cgo_headers) cacahe
            return self.cgo_cache[self.cgo_inline_source]
        else:
            self.cgo_inline_source = inline_source
            return self.complete(
                self.clang_index,
                self.cgo_cache,
                self.cgo_options,
                line_count,
                self.cgo_inline_source,
            )

    def get_inline_source(self, buffer) -> Tuple:
        # TODO(zchee): very slow. about 100ms

        if 'import "C"' not in buffer:
            return (0, "")

        pos_import_c = list(buffer).index('import "C"')
        c_inline = buffer[:pos_import_c]

        if c_inline[len(c_inline) - 1] == "*/":
            comment_start = next(
                i
                for i, v in zip(range(len(c_inline) - 1, 0, -1), reversed(c_inline))
                if v == "/*"
            )
            c_inline = c_inline[comment_start + 1 : len(c_inline) - 1]
            
        cgo_pattern = r"#cgo (\S+): (.+)"
        for i, line in enumerate(c_inline):
            if re.match(cgo_pattern, line):
                del(c_inline[i])

        return (len(c_inline), "\n".join(c_inline))

    def complete(self, index, cache, cgo_options, line_count, source):
        cgo_pattern = r"#cgo (\S+): (.+)"
        flags = set()
        for key, value in re.findall(cgo_pattern, source):
            if key == "pkg-config":
                for flag in self.get_pkgconfig(value.split()):
                    flags.add(flag)
            else:
                if "${SRCDIR}" in key:
                    key = key.replace("${SRCDIR}", "./")
                flags.add("%s=%s" % (key, value))

        cgo_flags = ["-std", cgo_options["std"]["c"]] + list(flags)

        fname = "cgo_inline.c"
        main = """
int main(void) {
struct 
};
    """
        template = source + main
        files = [(fname, template)]

        # clang.TranslationUnit
        # PARSE_NONE = 0
        # PARSE_DETAILED_PROCESSING_RECORD = 1
        # PARSE_INCOMPLETE = 2
        # PARSE_PRECOMPILED_PREAMBLE = 4
        # PARSE_CACHE_COMPLETION_RESULTS = 8
        # PARSE_SKIP_FUNCTION_BODIES = 64
        # PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION = 128
        options = (
            clang.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD
            | clang.TranslationUnit.PARSE_INCOMPLETE
            | clang.TranslationUnit.PARSE_PRECOMPILED_PREAMBLE
            | clang.TranslationUnit.PARSE_CACHE_COMPLETION_RESULTS
        )

        tu = index.parse(
            path=fname, args=cgo_flags, unsaved_files=files, options=options
        )

        cr = tu.codeComplete(
            path=fname,
            line=(line_count + 2),
            column=1,
            unsaved_files=files,
            include_macros=True,
            include_code_patterns=True,
            include_brief_comments=True,
        )
        cr_struct = tu.codeComplete(
            path=fname,
            line=(line_count + 2),
            column=8,
            unsaved_files=files,
            include_macros=True,
            include_code_patterns=True,
            include_brief_comments=True,
        )

        if cr is None or cr_struct is None:
            return []
        results = cr.results
        struct_results = cr_struct.results
        if cgo_options["sort_algo"] == "priority":
            results = sorted(cr.results, key=self.get_priority)
            struct_results = sorted(cr_struct.results, key=self.get_priority)
        elif cgo_options["sort_algo"] == "alphabetical":
            results = sorted(cr.results, key=self.get_abbrevation)
            struct_results = sorted(cr_struct.results, key=self.get_abbrevation)

        cache[source] = [
            {
                "word": "CString",
                "abbr": "CString(string) *C.char",
                "info": "CString(string) *C.char",
                "kind": "function",
                "dup": 1,
            },
            {
                "word": "CBytes",
                "abbr": "CBytes([]byte) unsafe.Pointer",
                "info": "CBytes([]byte) unsafe.Pointer",
                "kind": "function",
                "dup": 1,
            },
            {
                "word": "GoString",
                "abbr": "GoString(*C.char) string",
                "info": "GoString(*C.char) string",
                "kind": "function",
                "dup": 1,
            },
            {
                "word": "GoStringN",
                "abbr": "GoStringN(*C.char, C.int) string",
                "info": "GoStringN(*C.char, C.int) string",
                "kind": "function",
                "dup": 1,
            },
            {
                "word": "GoBytes",
                "abbr": "GoBytes(unsafe.Pointer, C.int) []byte",
                "info": "GoBytes(unsafe.Pointer, C.int) []byte",
                "kind": "function",
                "dup": 1,
            },
        ]

        cache[source] += list(map(self.parse_candidates, results))
        cache[source] += list(map(self.parse_candidates, struct_results))

        return cache[source]

    def get_priority(self, x):
        return x.string.priority

    def get_abbr(self, strings):
        for chunks in strings:
            if chunks.isKindTypedText():
                return chunks.spelling
        return ""

    def get_abbrevation(self, x):
        return self.get_abbr(x.string).lower()

    def parse_candidates(self, result):
        completion = {"dup": 1, "word": ""}
        _type = ""
        word = ""
        placeholder = ""
        sep = " "

        for chunk in [x for x in result.string if x.spelling]:
            chunk_spelling = chunk.spelling
            # ignore inline fake main(void), and meaningless spellings
            if (
                chunk_spelling is None
                or chunk_spelling == "main"
                or chunk_spelling == "struct"
                or chunk_spelling == "("
            ):
                continue

            if chunk.isKindTypedText():
                word += chunk_spelling
                placeholder += chunk_spelling
            elif chunk.isKindResultType():
                _type += chunk_spelling
            else:
                placeholder += chunk_spelling

        if not word:
            # early return
            return completion

        abbr = completion["info"] = placeholder + sep + _type

        if result.kind == clang.CursorKind.STRUCT_DECL:
            completion["word"] = "struct_" + word
            completion["abbr"] = "struct_" + abbr
        elif result.kind == clang.CursorKind.UNION_DECL:
            completion["word"] = "union_" + word
            completion["abbr"] = "union_" + abbr
        elif result.kind == clang.CursorKind.ENUM_CONSTANT_DECL:
            completion["word"] = "enum_" + word
            completion["abbr"] = "enum_" + abbr
        else:
            completion["word"] = word
            completion["abbr"] = abbr

        completion["kind"] = " ".join(
            [
                (
                    CXCursor.kinds[result.cursorKind]
                    if (result.cursorKind in CXCursor.kinds)
                    else str(result.cursorKind)
                )
            ]
        )

        return completion

    def get_pkgconfig(self, packages):
        out = []
        pkgconfig = self.find_binary_path("pkg-config")
        if pkgconfig != "":
            for pkg in packages:
                flag = os.popen(pkgconfig + " " + pkg + " --cflags --libs").read()
                out += flag.rstrip().split(" ")
        return out

    def find_binary_path(self, path):
        def is_exec(bin_path):
            return os.path.isfile(bin_path) and os.access(bin_path, os.X_OK)

        dirpath, binary = os.path.split(path)
        if dirpath:
            if is_exec(path):
                return path
        else:
            for p in os.environ["PATH"].split(os.pathsep):
                p = p.strip('"')
                binary = os.path.join(p, path)
                if is_exec(binary):
                    return binary
        return self.print_error(path + " binary not found")
