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
        """if (sametypeof(1.2,"Hello World!")){""",
        """printf("%f","Hello World!");""",
        """} else if (sizeof("Hello World!") == 1) {""",
        """printf("%s", "Hello World!" ? "true" : "false");""",
        """} else if (sametypeof(1, "Hello World!")){""",
        """printf("%d", "Hello World!");""",
        """} else if (sametypeof("string","Hello World!")){""",
        """printf("%s","Hello World!");""",
        "}",
        ";",
        """if (sametypeof(1.2,"I am learning Cimple.")){""",
        """printf("%f","I am learning Cimple.");""",
        """} else if (sizeof("I am learning Cimple.") == 1) {""",
        """printf("%s", "I am learning Cimple." ? "true" : "false");""",
        """} else if (sametypeof(1, "I am learning Cimple.")){""",
        """printf("%d", "I am learning Cimple.");""",
        """} else if (sametypeof("string","I am learning Cimple.")){""",
        """printf("%s","I am learning Cimple.");""",
        "}",
        ";",
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
        "int add(int a,double b) {",
            "a = (a + 5);",
            "b = ((8.2 * 2) + b);",
            "return (a + b);",
            "}",         
            "void main() {",
            """char* text = "This is a test";""",
            """if (sametypeof(1.2,text)){""",
            """printf("%f",text);""",
            """} else if (sizeof(text) == 1) {""",
            """printf("%s", text ? "true" : "false");""",
            """} else if (sametypeof(1, text)){""",
            """printf("%d", text);""",
            """} else if (sametypeof("string",text)){""",
            """printf("%s",text);""",
            "}",
            ";",
            "int a = 8;",
            "while ((5 < a))",
            "{",
            "add(5,a);",
            "}",
            "return;",
            "}"
    ]
