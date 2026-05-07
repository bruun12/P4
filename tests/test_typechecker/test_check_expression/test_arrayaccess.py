from parser.ASTNodes import ArrayAccess, Literal, Variable
from error_handling import ErrorCode
from type_checker.TypeChecker import (
    TypeChecker,
    TypeEnvironment,
    ArrayType,
    INTEGER,
    ERROR,
)


def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)


def test_valid_array_access_returns_element_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    env.define("nums", ArrayType(INTEGER, 5))

    expr = ArrayAccess(
        name="nums",
        offset=Literal(2, line=1, column=6),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


def test_array_access_undefined_variable():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = ArrayAccess(
        name="nums",
        offset=Literal(2, line=1, column=6),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.UNDEFINED_VARIABLE_ERROR)


def test_array_access_on_non_array():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    env.define("x", INTEGER)

    expr = ArrayAccess(
        name="x",
        offset=Literal(0, line=1, column=3),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)


def test_array_access_requires_integer_index():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    env.define("nums", ArrayType(INTEGER, 5))

    expr = ArrayAccess(
        name="nums",
        offset=Literal("hello", line=1, column=6),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)


def test_array_access_negative_literal_index():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    env.define("nums", ArrayType(INTEGER, 5))

    expr = ArrayAccess(
        name="nums",
        offset=Literal(-1, line=1, column=6),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert has_error(checker, ErrorCode.INVALID_ARGUMENT_COUNT)