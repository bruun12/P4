from lexer.lexer import Lexer

# checks if it can find the current char (the first one being "i")
def test_current_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.current_char() == "i"
