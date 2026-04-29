from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import FunctionCall
from tests.test_interpreter.test_line_trim import lineTrim

def test_small_program():
    lex = Lexer("""print("Hej med dig")""")
    lex.lexer()
    node = Parser(lex.tokens).parse_expression()
    assert isinstance(node, FunctionCall)
    assert node.to_c() == """printf("Hej med dig")"""