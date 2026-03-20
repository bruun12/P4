from src.lexer.lexer import Lexer

def test_peek_next_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.peek_next_char() == "n"
