from lexer.lexer import Lexer

# Checks if it correctly reads the next char
def test_peek_next_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.peek_next_char() == "n"

# Checks it does not peek two chars at the same time
def test_not_peek_two_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert not lex.peek_next_char() == "nt"

# Checks if it correctly stops peeking the next line if there is none
def test_stop_peek_next_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)

    while(lex.peek_next_char() is not None):
        lex.advance()

    assert lex.peek_next_char() is None

# Checks it can peek a space
def test_peek_space():
    string = "  int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.peek_next_char() == " "
