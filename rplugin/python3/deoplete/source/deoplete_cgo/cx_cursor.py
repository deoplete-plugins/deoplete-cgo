class CXCursor(object):
    kinds = dict(
        {
            # Declarations
            1: "unexposed",  # CXCursor_UnexposedDecl
            2: "struct",  # CXCursor_StructDecl: A C or C++ struct
            3: "union",  # CXCursor_UnionDecl: A C or C++ union.
            4: "class",  # CXCursor_ClassDecl: A C++ class.
            5: "enumeration",  # CXCursor_EnumDecl: An enumeration.
            6: "field",  # CXCursor_FieldDecl: A field (in C) or non-static data member (in C++) in a struct, union, or C++ class.
            7: "enumerator constant",  # CXCursor_EnumConstantDecl: An enumerator constant.
            8: "function",  # CXCursor_FunctionDecl: A function.
            9: "variable",  # CXCursor_VarDecl: A variable.
            10: "method parameter",  # CXCursor_ParmDecl: A function or method parameter.
            11: "@interface",  # CXCursor_ObjCInterfaceDecl: An Objective-C @interface.
            12: "@interface category",  # CXCursor_ObjCCategoryDecl: An Objective-C @interface for a category.
            13: "@protocol",  # CXCursor_ObjCProtocolDecl: An Objective-C @protocol declaration.
            14: "@property",  # CXCursor_ObjCPropertyDecl: An Objective-C @property declaration.
            15: "instance",  # CXCursor_ObjCIvarDecl: An Objective-C instance variable.
            16: "instance method",  # CXCursor_ObjCInstanceMethodDecl: An Objective-C instance method.
            17: "class method",  # CXCursor_ObjCClassMethodDecl: An Objective-C class method.
            18: "@implementation",  # CXCursor_ObjCImplementationDecl: An Objective-C @implementation.
            19: "@implementation category",  # CXCursor_ObjCCategoryImplDecl: An Objective-C @implementation for a category.
            20: "typedef",  # CXCursor_TypedefDecl: A typedef.
            21: "class method",  # CXCursor_CXXMethod: A C++ class method.
            22: "namespace",  # CXCursor_Namespace: A C++ namespace.
            23: "linkage",  # CXCursor_LinkageSpec: A linkage specification, e.g. 'extern "C"'.
            24: "constructor",  # CXCursor_Constructor: A C++ constructor.
            25: "destructor",  # CXCursor_Destructor: A C++ destructor.
            26: "conversion function",  # CXCursor_ConversionFunction: A C++ conversion function.
            27: "template type parameter",  # CXCursor_TemplateTypeParameter: A C++ template type parameter.
            28: "template non-type parameter",  # CXCursor_NonTypeTemplateParameter: A C++ non-type template parameter.
            29: "template template parameter",  # CXCursor_TemplateTemplateParameter: A C++ template template parameter.
            30: "function template",  # CXCursor_FunctionTemplate: A C++ function template.
            31: "class template",  # CXCursor_ClassTemplate: A C++ class template.
            32: "class template partial",  # CXCursor_ClassTemplatePartialSpecialization: A C++ class template partial specialization.
            33: "namespace alias",  # CXCursor_NamespaceAlias: A C++ namespace alias declaration.
            34: "using directive",  # CXCursor_UsingDirective: A C++ using directive.
            35: "using declaration",  # CXCursor_UsingDeclaration: A C++ using declaration.
            36: "alias declaration",  # CXCursor_TypeAliasDecl: A C++ alias declaration
            37: "@synthesize definition",  # CXCursor_ObjCSynthesizeDecl: An Objective-C @synthesize definition.
            38: "@dynamic definition",  # CXCursor_ObjCDynamicDecl: An Objective-C @dynamic definition.
            39: "access specifier",  # CXCursor_CXXAccessSpecifier: An access specifier.
            # References
            40: "SuperClass reference",  # CXCursor_ObjCSuperClassRef
            41: "Protocol reference",  # CXCursor_ObjCProtocolRef
            42: "Class reference",  # CXCursor_ObjCClassRef
            43: "type declaration reference",  # CXCursor_TypeRef: A reference to a type declaration. # TODO(zchee): fix kind string
            44: "base specifier",  # CXCursor_CXXBaseSpecifier
            45: "template reference",  # CXCursor_TemplateRef: A reference to a class template, function template, template template parameter, or class template partial specialization.
            46: "namespace reference",  # CXCursor_NamespaceRef: A reference to a namespace or namespace alias.
            47: "member of a struct, union, or class reference",  # CXCursor_MemberRef: A reference to a member of a struct, union, or class that occurs in some non-expression context, e.g., a designated initializer.
            48: "labeled reference",  # CXCursor_LabelRef: A reference to a labeled statement.
            49: "overloaded functions or function templates reference",  # CXCursor_OverloadedDeclRef: A reference to a set of overloaded functions or function templates that has not yet been resolved to a specific function or function template.
            50: "variable reference",  # CXCursor_VariableRef: A reference to a variable that occurs in some non-expression context, e.g., a C++ lambda capture list.
            # Error conditions """
            70: "invalid file",  # CXCursor_InvalidFile
            71: "no decl found",  # CXCursor_NoDeclFound
            72: "not implemented",  # CXCursor_NotImplemented
            73: "invalid code",  # CXCursor_InvalidCode
            # Expressions """
            100: "unexposed expr",  # CXCursor_UnexposedExpr: An expression whose specific kind is not exposed via this interface.
            101: "decl ref expr",  # CXCursor_DeclRefExpr: An expression that refers to some value declaration, such as a function, variable, or enumerator.
            102: "member ref expr",  # CXCursor_MemberRefExpr: An expression that refers to a member of a struct, union, class, Objective-C class, etc.
            103: "calls function expr",  # CXCursor_CallExpr: An expression that calls a function.
            104: "Objective-C message expr",  # CXCursor_ObjCMessageExpr: An expression that sends a message to an Objective-C object or class.
            105: "block literal expr",  # CXCursor_BlockExpr: An expression that represents a block literal.
            106: "integer",  # CXCursor_IntegerLiteral: An integer literal.
            107: "floating point number",  # CXCursor_FloatingLiteral: A floating point number literal.
            108: "imaginary number",  # CXCursor_ImaginaryLiteral: An imaginary number literal.
            109: "string",  # CXCursor_StringLiteral: A string literal.
            110: "character",  # CXCursor_CharacterLiteral: A character literal.
            111: "parenthesized",  # CXCursor_ParenExpr: A parenthesized expression, e.g. "(1)". This AST node is only formed if full location information is requested.
            112: "unary",  # CXCursor_UnaryOperator: This represents the unary-expression's (except sizeof and alignof).
            113: "array Subscripting",  # CXCursor_ArraySubscriptExpr: [C99 6.5.2.1] Array Subscripting.
            114: "builtin binary operation",  # CXCursor_BinaryOperator: A builtin binary operation expression such as "x + y" or "x <= y".
            115: "compound assignment",  # CXCursor_CompoundAssignOperator: Compound assignment such as "+=".
            116: "ternary",  # CXCursor_ConditionalOperator: The ?: ternary operator.
            117: "explicit cast",  # CXCursor_CStyleCastExpr: An explicit cast in C (C99 6.5.4) or a C-style cast in C++ (C++ [expr.cast]), which uses the syntax (Type)expr.
            118: "compound literal",  # CXCursor_CompoundLiteralExpr: [C99 6.5.2.5]
            119: "initializer list",  # CXCursor_InitListExpr: Describes an C or C++ initializer list.
            120: "GNU address of label extension",  # CXCursor_AddrLabelExpr: The GNU address of label extension, representing &label.
            121: "GNU Statement Expression extension",  # CXCursor_StmtExpr: This is the GNU Statement Expression extension: ({int X=4; X;})
            122: "generic selection",  # CXCursor_GenericSelectionExpr: Represents a C11 generic selection.
            123: "GNU __null extension",  # CXCursor_GNUNullExpr: Implements the GNU __null extension, which is a name for a null pointer constant that has integral type (e.g., int or long) and is the same size and alignment as a pointer.
            124: "static_cast",  # CXCursor_CXXStaticCastExpr: C++'s static_cast<> expression.
            125: "dynamic_cast",  # CXCursor_CXXDynamicCastExpr: C++'s dynamic_cast<> expression.
            126: "reinterpret_cast",  # CXCursor_CXXReinterpretCastExpr: C++'s reinterpret_cast<> expression.
            127: "const_cast",  # CXCursor_CXXConstCastExpr: C++'s const_cast<> expression.
            128: "type conversion",  # CXCursor_CXXFunctionalCastExpr: Represents an explicit C++ type conversion that uses "functional" notion (C++ [expr.type.conv]).
            129: "typeid expression",  # CXCursor_CXXTypeidExpr: A C++ typeid expression (C++ [expr.typeid]).
            130: "boolean",  # CXCursor_CXXBoolLiteralExpr: [C++ 2.13.5] C++ Boolean Literal.
            131: "pointer",  # CXCursor_CXXNullPtrLiteralExpr: [C++0x 2.14.7] C++ Pointer Literal.
            132: "this",  # CXCursor_CXXThisExpr: Represents the "this" expression in C++
            133: "throw",  # CXCursor_CXXThrowExpr: [C++ 15] C++ Throw Expression.
            134: "new",  # CXCursor_CXXNewExpr: A new expression for memory allocation and constructor calls, e.g: "new CXXNewExpr(foo)".
            135: "delete",  # CXCursor_CXXDeleteExpr: A delete expression for memory deallocation and destructor calls,e.g. "delete[] pArray".
            136: "unary",  # CXCursor_UnaryExpr: A unary expression. (noexcept, sizeof, or other traits)
            137: "Objective-C string",  # CXCursor_ObjCStringLiteral: An Objective-C string literal i.e. @"foo".
            138: "Objective-C @encode",  # CXCursor_ObjCEncodeExpr: An Objective-C @encode expression.
            139: "Objective-C @selector",  # CXCursor_ObjCSelectorExpr: An Objective-C @selector expression.
            140: "Objective-C @protocol",  # CXCursor_ObjCProtocolExpr: An Objective-C @protocol expression.
            141: "Objective-C bridged cast",  # CXCursor_ObjCBridgedCastExpr: An Objective-C "bridged" cast expression, which casts between Objective-C pointers and C pointers, transferring ownership in the process.
            142: "pack",  # CXCursor_PackExpansionExpr: Represents a C++0x pack expansion that produces a sequence of expressions.
            143: "sizeof pack",  # CXCursor_SizeOfPackExpr: Represents an expression that computes the length of a parameter pack.
            144: "lambda",  # CXCursor_LambdaExpr: Represents a C++ lambda expression that produces a local function object.
            145: "Objective-c boolean",  # CXCursor_ObjCBoolLiteralExpr: Objective-c Boolean Literal.
            146: "Objective-c self",  # CXCursor_ObjCSelfExpr: Represents the "self" expression in an Objective-C method.
            147: "OpenMP array",  # CXCursor_OMPArraySectionExpr: OpenMP 5.0 [2.1.5, Array Section].
            148: "@available",  # CXCursor_ObjCAvailabilityCheckExpr: Represents an @available(...) check.
            149: "fixed point",  # CXCursor_FixedPointLiteral: Fixed point literal
            150: "OpenMP array shaping",  # CXCursor_OMPArrayShapingExpr: OpenMP 5.0 [2.1.4, Array Shaping].
            151: "OpenMP iterators",  # CXCursor_OMPIteratorExpr: OpenMP 5.0 [2.1.6 Iterators]
            152: "OpenCL addrspace_cast",  # CXCursor_CXXAddrspaceCastExpr: OpenCL's addrspace_cast<> expression.
            # Statements """
            200: "unexposed stmt",  # CXCursor_UnexposedStmt: A statement whose specific kind is not exposed via this interface.
            201: "labelled stmt",  # CXCursor_LabelStmt: A labelled statement in a function.
            202: "group of stmts",  # CXCursor_CompoundStmt: A group of statements like { stmt stmt }.
            203: "case stmt",  # CXCursor_CaseStmt: A case statement.
            204: "default stmt",  # CXCursor_DefaultStmt: A default statement.
            205: "if stmt",  # CXCursor_IfStmt: An if statement
            206: "switch stmt",  # CXCursor_SwitchStmt: A switch statement.
            207: "while stmt",  # CXCursor_WhileStmt: A while statement.
            208: "do stmt",  # CXCursor_DoStmt: A do statement.
            209: "for stmt",  # CXCursor_ForStmt: A for statement.
            210: "goto stmt",  # CXCursor_GotoStmt: A goto statement.
            211: "indirect goto stmt",  # CXCursor_IndirectGotoStmt: An indirect goto statement.
            212: "continue stmt",  # CXCursor_ContinueStmt: A continue statement.
            213: "break stmt",  # CXCursor_BreakStmt: A break statement.
            214: "return stmt",  # CXCursor_ReturnStmt: A return statement.
            215: "GCC inline assembly stmt",  # CXCursor_GCCAsmStmt: A GCC inline assembly statement extension.
            216: "Objective-C @try-@catch-@finally",  # CXCursor_ObjCAtTryStmt: Objective-C's overall @try-@catch-@finally statement.
            217: "Objective-C @catch",  # CXCursor_ObjCAtCatchStmt: Objective-C's @catch statement.
            218: "Objective-C @finally",  # CXCursor_ObjCAtFinallyStmt: Objective-C's @finally statement.
            219: "Objective-C @throw",  # CXCursor_ObjCAtThrowStmt: Objective-C's @throw statement.
            220: "Objective-C @synchronized",  # CXCursor_ObjCAtSynchronizedStmt: Objective-C's @synchronized statement.
            221: "Objective-C autorelease pool",  # CXCursor_ObjCAutoreleasePoolStmt: Objective-C's autorelease pool statement.
            222: "Objective-C collection",  # CXCursor_ObjCForCollectionStmt: Objective-C's collection statement.
            223: "catch",  # CXCursor_CXXCatchStmt: C++'s catch statement.
            224: "try",  # CXCursor_CXXTryStmt: C++'s try statement.
            225: "for",  # CXCursor_CXXForRangeStmt: C++'s for (* : *) statement.
            226: "226",  # CXCursor_SEHTryStmt: Windows Structured Exception Handling's try statement.
            227: "227",  # CXCursor_SEHExceptStmt: Windows Structured Exception Handling's except statement.
            228: "228",  # CXCursor_SEHFinallyStmt: Windows Structured Exception Handling's finally statement.
            229: "229",  # CXCursor_MSAsmStmt: A MS inline assembly statement extension.
            230: "null",  # CXCursor_NullStmt: The null statement ";": C99 6.8.3p3.
            231: "mixing declarations",  # CXCursor_DeclStmt: Adaptor class for mixing declarations with statements and expressions.
            # TODO(zchee): 232-287
            300: "300",  # CXCursor_TranslationUnit (Cursor that represents the
            400: "400",  # CXCursor_UnexposedAttr
            401: "401",  # CXCursor_IBActionAttr
            402: "402",  # CXCursor_IBOutletAttr
            403: "403",  # CXCursor_IBOutletCollectionAttr
            404: "404",  # CXCursor_CXXFinalAttr
            405: "405",  # CXCursor_CXXOverrideAttr
            406: "406",  # CXCursor_AnnotateAttr
            407: "407",  # CXCursor_AsmLabelAttr
            500: "500",  # CXCursor_PreprocessingDirective
            501: "define",  # CXCursor_MacroDefinition
            502: "502",  # CXCursor_MacroInstantiation
            503: "503",  # CXCursor_InclusionDirective
            600: "600",  # CXCursor_ModuleImportDecl (A module import declaration)
        }
    )
