from type_checker.TypeChecker import type_name, ArrayType, FunctionType, Type, INTEGER, DOUBLE, BOOLEAN, VOID, STRING, ERROR

class DummyTest(Type):
    pass

def test_correct_types():
    assert type_name(INTEGER) == "integer"
    assert type_name(DOUBLE) == "double"
    assert type_name(BOOLEAN) == "boolean"
    assert type_name(STRING), "string"
    assert type_name(VOID), "void"
    assert type_name(ERROR), "<error>"

def test_array_type():
    arrayObj_int = ArrayType(INTEGER, 1)
    arrayObj_str = ArrayType(STRING, 1)
    arrayObj_bool = ArrayType(BOOLEAN, 1)
    arrayObj_void = ArrayType(VOID, 1)

    assert type_name(arrayObj_int) == "integer[]"
    assert type_name(arrayObj_int) != "integer"
    assert type_name(arrayObj_str) == "string[]"
    assert type_name(arrayObj_str) != "string"
    assert type_name(arrayObj_bool) == "boolean[]"
    assert type_name(arrayObj_bool) != "boolean"
    assert type_name(arrayObj_void) == "void[]"
    assert type_name(arrayObj_void) != "void" 
    
def test_nested_array_type():
    arrayObj_nested_int = ArrayType(ArrayType(INTEGER, 1),1)
    arrayObj_nested_str = ArrayType(ArrayType(STRING,1), 1)
    arrayObj_nested_bool = ArrayType(ArrayType(BOOLEAN, 1), 1)
    arrayObj_nested_void = ArrayType(ArrayType(VOID, 1), 1)

    assert type_name(arrayObj_nested_int) == "integer[][]"
    assert type_name(arrayObj_nested_int) != "integer[]"
    assert type_name(arrayObj_nested_str) == "string[][]"
    assert type_name(arrayObj_nested_str) != "string[]"
    assert type_name(arrayObj_nested_bool) == "boolean[][]"
    assert type_name(arrayObj_nested_bool) != "boolean[]"
    assert type_name(arrayObj_nested_void) == "void[][]"
    assert type_name(arrayObj_nested_void) != "void[]"

def test_function_type():
    funcObj = FunctionType(
        parameter_types=(INTEGER,),
        return_type=STRING
    )
        
    assert type_name(funcObj) == "function(integer) -> string"
    assert type_name(funcObj) != "function(integer, integer) -> string"

def test_function_tuple_type():
    funcObj = FunctionType(
        parameter_types=(INTEGER, DOUBLE),
        return_type=BOOLEAN
    )
        
    assert type_name(funcObj) == "function(integer, double) -> boolean"
    assert type_name(funcObj) != "function(double, integer) -> string"

def test_array_function_type():
    funcObj = FunctionType(
        parameter_types=[ArrayType(INTEGER,1),ArrayType(BOOLEAN,1,)],
        return_type=STRING
    )
    assert type_name(funcObj) == "function(integer[], boolean[]) -> string"

def test_repr_type():
    tObj = DummyTest()

    assert type_name(tObj) == repr(tObj)
