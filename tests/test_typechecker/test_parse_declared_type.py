from type_checker.ClassesAndHelpers import parse_declared_type, TypeCheckError, INTEGER, DOUBLE, BOOLEAN, STRING, VOID
import pytest

def test_correct_type():
    assert parse_declared_type("integer") == INTEGER
    assert parse_declared_type("double") == DOUBLE
    assert parse_declared_type("boolean") == BOOLEAN
    assert parse_declared_type("string") == STRING
    assert parse_declared_type("void") == VOID

def test_type_error_int():
    with pytest.raises(TypeCheckError):
        parse_declared_type("int")
    
def test_type_error_double():
    with pytest.raises(TypeCheckError):
        parse_declared_type("float")

def test_type_error_case_sensitive():
    with pytest.raises(TypeCheckError):
        parse_declared_type("INTEGER")

def test_type_error_extra_space():
    with pytest.raises(TypeCheckError):
        parse_declared_type("void ")