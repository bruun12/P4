import pytest
from lexer.lexer import Lexer
from lexer.token import TokenType
from error_handling import LexerError


def test_read_simple_string():
    lexer = Lexer('"HejMorten"')
    token = lexer.read_string()

    assert token.type == TokenType.STRING
    assert token.value == "HejMorten"


def test_read_empty_string():
    lexer = Lexer('""')
    token = lexer.read_string()

    assert token.type == TokenType.STRING
    assert token.value == ""


def test_string_with_spaces():
    lexer = Lexer('"hello world"')
    token = lexer.read_string()

    assert token.type == TokenType.STRING
    assert token.value == "hello world"


def test_missing_closing_quote():
    lexer = Lexer('"hello')

    with pytest.raises(LexerError):
        lexer.read_string()