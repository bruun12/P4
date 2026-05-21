from parser.ASTNodes import Literal, ExpressionStatement

from type_checker.TypeChecker import TypeChecker, TypeEnvironment

# Checks valid expression
def test_valid_expression():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = ExpressionStatement(Literal(5,2,3),1,1,)

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []