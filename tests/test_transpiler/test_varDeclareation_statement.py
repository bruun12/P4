import pytest
from tests.test_transpiler.test_line_trim import lineTrim
from error_handling import LexerError, ParserError, ErrorCode

def test_varDeclaration_integer():
    correctLines = lineTrim("integer b=5;")

    assert correctLines[0] == "int b = 5;"

def test_varDeclaration_double():
    correctLines = lineTrim("double b=5.4;")

    assert correctLines[0] == "double b = 5.4;"

def test_varDeclaration_string():
    correctLines = lineTrim('string greating = "Hello my friend";')

    assert correctLines[0] == 'char* greating = "Hello my friend";'
    
def test_varDeclaration_boolean():
    correctLines = lineTrim("boolean b=true;")

    assert correctLines[0] == "bool b = true;"

# checks for banned keywords should be stopped at the lexer
def test_integer_int_edgecase():
    with pytest.raises(LexerError) as err:
        lineTrim("integer int = 5;")
    assert err.value.error_code == ErrorCode.BANNED_WORD

# since while is a banned word but is used in cimple
# the error is allowed in the lexer
# but it is a structural error and is there for thrown in the parser    
def test_boolean_while_edgecase():
    with pytest.raises(ParserError) as err:
        lineTrim("boolean while = true;")
    assert err.value.error_code == ErrorCode.STRUCTURE_ERROR

