from lexer.token import TokenType, Token
from parser.parser import Parser
tokens = [Token(TokenType.WHILE, "while", 1, 1),
            Token(TokenType.LPAREN, "(", 1, 2),
            Token(TokenType.TRUE, "true", 1, 3),
            Token(TokenType.RPAREN, ")", 1, 4),
            Token(TokenType.EOF, "EOF", 1, 5)]

def test_current_while_success():
    parser = Parser(tokens)
    current = parser.current()
    assert current.type == TokenType.WHILE

def test_current_lparen_success():
    parser = Parser(tokens)
    parser.advance()
    current = parser.current()
    assert current.type == TokenType.LPAREN

def test_previous_lparen_success():
    parser = Parser(tokens)
    parser.advance()
    parser.advance()
    current = parser.previous()
    assert current.type == TokenType.LPAREN

def test_previous_true_success():
    parser = Parser(tokens)
    parser.advance()
    parser.advance()
    parser.advance()
    current = parser.previous()
    assert current.type == TokenType.TRUE

def test_is_at_end_true():
    parser = Parser(tokens)
    parser.advance()
    parser.advance()
    parser.advance()
    parser.advance()
    assert parser.is_at_end()

def test_is_at_end_false():
    parser = Parser(tokens)
    parser.advance()
    assert not parser.is_at_end()

def test_peek_normal():
    parser = Parser(tokens)
    peek = parser.peek()
    assert peek.type == TokenType.LPAREN

def test_peek_at_end():
    parser = Parser(tokens)
    parser.advance()
    parser.advance()
    parser.advance()
    parser.advance()
    peek = parser.peek()
    assert peek is None