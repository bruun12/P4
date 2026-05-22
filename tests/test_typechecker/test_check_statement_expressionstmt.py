from parser.ASTNodes import Literal, ExpressionStatement, VarDeclaration

from type_checker.TypeChecker import TypeChecker, TypeEnvironment
from error_handling import ErrorCode

# Checks valid expression
def test_valid_expression():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = ExpressionStatement(Literal(5 ,line = 2,column = 3),line = 1,column = 1,)

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []

def test_invalid_expression():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = ExpressionStatement(
        VarDeclaration(
        type= "integer",
        name= "x",
        value= Literal(5 ,line = 2,column = 3),
        line= 1,
        column=1
        
        )     
    ,line = 1,column = 1,)

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.UNKNOWN_AST_NODE_ERROR for err in checker.errors)