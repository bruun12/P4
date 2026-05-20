from parser.ASTNodes import ReturnStatement, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER, VOID

# Checks it correctly handles a return stmt with an integer return type
def test_valid_return_statement_integer():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
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


# Checks it correctly handles a return type with void
def test_valid_return_statement_void():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
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


# Checks it correctly handles an invalid return value with no void but no return value
def test_invalid_return_statement_non_void_without_value():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
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


# Checks it correctly handles a return-stmt with expected return to be void, but has something else
def test_invalid_return_statement_void_with_value():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
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


# Checks that it correctly handles when a return type has a mismatch in return value
def test_invalid_return_statement_type_mismatch():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    checker.current_function_name = "function"
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


# Checks it correctly handles that return is not the final statement
def test_invalid_return_statement_not_final_statement():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    checker.expected_return_type = INTEGER
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)


# Checks it correctly handles when a return stmt is placed wrongly
def test_invalid_return_statement_not_allowed_here():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    checker.expected_return_type = None
    checker.does_return_correctly = False

    stmt = ReturnStatement(
        value=Literal(5, line=1, column=12),
        line=1,
        column=5,
    )

    checker.check_statement(stmt, env, within_function=True)

    assert any(err.error_code == ErrorCode.INVALID_RETURN_ERROR for err in checker.errors)