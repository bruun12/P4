from parser.ASTNodes import (
    AssignStatement,
    BlockStatement,
    Literal,
    ReturnStatement,
    VarDeclaration,
    Variable,
    WhileStatement,
    ExpressionStatement
)

from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment

# Checks valid expression
def test_valid_expression():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = ExpressionStatement(Literal(5,2,3),1,1,)

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []