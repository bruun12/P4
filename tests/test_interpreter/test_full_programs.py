from parser.parser import Parser
from lexer.lexer import Lexer
from tests.test_interpreter.test_functions import lineTrimFunction

def test_small_program():
    correctLines = lineTrimFunction("""void main(){
                            integer x = 5;
                            return;}""")
    assert correctLines == [
        "void main() {",
        "int x = 5;",
        "return;",
        "}"
    ]

def test_medium_program():
    correctLines = lineTrimFunction("""void main(){
                            print("Hello World!");
                            print("I am learning Cimple.");
                            return;
                            } """)
    assert correctLines == [
        "void main() {",
        """printf("Hello World!");""",
        """printf("I am learning Cimple.");""",
        "return;",
        "}"
    ]

def test_big_program():
    correctLines = lineTrimFunction("""integer add (integer a, double b){
                                    a = a + 5;
                                    b = 8.2 * 2 + b;
                                    return a + b;}
                                    
                                    void main(){
                                    string text = "This is a test";
                                    print(text);
                                    integer a = 8;
                                    while(5 < a){
                                    add(5,a);
                                    }
                                    return;
                                    }""")
    assert correctLines == [
        "int add(int a,float b) {",
            "a = (a + 5);",
            "b = ((8.2 * 2) + b);",
            "return (a + b);",
            "}",         
            "void main() {",
            """char* text[] = "This is a test";""",
            "printf(text);", 
            "int a = 8;",
            "while ((5 < a))",
            "{",
            "add(5,a);",
            "}",
            "return;",
            "}"
    ]