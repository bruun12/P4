from tests.test_transpiler.test_line_trim import lineTrim

# With the use of lineTime check for different scenarios in which the function assign() checks if it can assign a name to a value

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