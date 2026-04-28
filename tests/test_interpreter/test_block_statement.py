from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import BlockStatement

def test_block_statement():
    lex = Lexer("{x = 2;}")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, BlockStatement)
    assert node.to_c() == """{x = 2;\n}"""

def test_block_statement_with_2():
    lex = Lexer("""{
                integer x = 2;
                integer arr[] = {1,2};
                }""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, BlockStatement)
    assert node.to_c() == """{int x = 2;\nint arr[] = {1,2};\n}"""

def test_block_statement_with_3():
    lex = Lexer("""{
                integer y = 3;
                integer x = 2;
                double abe = 4.2;
                }""")
    lex.lexer()
    node = Parser(lex.tokens).statement()
    assert isinstance(node, BlockStatement)
    assert node.to_c() == """{int y = 3;\nint x = 2;\nfloat abe = 4.2;\n}"""