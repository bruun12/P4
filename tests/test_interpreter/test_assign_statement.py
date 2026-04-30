from tests.test_interpreter.test_line_trim import lineTrim

def test_assign_var_simple():
    correctLines = lineTrim("b=5;")

    assert correctLines[0] == "b = 5;"


def test_assign_var_expression():
    correctLines = lineTrim("a=3+5;")

    assert correctLines[0] == "a = (3 + 5);"

    
def test_assign_var_to_var():
    correctLines = lineTrim("b=a;")

    assert correctLines[0] == "b = a;"


def test_assign_var_space():
    correctLines = lineTrim("""b
                            =                  a
                            ;""")

    assert correctLines[0] == "b = a;"
    
def test_assign_arr_simple_index():
    correctLines = lineTrim("a[1]=5;")

    assert correctLines[0] == "a[1] = 5;"

def test_assign_arr_index_space():
    correctLines = lineTrim("""a[
                                5]
                                =5;""")

    assert correctLines[0] == "a[5] = 5;"
    

def test_assign_arr_binary_index():
    correctLines = lineTrim("a[1+5]=5;")

    assert correctLines[0] == "a[(1 + 5)] = 5;"
    
def test_assign_arr_simple_binary_value():
    correctLines = lineTrim("a[5]=1+5;")

    assert correctLines[0] == "a[5] = (1 + 5);"