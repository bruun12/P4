from lexer.lexer import Lexer

# Checks if it can advance one line
def test_advance_one_line():
    string = "int x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    while(lex.peek_next_char() is not None):
        lex.advance()

    assert not lex.line == 1
    assert lex.line == 2
    assert lex.column == 9

# Checks it cannot advance to a line and column that does not exist
def test_cannot_advance():
    string = "int x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    while(lex.current_char() is not None):
        lex.advance()

    assert lex.advance() is None
    assert not lex.line == 3 # to explicit show it does not take the next line
