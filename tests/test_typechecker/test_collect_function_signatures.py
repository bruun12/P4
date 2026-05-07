from parser.ASTNodes import (
    ExpressionStatement,
    Literal,
    Function,
    Program
)
from error_handling import ErrorCode, TypeCheckError
from type_checker.TypeChecker import TypeChecker, Parameter

# Error with duplication of functionname
def test_error_for_duplicated_funcs_name():
    checker = TypeChecker(source_code="")
    

    function1 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function2 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    program = Program(functions=[function1, function2], line=30, column=20)
    
    checker.collect_function_signatures(program)

    assert len(checker.errors) == 1 #there should only be one error
    assert checker.errors[0].error_code == TypeCheckError("Function 'func1' is already declared.", ErrorCode.ALREADY_DECLARED_ERROR, 3, 4).error_code

# Error with duplication of functionname but different type
def test_error_for_duplicated_funcs_name_different_type():
    checker = TypeChecker(source_code="")
    

    function1 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function2 = Function(return_type="double", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    program = Program(functions=[function1, function2], line=30, column=20)
    
    checker.collect_function_signatures(program)

    assert len(checker.errors) == 1 #there should only be one error
    assert checker.errors[0].error_code == TypeCheckError("Function 'func1' is already declared.", ErrorCode.ALREADY_DECLARED_ERROR, 3, 4).error_code


#Test that for different functione names there should be no errors
def test_no_error_for_different_funcs_name():
    checker = TypeChecker(source_code="")
    

    function1 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function2 = Function(return_type="integer", name="func2", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    program = Program(functions=[function1, function2], line=30, column=20)
    
    checker.collect_function_signatures(program)

    assert len(checker.errors) == 0
    
#Test that it gives an error for each error
def test_error_for_multiple_duplicated_funcs_name():
    checker = TypeChecker(source_code="")
    

    function1 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function2 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function3 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    function4 = Function(return_type="integer", name="func1", parameters=[], statement=ExpressionStatement(Literal(1,2,3),2,3), line=3, column=4)
    program = Program(functions=[function1, function2, function3, function4], line=30, column=20)
    
    checker.collect_function_signatures(program)

    assert len(checker.errors) == 3 #there should only be 3 errors
    assert checker.errors[0].error_code == TypeCheckError("Function 'func1' is already declared.", ErrorCode.ALREADY_DECLARED_ERROR, 3, 4).error_code
    assert checker.errors[1].error_code == TypeCheckError("Function 'func1' is already declared.", ErrorCode.ALREADY_DECLARED_ERROR, 3, 4).error_code
    assert checker.errors[2].error_code == TypeCheckError("Function 'func1' is already declared.", ErrorCode.ALREADY_DECLARED_ERROR, 3, 4).error_code
