import pytest
from lexer.lexer import Lexer
from parser.parser import Parser
from error_handling import ParserError

def parse_args(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    return p.arguments()

def test_empty_argument_list():
    args = parse_args("()")

    assert len(args) == 0

def test_single_argument_string():
    args = parse_args("""("String")""")

    assert len(args) == 1
    assert args[0].value == "String"

def test_single_argument_integer():
    args = parse_args("""(1)""")

    assert len(args) == 1
    assert args[0].value == 1

def test_single_argument_double():
    args = parse_args("""(1.2)""")

    assert len(args) == 1
    assert args[0].value == 1.2

def test_single_argument_boolean():
    args = parse_args("""(true)""")

    assert len(args) == 1
    assert args[0].value

def test_single_argument_variable():
    args = parse_args("""(x)""")

    assert len(args) == 1
    assert args[0].name == "x"

def test_multi_argument():
    args = parse_args("""(x, "String", 2)""")

    assert len(args) == 3
    assert args[0].name == "x"
    assert args[1].value == "String"
    assert args[2].value == 2

def test_multi_argument_complex_expression():
    args = parse_args("""(x + 1, y < 5)""")

    assert len(args) == 2
    assert args[0].left.name == "x"
    assert args[0].right.value == 1
    assert args[1].left.name == "y"
    assert args[1].right.value == 5
