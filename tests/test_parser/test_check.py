from parser.parser import Parser
from lexer.lexer import Lexer, TokenType

def test_check():
    string = "integer x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    lex.lexer()

    parser = Parser(lex.tokens)
    assert parser.check(TokenType.TYPE)

    while parser.current().type != TokenType.EOF:
        parser.advance()

    assert parser.check(TokenType.EOF)
