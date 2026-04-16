import pytest
from parser.parser import Parser
from lexer.lexer import TokenType, Token
from parser.ASTNodes import ParserError

def test_consume_success():
    tokens = [Token(TokenType.TYPE, "integer", 1, 1), 
            Token(TokenType.IDENTIFIER, "x", 2, 1)
            ]

    parser = Parser(tokens)
    
    parser.consume(TokenType.TYPE, "error message")
    consumedToken = parser.previous() #needs to be previous because consume self advance 
    assert consumedToken.type == TokenType.TYPE
    parser.consume(TokenType.IDENTIFIER, "error message")
    consumedToken = parser.previous() 
    assert consumedToken.type == TokenType.IDENTIFIER

def test_consume_fail():
    tokens = [Token(TokenType.TYPE, "integer", 1, 1), 
              Token(TokenType.INTEGER, "4", 2, 1)]

    parser = Parser(tokens)
    
    parser.consume(TokenType.TYPE, "error message")
    consumedToken = parser.previous() #needs to be previous because consume self advance 
    assert consumedToken.type == TokenType.TYPE
    #Raises error if there is a mistake
    with pytest.raises(ParserError):
        parser.consume(TokenType.IDENTIFIER, "error message")