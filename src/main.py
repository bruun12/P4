from lexer.lexer import Lexer
from parser.parser import Parser

string = """
integer main(){
    integer a = 1 + 2 * 5;
    string b = "Peter kan godt lide tis";
    double c = (9.9+7);
    double d = -5;
    if (d < 500){
        a = 1; b = "øv";
    } else {
        a = 999;
        b = a;
    }
    return 0;
}
"""
lex = Lexer(string)

lex.lexer()

p = Parser(lex.tokens)

# Print AST tree
print("\nAST Tree:")
print(p.parse())

