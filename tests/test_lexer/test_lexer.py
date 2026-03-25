from lexer.lexer import Lexer

def test_lexer():
    lex = Lexer("integer x = \"Hello world!\";")

    lex.lexer()

    assert len(lex.tokens) == 4
    #and some more assertions 