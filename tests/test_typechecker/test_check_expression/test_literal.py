from parser.ASTNodes import Literal
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


def test_integer_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal(5, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


def test_double_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal(5.5, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == DOUBLE
    assert checker.errors == []


def test_boolean_true_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal(True, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == BOOLEAN
    assert checker.errors == []


def test_boolean_false_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal(False, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == BOOLEAN
    assert checker.errors == []


def test_string_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal("hello", line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == STRING
    assert checker.errors == []


def test_unsupported_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Literal([1, 2, 3], line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)