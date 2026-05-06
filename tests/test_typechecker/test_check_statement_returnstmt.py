from parser.ASTNodes import ReturnStatement, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER, VOID


def test_valid_return_statement_integer():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = INTEGER
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert checker.errors == []
    assert checker.does_return_correctly is True


def test_valid_return_statement_void():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = VOID
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=None,
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert checker.errors == []
    assert checker.does_return_correctly is True


def test_invalid_return_statement_non_void_without_value():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = INTEGER
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=None,
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)
    assert checker.does_return_correctly is False


def test_invalid_return_statement_void_with_value():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = VOID
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)
    assert checker.does_return_correctly is False


def test_invalid_return_statement_type_mismatch():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = INTEGER
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal("hello", line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)
    assert checker.does_return_correctly is True


def test_invalid_return_statement_not_final_statement():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = INTEGER
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)


def test_invalid_return_statement_not_allowed_here():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    checker.expected_return_type = None
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)