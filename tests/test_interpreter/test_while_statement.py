from parser.parser import Parser
from lexer.lexer import Lexer
from parser.ASTNodes import WhileStatement
from tests.test_interpreter.test_line_trim import lineTrim

def test_while_statement():
    correctLines = lineTrim("""
                while(true)
                {x = 4;}""")

    assert correctLines[0] == "while (true)"
    assert correctLines[1] == "{"
    assert correctLines[2] == "x = 4;"
    assert correctLines[3] == "}"

def test_while_statement2():
    correctLines = lineTrim("""
                while(true AND !false){
                if(a<b){
                    integer x = 8;
                }else{
                a = a + b;
                }
                x = 4;}""")

    assert correctLines[0] == "while ((true && !false))"
    assert correctLines[1] == "{"
    assert correctLines[2] == "if ((a < b))"
    assert correctLines[3] == "{"
    assert correctLines[4] == "int x = 8;"
    assert correctLines[5] == "}"
    assert correctLines[6] == "else"
    assert correctLines[7] == "{"
    assert correctLines[8] == "a = (a + b);"
    assert correctLines[9] == "}"
    assert correctLines[10] == "x = 4;"
    assert correctLines[11] == "}"

def test_while_statement3():
    correctLines = lineTrim("""
                while(true
                
                 AND         !
                
                
                false      )
                
                
                {
                if    (   
                a       <b){
                    integer   x 
                =
                
                 8;
                }       else{
                a = a + b;  


                           }
                x 
                 = 4
                ;}""")

    assert correctLines[0] == "while ((true && !false))"
    assert correctLines[1] == "{"
    assert correctLines[2] == "if ((a < b))"
    assert correctLines[3] == "{"
    assert correctLines[4] == "int x = 8;"
    assert correctLines[5] == "}"
    assert correctLines[6] == "else"
    assert correctLines[7] == "{"
    assert correctLines[8] == "a = (a + b);"
    assert correctLines[9] == "}"
    assert correctLines[10] == "x = 4;"
    assert correctLines[11] == "}"

