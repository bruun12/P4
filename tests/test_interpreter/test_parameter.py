from tests.test_interpreter.test_line_trim import lineTrim

def test_parameter():
    correctLines = lineTrim("integer x;")
    assert correctLines[0] == "int x;"

