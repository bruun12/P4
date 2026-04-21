from parser.parser import Parser
from lexer.lexer import Token, TokenType

def test_check_stopper():
    tokens = [Token(TokenType.TYPE, "string", 1, 1), 
              Token(TokenType.IDENTIFIER, "x", 2, 1),
              Token(TokenType.EQ, "=", 3, 1),
              Token(TokenType.STRING, "hello world", 4, 1),
              Token(TokenType.SEMICOLON, ";", 5, 1),
              Token(TokenType.EOF, "EOF", 6, 1)
              ]

    parser = Parser(tokens)
    assert parser.check(TokenType.TYPE)

    # ensure that it tries to advance further than the token array 
    for x in range(1 , 20):
        parser.advance()

    assert parser.check(TokenType.EOF)
