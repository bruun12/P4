from type_checker.TypeChecker import can_assign, INTEGER, DOUBLE, STRING, BOOLEAN, ArrayType


def test_same_type():
    assert can_assign(INTEGER, INTEGER)
    assert can_assign(DOUBLE, DOUBLE)
    assert can_assign(BOOLEAN, BOOLEAN)
    assert can_assign(STRING, STRING)

def test_int_to_double():
    assert can_assign(DOUBLE, INTEGER)

def test_double_to_int():
    assert not can_assign(INTEGER, DOUBLE)

def test_wrong_assign_type():
    assert not can_assign(DOUBLE, BOOLEAN)
    assert not can_assign(STRING, DOUBLE)
    assert not can_assign(DOUBLE, STRING)
    
def test_same_array_type():
    assert can_assign(ArrayType(INTEGER, 1), ArrayType(INTEGER, 1))
    assert can_assign(ArrayType(DOUBLE, 2), ArrayType(DOUBLE, 1))
    assert can_assign(ArrayType(STRING, 1), ArrayType(STRING, 1))

def test_different_array_type():
    assert not can_assign(ArrayType(INTEGER, 1), ArrayType(DOUBLE, 1))
    assert not can_assign(ArrayType(DOUBLE, 2), ArrayType(STRING, 1))
    assert not can_assign(ArrayType(STRING, 1), ArrayType(INTEGER, 1))
