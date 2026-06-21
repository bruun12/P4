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

# makes use of the has_error function
def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)


# Checks it correctly handles an integer
def test_integer_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal(5, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


# Checks it correctly handles a double
def test_double_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal(5.5, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == DOUBLE
    assert checker.errors == []


# Checks it correctly handles boolean true
def test_boolean_true_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal(True, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == BOOLEAN
    assert checker.errors == []


# Checks it correctly handles boolean false
def test_boolean_false_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal(False, line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == BOOLEAN
    assert checker.errors == []


# Checks it correctly handles a string
def test_string_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal("hello", line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == STRING
    assert checker.errors == []


# Checks it correctly throws an error when an unsupported literal is given
def test_unsupported_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    expr = Literal([1, 2, 3], line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)