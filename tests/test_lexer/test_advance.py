from src.lexer.lexer import Lexer

def test_advance():
    string = "int x = 20 // initilizing x\ny = x * 5"
    lex = Lexer(string)

    while(lex.peek_next_char() is not None):
        lex.advance()

    assert lex.line == 2
    assert lex.column == 9