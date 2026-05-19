from parser.ASTNodes import (
    AssignStatement,
    BlockStatement,
    Literal,
    ReturnStatement,
    VarDeclaration,
    Variable,
    WhileStatement,
)
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment


# Checks it correctly handles when a while-stmt recieves a boolean condition
def test_while_statement_valid_boolean_condition():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = WhileStatement(
        condition=Literal(True, line=1, column=8),
        body=BlockStatement(
            statements=[],
            line=1,
            column=14,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []


# Checks it correctly handles when it receives a wrong condition type
def test_while_statement_invalid_condition_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = WhileStatement(
        condition=Literal(123, line=1, column=8),
        body=BlockStatement(
            statements=[],
            line=1,
            column=14,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)


# Checks it correctly checks the entire while body
def test_while_statement_checks_body():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = WhileStatement(
        condition=Literal(True, line=1, column=8),
        body=BlockStatement(
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
            column=14,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR for err in checker.errors)


# Checks it correctly checks its own body scope
def test_while_statement_body_has_its_own_scope():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = WhileStatement(
        condition=Literal(True, line=1, column=8),
        body=BlockStatement(
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
            column=14,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []
    assert env.contains_in_current_scope("x") is False


# Checks it correctly handles when the user tries to make a nested return 
def test_while_statement_nested_return_is_invalid():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    checker.expected_return_type = None

    stmt = WhileStatement(
        condition=Literal(True, line=1, column=8),
        body=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Literal(1, line=2, column=12),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=14,
        ),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)