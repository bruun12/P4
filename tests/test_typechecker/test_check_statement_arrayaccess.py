from parser.ASTNodes import ArrayDeclaration, Literal, ArrayAccess, VarDeclaration, Variable
from type_checker.TypeChecker import TypeChecker, TypeEnvironment
from error_handling import ErrorCode


def test_valid_array_access_with_literal():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(3, line=1, column=13),
        line=1,
        column=1,
    )
    assign_stmt = VarDeclaration(
                    type="integer",
                    name="x",
                    value=ArrayAccess(
                        name="arr",
                        offset=Literal(1, line=21, column=20),
                        line=21,
                        column=16,
                    ),
                    line=21,
                    column=5,
                )

    checker.check_statement(stmt, env, within_function=False)
    checker.check_statement(assign_stmt, env, within_function=False)

    assert checker.errors == []


def test_valid_array_access_with_variable():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    
    index = VarDeclaration(
                    type="integer",
                    name="index",
                    value=Literal(1, line=21, column=20),
                    line=21,
                    column=5,
                )
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(3, line=1, column=13),
        line=1,
        column=1,
    )
    assign_stmt = VarDeclaration(
                    type="integer",
                    name="x",
                    value=ArrayAccess(
                        name="arr",
                        offset=Variable("index", line=21, column=20),
                        line=21,
                        column=16,
                    ),
                    line=21,
                    column=5,
                )

    checker.check_statement(index, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)
    checker.check_statement(assign_stmt, env, within_function=False)

    assert checker.errors == []

def test_invalid_array_access_with_wrong_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(3, line=1, column=13),
        line=1,
        column=1,
    )
    assign_stmt = VarDeclaration(
                    type="integer",
                    name="x",
                    value=ArrayAccess(
                        name="arr",
                        offset=Literal("index", line=21, column=20),
                        line=21,
                        column=16,
                    ),
                    line=21,
                    column=5,
                )

    checker.check_statement(stmt, env, within_function=False)
    checker.check_statement(assign_stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)

def test_invalid_array_access_with_negative_index():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(3, line=1, column=13),
        line=1,
        column=1,
    )
    assign_stmt = VarDeclaration(
                    type="integer",
                    name="x",
                    value=ArrayAccess(
                        name="arr",
                        offset=Literal(-1, line=21, column=20),
                        line=21,
                        column=16,
                    ),
                    line=21,
                    column=5,
                )

    checker.check_statement(stmt, env, within_function=False)
    checker.check_statement(assign_stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_ARGUMENT_COUNT for err in checker.errors)

def test_invalid_array_access_with_index_out_of_range():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(3, line=1, column=13),
        line=1,
        column=1,
    )
    assign_stmt = VarDeclaration(
                    type="integer",
                    name="x",
                    value=ArrayAccess(
                        name="arr",
                        offset=Literal(3, line=21, column=20),
                        line=21,
                        column=16,
                    ),
                    line=21,
                    column=5,
                )

    checker.check_statement(stmt, env, within_function=False)
    checker.check_statement(assign_stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_ARGUMENT_COUNT for err in checker.errors)


