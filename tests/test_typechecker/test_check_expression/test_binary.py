from parser.ASTNodes import Binary, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import (
    TypeChecker,
    TypeEnvironment,
    INTEGER,
    DOUBLE,
    BOOLEAN,
    STRING,
    ERROR,
)


def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)
def test_binary_add_integer_and_integer():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Binary(
        left=Literal(1, line=1, column=1),
        operator="+",
        right=Literal(2, line=1, column=5),
        line=1,
        column=3,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


def test_binary_add_integer_and_double():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Binary(
        left=Literal(1, line=1, column=1),
        operator="+",
        right=Literal(2.5, line=1, column=5),
        line=1,
        column=3,
    )

    result = checker.check_expression(expr, env)

    assert result == DOUBLE
    assert checker.errors == []


def test_binary_string_plus_string():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Binary(
        left=Literal("hello", line=1, column=1),
        operator="+",
        right=Literal("world", line=1, column=11),
        line=1,
        column=8,
    )

    result = checker.check_expression(expr, env)

    assert result == STRING
    assert checker.errors == []


def test_binary_string_plus_integer_is_invalid():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Binary(
        left=Literal("hello", line=1, column=1),
        operator="+",
        right=Literal(1, line=1, column=11),
        line=1,
        column=8,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)