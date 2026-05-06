from parser.ASTNodes import FunctionCall, Literal, Variable
from error_handling import ErrorCode
from type_checker.TypeChecker import (
    TypeChecker,
    TypeEnvironment,
    FunctionType,
    INTEGER,
    DOUBLE,
    BOOLEAN,
    STRING,
    VOID,
    ERROR,
    ArrayType,
)


def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)


def test_valid_function_call_returns_declared_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    checker.function_env.define(
        "add",
        FunctionType(
            parameter_types=(INTEGER, INTEGER),
            return_type=INTEGER,
        ),
    )

    expr = FunctionCall(
        name="add",
        arguments=[
            Literal(1, line=1, column=5),
            Literal(2, line=1, column=8),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert checker.errors == []


def test_function_call_undefined_function():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = FunctionCall(
        name="mystery",
        arguments=[
            Literal(1, line=1, column=9),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.UNDEFINED_FUNCTION_ERROR)


def test_function_call_wrong_argument_count():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    checker.function_env.define(
        "add",
        FunctionType(
            parameter_types=(INTEGER, INTEGER),
            return_type=INTEGER,
        ),
    )

    expr = FunctionCall(
        name="add",
        arguments=[
            Literal(1, line=1, column=5),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.INVALID_ARGUMENT_COUNT)


def test_function_call_wrong_argument_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    checker.function_env.define(
        "add",
        FunctionType(
            parameter_types=(INTEGER, INTEGER),
            return_type=INTEGER,
        ),
    )

    expr = FunctionCall(
        name="add",
        arguments=[
            Literal("hello", line=1, column=5),
            Literal(2, line=1, column=14),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == INTEGER
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)


def test_valid_print_function_multiple_arguments():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    env.define("x", INTEGER)
    env.define("y", INTEGER)

    expr = FunctionCall(
        name="print",
        arguments=[
            Literal("x = ", line=1, column=7),
            Variable("x", line=1, column=15),
            Literal(" and y = ", line=1, column=18),
            Variable("y", line=1, column=31),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == VOID
    assert checker.errors == []


def test_print_requires_at_least_one_argument():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = FunctionCall(
        name="print",
        arguments=[],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.INVALID_ARGUMENT_COUNT)


def test_print_rejects_non_printable_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    env.define("arr", ArrayType(INTEGER, 3))

    expr = FunctionCall(
        name="print",
        arguments=[
            Variable("arr", line=1, column=7),
        ],
        line=1,
        column=1,
    )

    result = checker.check_expression(expr, env)

    assert result == VOID
    assert has_error(checker, ErrorCode.TYPE_MISMATCH_ERROR)