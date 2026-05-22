from parser.parser import Parser
from lexer.lexer import Lexer

def lineTrimProgram(source):
    lex = Lexer(source)
    lex.lexer()
    node = Parser(lex.tokens).parse()
    correctLines = []
    program = node.to_c()
    lines = program.split("\n")
    for line in lines:
        if line.strip() != "":
            correctLines.append(line.strip())
    return correctLines

def test_small_program():
    correctLines = lineTrimProgram("""void main(){
                            integer x = 5;
                            return;}""")
    assert correctLines == [
        "#include <stdlib.h>",
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#define sametypeof(x, y) _Generic((x),typeof((y) + 0): 1, default: 0)",
        "void main() {",
        "int x = 5;",
        "return;",
        "}"
    ]


def test_big_program():
    correctLines = lineTrimProgram("""
                                    void main(){
                                        string text = "This is a test";
                                        print(text);
                                        integer a = 8;
                                        while(5 < a){
                                            add(5,a);
                                    }
                                    return;
                                    }
                                    integer add (integer a, double b){
                                        a = a + 5;
                                        b = 8.2 * 2 + b;
                                        return a + b;}""")
    
    assert correctLines == [
        "#include <stdlib.h>",
        "#include <stdio.h>",
        "#include <stdbool.h>",
        "#define sametypeof(x, y) _Generic((x),typeof((y) + 0): 1, default: 0)",
        "int add(int a,double b);",        
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
        """}""",
        ";",
        "int a = 8;",
        "while ((5 < a))",
        "{",
        "add(5,a);",
        "}",
        "return;",
        "}",
        "int add(int a,double b) {",
        "a = (a + 5);",
        "b = ((8.2 * 2) + b);",
        "return (a + b);",
        "}"
    ]