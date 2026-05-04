from parser.ASTNodes import AssignStatement, VarDeclaration, ArrayDeclaration, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER, ArrayType

import pytest

def test_valid_assign_statement():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    var = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=13
    )
    
    stmt = AssignStatement(
        name="x",
        offset=None,
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(var, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []
    
    assigned = env.get("x")
    assert assigned == INTEGER
    
def test_valid_assign_statement_array():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    arr_dec = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13),
            Literal(8, line=1, column=13),
            Literal(9, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    
    stmt = AssignStatement(
        name="arr",
        offset=Literal(3, line=1, column=13),
        value=Literal(123, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(arr_dec, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []
    
    assigned = env.get("arr")
    assert isinstance(assigned, ArrayType)
    
def test_invalid_assign_statement_with_unknown_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt = AssignStatement(
        name="x",
        offset=None,
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR for err in checker.errors)

def test_assign_statement_invalid_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    var = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=13
    )
    
    stmt = AssignStatement(
        name="x",
        offset=None,
        value=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(var, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.CANNOT_ASSIGN for err in checker.errors)

def test_assign_statement_array_invalid_element_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    arr_dec = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13),
            Literal(8, line=1, column=13),
            Literal(9, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    
    stmt = AssignStatement(
        name="arr",
        offset=Literal(3, line=1, column=13),
        value=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(arr_dec, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.CANNOT_ASSIGN for err in checker.errors)

def test_assign_statement_array_invalid_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    var = VarDeclaration(
        type="integer",
        name="x",
        value=Literal(5, line=1, column=13),
        line=1,
        column=13
    )

    
    stmt = AssignStatement(
        name="x",
        offset=Literal(3, line=1, column=13),
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(var, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)

def test_assign_statement_array_invalid_offset():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    arr_dec = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13),
            Literal(8, line=1, column=13),
            Literal(9, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    
    stmt = AssignStatement(
        name="arr",
        offset=Literal(-3, line=1, column=13),
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(arr_dec, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_ARGUMENT_COUNT for err in checker.errors)
    
def test_assign_statement_array_invalid_offset():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    arr_dec = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13),
            Literal(8, line=1, column=13),
            Literal(9, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    
    stmt = AssignStatement(
        name="arr",
        offset=Literal(7, line=1, column=13),
        value=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(arr_dec, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_ARGUMENT_COUNT for err in checker.errors)

def test_assign_statement_array_invalid_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    arr_dec = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13),
            Literal(8, line=1, column=13),
            Literal(9, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )
    
    stmt = AssignStatement(
        name="arr",
        offset=None,
        value=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(arr_dec, env, within_function=False)
    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.CANNOT_ASSIGN for err in checker.errors)