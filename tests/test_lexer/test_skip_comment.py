import pytest
from lexer.lexer import Lexer
from error_handling import LexerError

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

    with pytest.raises(LexerError) as err: # Used pytest, for allowing the test to fail
        lexer.skip_comment()
        assert err.value.error_code == 420

def test_skip_comment_slash_before_end():
    lexer = Lexer(" comment * / still comment */x")

    lexer.skip_comment()
    assert lexer.current_char() == 'x'
