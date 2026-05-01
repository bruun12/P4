from type_checker.TypeChecker import numeric_result_type, INTEGER, DOUBLE, STRING, BOOLEAN

def test_result_of_same_types():
    assert numeric_result_type(DOUBLE, DOUBLE) == DOUBLE
    assert numeric_result_type(INTEGER, INTEGER) == INTEGER

def test_result_of_different_types():
    assert numeric_result_type(DOUBLE, INTEGER) == DOUBLE
    assert numeric_result_type(INTEGER, DOUBLE) == DOUBLE
    assert numeric_result_type(DOUBLE, STRING) == DOUBLE
    assert numeric_result_type(INTEGER, STRING) == INTEGER
    assert numeric_result_type(STRING, INTEGER) == INTEGER
    assert numeric_result_type(INTEGER, BOOLEAN) == INTEGER
    assert numeric_result_type(BOOLEAN, STRING) == INTEGER

def test_incorrect_results():
    assert not numeric_result_type(STRING, INTEGER) == STRING
    assert not numeric_result_type(BOOLEAN, INTEGER) == BOOLEAN
    assert not numeric_result_type(DOUBLE, STRING) == INTEGER
