from tests.test_interpreter.test_line_trim import lineTrim

def test_varDeclaration_integer():
    correctLines = lineTrim("integer b=5;")

    assert correctLines[0] == "int b = 5;"

def test_varDeclaration_double():
    correctLines = lineTrim("double b=5.4;")

    assert correctLines[0] == "float b = 5.4;"

def test_varDeclaration_string():
    correctLines = lineTrim('string greating = "Hello my friend";')

    assert correctLines[0] == 'char greating[] = "Hello my friend";'
    
def test_varDeclaration_boolean():
    correctLines = lineTrim("boolean b=true;")

    assert correctLines[0] == "bool b = true;"

def test_varDeclaration_integer_integer():
    correctLines = lineTrim("integer integer=5;")

    assert correctLines[0] == "int integer = 5;"

def test_varDeclaration_integer_boolean():
    correctLines = lineTrim("integer boolean=5;")

    assert correctLines[0] == "int boolean = 5;"