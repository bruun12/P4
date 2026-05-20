from type_checker.ClassesAndHelpers import is_numeric, INTEGER, DOUBLE, STRING, BOOLEAN, VOID

# Checks whether or not the char is a number

def test_valid_numbers():
    assert is_numeric(INTEGER)
    assert is_numeric(DOUBLE)

def test_invalid_values():
    assert not is_numeric(STRING)

def test_boolean():
    assert not is_numeric(BOOLEAN)

def test_empty():
    assert not is_numeric(VOID)
