from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import ArrayDeclaration, ArrayDeclarationEmpty

def test_arrayDeclarationEmpty():
    lex = Lexer("integer arr[3];")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ArrayDeclarationEmpty)
    assert node.to_c() ==  "int arr[3];"

def test_arrayDeclaration():
    lex = Lexer(f"""integer arr[] = {{{18}}};""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, ArrayDeclaration)
    assert node.to_c() == f"""int arr[] = {{{18}}};"""

    # Block, Parameter, Function