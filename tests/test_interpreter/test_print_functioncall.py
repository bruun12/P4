from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import FunctionCall
from parser.ASTNodes import BlockStatement
from tests.test_interpreter.test_line_trim import lineTrim

def test_print_func1():
    correctLines = lineTrim("""print("hej med dig");""")
    assert correctLines[0] == """if (sametypeof(1.2,"hej med dig")){"""
    assert correctLines[1] == """printf("%f","hej med dig");"""
    assert correctLines[2] == """} else if (sizeof("hej med dig") == 1) {"""
    assert correctLines[3] == """printf("%s", "hej med dig" ? "true" : "false");"""
    assert correctLines[4] == """} else if (sametypeof(1, "hej med dig")){"""
    assert correctLines[5] == """printf("%d", "hej med dig");"""
    assert correctLines[6] == """} else if (sametypeof("string","hej med dig")){"""
    assert correctLines[7] == """printf("%s","hej med dig");"""
    assert correctLines[8] == """}"""

def test_print_func2():
    correctLines = lineTrim("""
                {integer x = 5;
                double a = 3.2;
                print(x,a);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "int x = 5;"
    assert correctLines[2] == "double a = 3.2;"
    assert correctLines[3] == """if (sametypeof(1.2,x)){"""
    assert correctLines[4] == """printf("%f",x);"""
    assert correctLines[5] == """} else if (sizeof(x) == 1) {"""
    assert correctLines[6] == """printf("%s", x ? "true" : "false");"""
    assert correctLines[7] == """} else if (sametypeof(1, x)){"""
    assert correctLines[8] == """printf("%d", x);"""
    assert correctLines[9] == """} else if (sametypeof("string",x)){"""
    assert correctLines[10] == """printf("%s",x);"""
    assert correctLines[11] == """}"""
    assert correctLines[12] == """if (sametypeof(1.2,a)){"""
    assert correctLines[13] == """printf("%f",a);"""
    assert correctLines[14] == """} else if (sizeof(a) == 1) {"""
    assert correctLines[15] == """printf("%s", a ? "true" : "false");"""
    assert correctLines[16] == """} else if (sametypeof(1, a)){"""
    assert correctLines[17] == """printf("%d", a);"""
    assert correctLines[18] == """} else if (sametypeof("string",a)){"""
    assert correctLines[19] == """printf("%s",a);"""
    assert correctLines[20] == """}"""
    assert correctLines[21] == ";"
    assert correctLines[22] == "}"

def test_print_func3():
    correctLines = lineTrim("""{
                boolean b = true;
                print(b);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "bool b = true;"
    assert correctLines[2] == """if (sametypeof(1.2,b)){"""
    assert correctLines[3] == """printf("%f",b);"""
    assert correctLines[4] == """} else if (sizeof(b) == 1) {"""
    assert correctLines[5] == """printf("%s", b ? "true" : "false");"""
    assert correctLines[6] == """} else if (sametypeof(1, b)){"""
    assert correctLines[7] == """printf("%d", b);"""
    assert correctLines[8] == """} else if (sametypeof("string",b)){"""
    assert correctLines[9] == """printf("%s",b);"""
    assert correctLines[10] == """}"""
    assert correctLines[11] == ";"
    assert correctLines[12] == "}"