from lexer.lexer import Lexer

def test_current_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.current_char() == "i"
