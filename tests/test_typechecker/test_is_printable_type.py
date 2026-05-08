from type_checker.ClassesAndHelpers import INTEGER, DOUBLE, BOOLEAN, STRING, ERROR, VOID, ArrayType, FunctionType
from type_checker.TypeChecker import TypeChecker

def test_is_printable_type():
    checker = TypeChecker(source_code="")

    assert checker.is_printable_type(INTEGER)
    assert checker.is_printable_type(DOUBLE)
    assert checker.is_printable_type(BOOLEAN)
    assert checker.is_printable_type(STRING)

def test_is_not_printable_type():
    checker = TypeChecker(source_code="")

    assert not checker.is_printable_type(ERROR)
    assert not checker.is_printable_type(VOID)
    assert not checker.is_printable_type(ArrayType)
    assert not checker.is_printable_type(FunctionType)
