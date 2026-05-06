from parser.ASTNodes import VarDeclaration, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER, VOID, ERROR


def test_valid_var_declaration():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []
    assert env.get("x") == INTEGER


def test_var_declaration_duplicate_name():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt1 = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    stmt2 = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(10, line=2, column=13),
        line=2,
        column=1,
    )

    checker.check_statement(stmt1, env, within_function=False)
    checker.check_statement(stmt2, env, within_function=False)

    assert any(err.error_code == ErrorCode.ALREADY_DECLARED_ERROR for err in checker.errors)


def test_var_declaration_invalid_initializer_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = VarDeclaration(
        type="integer",
        name="x",
        value=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.CANNOT_ASSIGN for err in checker.errors)


def test_var_declaration_void_type_is_invalid():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = VarDeclaration(
        type="void",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_DECLARED_TYPE for err in checker.errors)


def test_var_declaration_unknown_declared_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()

    stmt = VarDeclaration(
        type="banana",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)
    assert any(err.error_code == ErrorCode.UNKNOWN_DECLARED_TYPE for err in checker.errors)
    assert env.get("x") == ERROR