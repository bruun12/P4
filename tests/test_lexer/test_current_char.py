from lexer.lexer import Lexer

# Checks if it can find the current char (the first one being "i")
def test_current_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.current_char() == "i"

# Checks to ensure it doesn't accept the next char
def test_not_current_char():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert not lex.current_char() == "n"

# Checks to ensure current char doesn't take in two chars
def test_not_two_current_chars():
    string = "int x = 20 // initilizing x"
    lex = Lexer(string)
    assert not lex.current_char() == "in"
    
# Checks if it takes in space as the current char 
def test_space():
    string = "       int x = 20 // initilizing x"
    lex = Lexer(string)
    assert lex.current_char() == " "
    assert not lex.current_char() == "i"

# Checks it correctly takes the next char after advancing
def test_next_current_char():
    string = "int x = 20 // initilizing x"
    lex_next_current = Lexer(string)
    lex_next_current.advance()
    assert lex_next_current.current_char() == "n"
    assert not lex_next_current.current_char == "i"
