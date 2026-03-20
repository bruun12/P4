from src.lexer.lexer import Lexer

def test_read_number_with_int_input():
    lex = Lexer("123")
    assert lex.read_number() == 123

def test_read_number_with_float_input():
    lex = Lexer("0.987")
    assert lex.read_number() == 0.987

def test_read_number_with_two_dots():
    lex = Lexer("0.42.0")
    assert lex.read_number() is None

def test_read_number_with_stress_input():
    lex = Lexer("1B2___?3")
    assert lex.read_number() == 1