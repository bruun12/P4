import pytest

from lexer.lexer import Lexer
from parser.parser import Parser


def test_parser_primary_int():
    lex = Lexer("1")
    lex.lexer()
    parser = Parser(lex.tokens)
    
    value = parser.parse_primary().value 

    assert value == 1 

def test_parser_primary_float():
    lex = Lexer("1.1")
    lex.lexer()
    parser = Parser(lex.tokens)

    value = parser.parse_primary().value

    assert value == 1.1

def test_parser_primary_true():
    lex = Lexer("true")
    lex.lexer()
    parser = Parser(lex.tokens)

    value = parser.parse_primary().value

    assert value == True

def test_parser_primary_false():
    lex = Lexer("false")
    lex.lexer()
    parser = Parser(lex.tokens)

    value = parser.parse_primary().value

    assert value == False

def test_parser_primary_string():
    lex = Lexer('"Hey"')
    lex.lexer()
    parser = Parser(lex.tokens)

    value = parser.parse_primary().value

    assert value == "Hey"

def test_parser_primary_LPAREN_RPAREN():
    lex = Lexer("(1)")
    lex.lexer()
    parser = Parser(lex.tokens)

    value = parser.parse_primary().value

    assert value == 1