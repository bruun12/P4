from tests.test_interpreter.test_line_trim import lineTrim

def test_block_statement():
    correctLines = lineTrim("x = 2;")
    assert correctLines[0] == "x = 2;"

def test_block_statement_with_2():
    correctLines = lineTrim("""{
                integer x = 2;
                integer arr[2] = [1,2];
                            }
                """)
    assert correctLines[0] == "{"
    assert correctLines[1] == "int x = 2;"
    assert correctLines[2] == "int arr[] = {1,2};"
    assert correctLines[3] == "}"

def test_block_statement_with_3():
    correctLines = lineTrim("""{
                integer y = 3;
                integer x = 2;
                double abe = 4.2;
                }""")
    assert correctLines[0] == "{"
    assert correctLines[1] == "int y = 3;"
    assert correctLines[2] == "int x = 2;"
    assert correctLines[3] == "double abe = 4.2;"
    assert correctLines[4] == "}"