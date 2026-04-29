from tests.test_interpreter.test_line_trim import lineTrim

def test_if_statement_simple():
    correctLines = lineTrim("""if(true){}""")

    assert correctLines[0] == "if (true)"
    assert correctLines[1] == "{"
    assert correctLines[2] == "}"

def test_if_statement_while():
    correctLines = lineTrim("""if(a<b){x=5;
                            while(false){
                            a = a+b;
                            }
                            7+5;
                            }""")

    assert correctLines[0] == "if ((a < b))"
    assert correctLines[1] == "{"
    assert correctLines[2] == "x = 5;"
    assert correctLines[3] == "while (false)"
    assert correctLines[4] == "{"
    assert correctLines[5] == "a = (a + b);"
    assert correctLines[6] == "}"
    assert correctLines[7] == "(7 + 5);"
    assert correctLines[8] == "}"

def test_if_statement_else():
    correctLines = lineTrim("""if(10<9){
                                   a = a + 7;
                               }else{
                                   a = 5;
                               }""")

    assert correctLines[0] == "if ((10 < 9))"
    assert correctLines[1] == "{"
    assert correctLines[2] == "a = (a + 7);"
    assert correctLines[3] == "}"
    assert correctLines[4] == "else"  
    assert correctLines[5] == "{"  
    assert correctLines[6] == "a = 5;"  
    assert correctLines[7] == "}"  

def test_if_statement_space():
    correctLines = lineTrim("""if(          a         ==  14){
                                   a      = a    + 7  ;
                               
                               
                               
                               }else{
                                   a   
                                   = 5;
                               }""")

    assert correctLines[0] == "if ((a == 14))"
    assert correctLines[1] == "{"
    assert correctLines[2] == "a = (a + 7);"
    assert correctLines[3] == "}"
    assert correctLines[4] == "else"  
    assert correctLines[5] == "{"  
    assert correctLines[6] == "a = 5;"  
    assert correctLines[7] == "}" 