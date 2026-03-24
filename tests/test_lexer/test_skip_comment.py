import pytest
from src.lexer.lexer import Lexer, MyCustomError

def test_skip_comment_with_inline_comment():
    lexer = Lexer("hello world*/x ")

    lexer.skip_comment()
    assert lexer.current_char() == 'x'

def test_skip_comment_empty():
    lexer = Lexer("*/x")

    lexer.skip_comment()
    assert lexer.current_char() == 'x'

def test_skip_comment_no_end():
    lexer = Lexer("hello world")

    with pytest.raises(MyCustomError, match="Comment is never ended"): # Used pytest, for allowing the test to fail
        lexer.skip_comment()

def test_skip_comment_slash_before_end():
    lexer = Lexer(" comment * / still comment */x")

    lexer.skip_comment()
    assert lexer.current_char() == 'x'
