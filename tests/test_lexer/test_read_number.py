from src.lexer.lexer import Lexer

def test_read_number_with_number_input():
    lex = Lexer("123t")
    assert lex.read_number() == 123