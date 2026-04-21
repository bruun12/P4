import pytest
from lexer.lexer import Lexer
from parser.parser import Parser
from error_handling import ParserError

def parse_params(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    return p.parameters()

def test_empty_paramlist():
    params = parse_params("()")

    assert len(params) == 0

def test_sigle_param():
    params = parse_params("(integer x)")

    assert len(params) == 1
    assert params[0].type == "integer"
    assert params[0].name == "x"

def test_double_params():
    params = parse_params("(integer x, string y)")

    assert len(params) == 2
    assert params[0].type == "integer"
    assert params[0].name == "x"
    assert params[1].type == "string"
    assert params[1].name == "y"


def test_multiple_params():
    params = parse_params("(integer xoxo, string yes, boolean bool, double d)")

    assert len(params) == 4
    assert params[0].type == "integer"
    assert params[0].name == "xoxo"
    assert params[1].type == "string"
    assert params[1].name == "yes"
    assert params[2].type == "boolean"
    assert params[2].name == "bool"
    assert params[3].type == "double"
    assert params[3].name == "d"

def test_syntax_error_in_params():
    with pytest.raises(ParserError):
        parse_params("(integer xoxo,, string yes)")

def test_syntax_error_in_params2():
    with pytest.raises(ParserError):
        parse_params("(integer xoxo string yes)")

def test_syntax_error_in_params3():
    with pytest.raises(ParserError):
        parse_params("(integer xoxo = 1)")
