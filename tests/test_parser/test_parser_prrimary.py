import pytest

from lexer.lexer import Lexer
from parser.ASTNodes import Literal, ParserError
from parser.parser import Parser


def test_parser_primary_int():
    lex = Lexer("1")
    lex.lexer()
    parser = Parser(lex.tokens)
    
    assert parser.parse_primary().getValue() == 1 

def test_parser_primary_float():
    lex = Lexer("1.1")
    lex.lexer()
    parser = Parser(lex.tokens)

    assert parser.parse_primary().getValue() == 1.1

def test_parser_primary_true():
    lex = Lexer("true")
    lex.lexer()
    parser = Parser(lex.tokens)

    assert parser.parse_primary().getValue()

def test_parser_primary_false():
    lex = Lexer("false")
    lex.lexer()
    parser = Parser(lex.tokens)

    assert not parser.parse_primary().getValue()

def test_parser_primary_string():
    lex = Lexer('"Hey"')
    lex.lexer()
    parser = Parser(lex.tokens)

    assert parser.parse_primary().getValue() == "Hey"