from tests.test_interpreter.test_line_trim import lineTrim

def test_varDeclaration_simple():
    correctLines = lineTrim("integer b=5;")

    assert correctLines[0] == "integer b = 5;"
