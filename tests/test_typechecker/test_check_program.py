from type_checker.TypeChecker import TypeChecker, Program, Function
from parser.ASTNodes import BlockStatement, ReturnStatement, Literal
from error_handling import TypeCheckError, ErrorCode


# tjekker om den køre programmet igennem rigtigt
def test_check_program():
    checker = TypeChecker(source_code="")

    stmt = ReturnStatement(
        value=Literal(5, 2, 1), 
        line=2, 
        column=1
    )

    func = Function (
        return_type="integer",
        name="test_function",
        parameters=[],
        statement=stmt, 
        line=1, 
        column=1
    )
    
    program = Program(functions=[func], line=1, column=1)

    checker.check(program)

    assert len(checker.errors) == 0
    assert not checker.has_errors() # for at eksplicitere at der ikke er nogen errors


# tjekker om programmet kan køre selvom den ikke har nogen returværdi
def test_check_missing_return():
    checker = TypeChecker(source_code="")

    stmt = BlockStatement(
        statements=[],
        line=1,
        column=1
    )

    func = Function (
        return_type="void",
        name="test_function",
        parameters=[],
        statement=stmt, 
        line=1, 
        column=1
    )
    
    program = Program(functions=[func], line=1, column=1)

    checker.check(program)

    assert len(checker.errors) == 0 # nul errors fordi en blockstmt ikke returnere noget


# tjekker om programmet kan håndtere et tomt program
def test_check_empty_program():
    checker = TypeChecker(source_code="")
    
    program = Program(functions=[], line=1, column=1)

    checker.check(program)

    assert len(checker.errors) == 0


def test_error_two_same_functions():
    checker = TypeChecker(source_code="")

    stmt = BlockStatement(
        statements=[],
        line=1,
        column=1
    )

    func1 = Function (
        return_type="void",
        name="test_function",
        parameters=[],
        statement=stmt, 
        line=1, 
        column=1
    )

    func2 = Function (
        return_type="void",
        name="test_function",
        parameters=[],
        statement=stmt, 
        line=5, 
        column=1
    )

    program = Program(functions=[func1, func2], line=1, column=1)

    checker.check(program)

    assert len(checker.errors) == 1

    err = checker.errors[0] 

    # for at sikre det er det rigtige objekt der bliver brugt
    assert isinstance(err, TypeCheckError)

    # tjekker at det er den korrekte fejl vi har at gøre med
    assert err.line != 1 # det er ikke den første func der er den duplicate
    assert err.line == 5 # det er den anden func der er den duplicate
    assert err.column == 1
    assert err.error_code == ErrorCode.ALREADY_DECLARED_ERROR
    assert err.message == "Function 'test_function' is already declared."
