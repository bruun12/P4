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
    assert node.to_c() == """if(sizeof("hej med dig")==8){printf("%f","hej med dig");}else if(sizeof("hej med dig")==4){printf("%d","hej med dig");}else if(sizeof("hej med dig")==1){printf("%s","hej med dig" ? "true" : "false");}else{printf("%s","hej med dig");}"""

def test_print_func2():
    correctLines = lineTrim("""
                {integer x = 5;
                double a = 3.2;
                print(x,a);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "int x = 5;"
    assert correctLines[2] == "float a = 3.2;"
    assert correctLines[3] == """if(sizeof(x)==8){printf("%f",x);}else if(sizeof(x)==4){printf("%d",x);}else if(sizeof(x)==1){printf("%s",x ? "true" : "false");}else{printf("%s",x);}if(sizeof(a)==8){printf("%f",a);}else if(sizeof(a)==4){printf("%d",a);}else if(sizeof(a)==1){printf("%s",a ? "true" : "false");}else{printf("%s",a);};"""
    assert correctLines[4] == "}"

def test_print_func3():
    correctLines = lineTrim("""{
                boolean b = true;
                print(b);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "bool b = true;"
    assert correctLines[2] == """if(sizeof(b)==8){printf("%f",b);}else if(sizeof(b)==4){printf("%d",b);}else if(sizeof(b)==1){printf("%s",b ? "true" : "false");}else{printf("%s",b);};"""
    assert correctLines[3] == "}"