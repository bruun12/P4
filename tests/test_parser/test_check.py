from parser.parser import Parser
from lexer.lexer import Token, TokenType
import pytest
from error_handling import ParserError

# Checks if it correctly checks the existing tokens

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

def check_fail_check_string():
    tokens = [Token(TokenType.TYPE, "string", 1, 1)
              ]
    
    parser = Parser(tokens)
    with pytest.raises(ParserError):
        parser.check(TokenType.IDENTIFIER)

def check_fail_check_identifier():
    tokens = [Token(TokenType.IDENTIFIER, "str", 1, 1)
              ]
    
    parser = Parser(tokens)
    with pytest.raises(ParserError):
        parser.check(TokenType.TYPE)

def test_check_different_types():
    tokens = [Token(TokenType.TYPE, "string", 1, 1), 
              Token(TokenType.IDENTIFIER, "x", 2, 1),
              Token(TokenType.EQ, "=", 3, 1),
              Token(TokenType.STRING, "hello world", 4, 1),
              Token(TokenType.SEMICOLON, ";", 5, 1),
              Token(TokenType.EOF, "EOF", 6, 1)
              ]

    parser = Parser(tokens)
    assert parser.check(TokenType.TYPE)
    parser.advance()
    assert parser.check(TokenType.IDENTIFIER)
    parser.advance()
    assert parser.check(TokenType.EQ)
    parser.advance()
    assert parser.check(TokenType.STRING)
    parser.advance()
    assert parser.check(TokenType.SEMICOLON)
    parser.advance()
    assert parser.check(TokenType.EOF)