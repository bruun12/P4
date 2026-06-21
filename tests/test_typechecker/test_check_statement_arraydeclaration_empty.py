from parser.ASTNodes import ArrayDeclarationEmpty, Literal
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, ArrayType, INTEGER

# Checks if it can declare an empty array
def test_valid_empty_array_declaration():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    
    stmt = ArrayDeclarationEmpty(
        type="integer",
        name="arr",
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


# Checks if it will throw an error if missing information(?)
def test_empty_array_declaration_requires_integer_size():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)

    stmt = ArrayDeclarationEmpty(
        type="integer",
        name="arr",
        size=Literal("hello", line=1, column=13),
        line=1,
        column=1,
    )

    checker.check_statement(stmt, env, within_function=False)

    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)

# Checks if it correctly handles an array with a void return type
def test_empty_array_declaration_cannot_have_void_element_type():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    
    stmt = ArrayDeclarationEmpty(
        type="void",
        name="arr",
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )
    
    checker.check_statement(stmt, env, within_function=False)
    
    assert any(err.error_code == ErrorCode.INVALID_DECLARED_TYPE for err in checker.errors)
    
# Checks if it correctly handles two empty arrays with the same name
def test_empty_array_declaration_duplicate_name():
    checker = TypeChecker(source_code="")
    env = TypeEnvironment(None)
    
    stmt1 = ArrayDeclarationEmpty(
        type="integer",
        name="arr",
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )
    
    stmt2 = ArrayDeclarationEmpty(
        type="integer",
        name="arr",
        size=Literal(5, line=1, column=13),
        line=1,
        column=1,
    )
    
    checker.check_statement(stmt1, env, within_function=False)
    checker.check_statement(stmt2, env, within_function=False)
    
    assert any(err.error_code == ErrorCode.ALREADY_DECLARED_ERROR for err in checker.errors)