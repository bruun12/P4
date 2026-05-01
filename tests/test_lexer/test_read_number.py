import pytest

from lexer.lexer import Lexer, TokenType
from error_handling import LexerError

def test_read_number_with_int_input():
    lex = Lexer("123")
    token = lex.read_number()
    assert token.type == TokenType.INTEGER
    assert token.value == 123

def test_read_number_with_double_input():
    lex = Lexer("0.987")
    token = lex.read_number()
    assert token.type == TokenType.DOUBLE
    assert token.value == 0.987

def test_read_number_with_two_dots():
    lex = Lexer("0.42.0")
    #Expects the program to throw error numbered accordinly to the issue
    with pytest.raises(LexerError) as err:    
        lex.read_number()    
    assert err.value.error_code == 12

def test_read_number_with_stress_input():
    lex = Lexer("1B2___?3")
    token = lex.read_number()
    assert token.type == TokenType.INTEGER
    assert token.value == 1
