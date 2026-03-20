from src.lexer.lexer import Lexer

def test_skip_comment_with_inline_comment():
    lexer = Lexer("hello world*/x ")

    lexer.skip_comment()
    assert lexer.current_char() == 'x'
