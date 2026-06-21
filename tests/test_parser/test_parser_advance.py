from parser.parser import Parser
from lexer.lexer import TokenType, Token

# Checks if it correctly advances to the next token
def test_advance_success():
    tokens = [Token(TokenType.TYPE, "string", 1, 1),
              Token(TokenType.IDENTIFIER, "x", 2, 1)]

    parser = Parser(tokens)
    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.current().type == TokenType.IDENTIFIER

def test_advance_success_with_more_tokens():
    tokens = [Token(TokenType.TYPE, "string", 1, 1),
              Token(TokenType.IDENTIFIER, "x", 2, 1),
              Token(TokenType.ASSIGN, "=", 3, 1),
              Token(TokenType.STRING, "Hey hallo", 4, 1)
              ]

    parser = Parser(tokens)
    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.current().type == TokenType.IDENTIFIER
    parser.advance()
    assert parser.current().type == TokenType.ASSIGN
    parser.advance()
    assert parser.current().type == TokenType.STRING

def test_advance_success_with_even_more():
    tokens = [Token(TokenType.TYPE, "string", 1, 1),
              Token(TokenType.IDENTIFIER, "x", 2, 1),
              Token(TokenType.ASSIGN, "=", 3, 1),
              Token(TokenType.STRING, "Hey hallo", 4, 1),
              Token(TokenType.TYPE, "double", 5, 1),
              Token(TokenType.ASSIGN, "=", 6, 1),
              Token(TokenType.DOUBLE, "3.2", 7, 1)
              ]

    parser = Parser(tokens)
    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.current().type == TokenType.IDENTIFIER
    parser.advance()
    assert parser.current().type == TokenType.ASSIGN
    parser.advance()
    assert parser.current().type == TokenType.STRING
    parser.advance()
    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.current().type == TokenType.ASSIGN
    parser.advance()
    assert parser.current().type == TokenType.DOUBLE

# Tests if advance right to end of file
def test_advance_with_one_token():
    tokens = [
        Token(TokenType.TYPE, "string", 1, 1),
        Token(TokenType.EOF, "", 2, 1)
    ]
    parser = Parser(tokens)

    assert parser.current().type == TokenType.TYPE
    parser.advance()
    assert parser.is_at_end() == True

# Check that advance cant advance over end of file
def test_advance_past_end_of_file_more_times():
    tokens = [
        Token(TokenType.TYPE, "string", 1, 1),
        Token(TokenType.EOF, "", 2, 1)
    ]
    parser = Parser(tokens)

    parser.advance()
    assert parser.is_at_end() == True

    parser.advance()
    parser.advance()
    assert parser.is_at_end() == True
    assert parser.current().type == TokenType.EOF