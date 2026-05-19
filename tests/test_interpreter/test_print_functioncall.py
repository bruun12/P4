from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import FunctionCall
from parser.ASTNodes import BlockStatement
from tests.test_interpreter.test_line_trim import lineTrim

def test_print_func1():
    lex = Lexer("""print("hej med dig");""")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    assert isinstance(node, FunctionCall)
    assert lineTrim("""print("hej med dig");""")[0:] == [
        "if (sametypeof(1.2,\"hej med dig\")){",
        "printf(\"%f\",\"hej med dig\");",
        "} else if (sizeof(\"hej med dig\") == 1) {",
        "printf(\"%s\", \"hej med dig\" ? \"true\" : \"false\");",
        "} else if (sametypeof(1, \"hej med dig\")){",
        "printf(\"%d\", \"hej med dig\");",
        "} else if (sametypeof(\"string\",\"hej med dig\")){",
        "printf(\"%s\",\"hej med dig\");",
        "}",
        ";",
    ]

def test_print_func2():
    correctLines = lineTrim("""
                {integer x = 5;
                double a = 3.2;
                print(x,a);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "int x = 5;"
    assert correctLines[2] == "double a = 3.2;"
    assert correctLines[3:] == [
        "if (sametypeof(1.2,x)){",
        "printf(\"%f\",x);",
        "} else if (sizeof(x) == 1) {",
        "printf(\"%s\", x ? \"true\" : \"false\");",
        "} else if (sametypeof(1, x)){",
        "printf(\"%d\", x);",
        "} else if (sametypeof(\"string\",x)){",
        "printf(\"%s\",x);",
        "}",
        "if (sametypeof(1.2,a)){",
        "printf(\"%f\",a);",
        "} else if (sizeof(a) == 1) {",
        "printf(\"%s\", a ? \"true\" : \"false\");",
        "} else if (sametypeof(1, a)){",
        "printf(\"%d\", a);",
        "} else if (sametypeof(\"string\",a)){",
        "printf(\"%s\",a);",
        "}",
        ";",
        "}",
    ]

def test_print_func3():
    correctLines = lineTrim("""{
                boolean b = true;
                print(b);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "bool b = true;"
    assert correctLines[2:] == [
        "if (sametypeof(1.2,b)){",
        "printf(\"%f\",b);",
        "} else if (sizeof(b) == 1) {",
        "printf(\"%s\", b ? \"true\" : \"false\");",
        "} else if (sametypeof(1, b)){",
        "printf(\"%d\", b);",
        "} else if (sametypeof(\"string\",b)){",
        "printf(\"%s\",b);",
        "}",
        ";",
        "}",
    ]
