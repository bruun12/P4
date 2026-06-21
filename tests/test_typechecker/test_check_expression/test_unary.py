from parser.ASTNodes import Unary, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import (
    TypeChecker,
    TypeEnvironment,
    INTEGER,
    DOUBLE,
    BOOLEAN,
    ERROR,
)

# makes use of the has_error function
def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)


# Checks it correctly handles a minus with an integer
def test_unary_minus_integer():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Unary(
        operator="-",
        right=Literal(5, line=1, column=2),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


# Checks it correctly handles a minus with a double
def test_unary_minus_double():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Unary(
        operator="-",
        right=Literal(5.5, line=1, column=2),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == DOUBLE
    assert checker.errors == []


# Checks it correctly handles an error when minuses a string
def test_unary_minus_string_is_invalid():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Unary(
        operator="-",
        right=Literal("hello", line=1, column=2),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)


# Checks it correctly handles the NOT symbol in front of a boolean value
def test_unary_not_boolean():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Unary(
        operator="!",
        right=Literal(True, line=1, column=2),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == BOOLEAN
    assert checker.errors == []


# Checks it correctly handles the NOT symbol in front of an integer value
# should give error as you cannot do that
def test_unary_not_integer_is_invalid():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Unary(
        operator="!",
        right=Literal(1, line=1, column=2),
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)