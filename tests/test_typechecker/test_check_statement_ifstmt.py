from parser.ASTNodes import (
    AssignStatement,
    BlockStatement,
    IfStatement,
    Literal,
    VarDeclaration,
    Variable,
)
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER


def test_if_statement_valid_boolean_condition():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = IfStatement(
        condition=Literal(True, line=1, column=5),
        then_branch=BlockStatement(
            statements=[],
            line=1,
            column=10,
        ),
        else_branch=None,
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []


def test_if_statement_invalid_condition_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = IfStatement(
        condition=Literal(123, line=1, column=5),
        then_branch=BlockStatement(
            statements=[],
            line=1,
            column=10,
        ),
        else_branch=None,
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)


def test_if_statement_checks_then_branch():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = IfStatement(
        condition=Literal(True, line=1, column=5),
        then_branch=BlockStatement(
            statements=[
                AssignStatement(
                    name="x",
                    offset=None,
                    value=Literal(5, line=2, column=9),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=10,
        ),
        else_branch=None,
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR for err in checker.errors)


def test_if_statement_checks_else_branch():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = IfStatement(
        condition=Literal(True, line=1, column=5),
        then_branch=BlockStatement(
            statements=[],
            line=1,
            column=10,
        ),
        else_branch=BlockStatement(
            statements=[
                AssignStatement(
                    name="x",
                    offset=None,
                    value=Literal(5, line=3, column=9),
                    line=3,
                    column=5,
                )
            ],
            line=2,
            column=10,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR for err in checker.errors)


def test_if_statement_then_branch_has_its_own_scope():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = IfStatement(
        condition=Literal(True, line=1, column=5),
        then_branch=BlockStatement(
            statements=[
                VarDeclaration(
                    type="integer",
                    name="x",
                    value=Literal(5, line=2, column=17),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=10,
        ),
        else_branch=None,
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []

    # x should not exist outside the if-branch scope
    assert env.contains_in_current_scope("x") is False