import pytest
from lexer.lexer import Lexer
from lexer.token import TokenType

def test_read_word_identifier():
    lexer = Lexer('id')
    token = lexer.read_word()

    assert token.type == TokenType.IDENTIFIER
    assert token.value == "id"

def test_read_word_keyword_while():
    lexer = Lexer('while')
    token = lexer.read_word()

    assert token.type == TokenType.WHILE
    assert token.value == "while"

def test_read_word_type_integer():
    lexer = Lexer('integer')
    token = lexer.read_word()

    assert token.type == TokenType.TYPE
    assert token.value == "integer"

def test_read_word_type_string():
    lexer = Lexer('string')
    token = lexer.read_word()

    assert token.type == TokenType.TYPE
    assert token.value == "string"

def test_read_word_type_double():
    lexer = Lexer('double')
    token = lexer.read_word()
    
    assert token.type == TokenType.TYPE
    assert token.value == "double"