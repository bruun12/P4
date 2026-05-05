import pytest

from error_handling import ErrorCode
from parser.ASTNodes import (
    BlockStatement,
    Function,
    Literal,
    Parameter,
    ReturnStatement,
    VarDeclaration,
)
from type_checker.TypeChecker import TypeChecker


def make_checker():
    return TypeChecker(source_code="")


def test_valid_non_void_function():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(0, line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert checker.errors == []


def test_missing_return_in_non_void_function():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                VarDeclaration(
                    type="integer",
                    name="x",
                    value=Literal(1, line=2, column=17),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert len(checker.errors) == 1
    assert checker.errors[0].error_code == ErrorCode.MISSING_RETURN_ERROR


def test_duplicate_parameter_names():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[
            Parameter("integer", "x", line=1, column=18),
            Parameter("integer", "x", line=1, column=29),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(0, line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=35,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.ALREADY_DECLARED_ERROR for err in checker.errors)


def test_void_parameter_is_invalid():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[
            Parameter("void", "x", line=1, column=18),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(0, line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=28,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.INVALID_PARAMETER_TYPE for err in checker.errors)


def test_return_type_mismatch():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal("hello", line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)


def test_return_not_final_statement():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(1, line=2, column=12),
                    line=2,
                    column=5,
                ),
                VarDeclaration(
                    type="integer",
                    name="x",
                    value=Literal(2, line=3, column=17),
                    line=3,
                    column=5,
                ),
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)


def test_void_function_returning_value():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="void",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(1, line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=13,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)


def test_non_void_function_return_without_value():
    checker = TypeChecker(source_code="")

    fn = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=None,
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    checker.check_function(fn)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)