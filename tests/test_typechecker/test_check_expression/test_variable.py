from parser.ASTNodes import Literal, Variable
from error_handling import ErrorCode
from type_checker.TypeChecker import (
    TypeChecker,
    TypeEnvironment,
    VarDeclaration,
    INTEGER,
    ERROR,
)

def has_error(checker, error_code):
    return any(err.error_code == error_code for err in checker.errors)

def test_valid_variable():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, False)
    
    result = env.get("x")

    assert result == INTEGER
    assert checker.errors == []

def test_invalid_variable_use():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    expr = Variable("x", line=1, column=1)

    result = checker.check_expression(expr, env)

    assert result == ERROR
    assert has_error(checker, ErrorCode.UNDEFINED_VARIABLE_ERROR)
