from parser.ASTNodes import ArrayDeclaration, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, ArrayType, INTEGER

import pytest

def test_valid_array_declaration():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt = ArrayDeclaration(
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

    checker.check_statement(stmt, env, within_function=False)

    assert checker.errors == []
    
    declared = env.get("arr")
    assert isinstance(declared, ArrayType)
    assert declared.element_type == INTEGER
    assert declared.size == 5

def test_array_declaration_cannot_return_void ():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt = ArrayDeclaration(
        type="void",
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

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_DECLARED_TYPE for err in checker.errors)

def test_array_declaration_requires_integer_size ():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[],
        size=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)

def test_array_declaration_duplicate_name():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt1 = ArrayDeclaration(
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
    
    stmt2 = ArrayDeclaration(
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
    
    checker.check_statement(stmt1, env, within_function=False)
    checker.check_statement(stmt2, env, within_function=False)
    
    assert any(err.error_code == ErrorCode.ALREADY_DECLARED_ERROR for err in checker.errors)
    
def test_invalid_array_declaration_missing_elements ():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment()
    
    stmt = ArrayDeclaration(
        type="integer",
        name="arr",
        elements=[
            Literal(5, line=1, column=13),
            Literal(6, line=1, column=13),
            Literal(7, line=1, column=13)
        ],
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.INVALID_ARGUMENT_COUNT for err in checker.errors)
