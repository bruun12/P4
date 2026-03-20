from src.lexer.lexer import Lexer

def test_skip_comment_with_inline_comment(capsys):
    #string = "int x = 20 // initilizing x"
    lex = Lexer("Hejs")
    assert lex.length == 4
    