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
    assert node.to_c() == """if(sizeof("hej med dig")==8){printf("%f","hej med dig");}else if(sizeof("hej med dig")==4){printf("%d","hej med dig");}else{printf("%s","hej med dig");}"""

def test_print_func2():
    correctLines = lineTrim("""
                {integer a = 5;
                print(a);
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "int a = 5;"
    assert correctLines[2] == """if(sizeof(a)==8){printf("%f",a);}else if(sizeof(a)==4){printf("%d",a);}else{printf("%s",a);};"""
    assert correctLines[3] == "}"