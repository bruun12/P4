from lexer.lexer import Lexer
from parser.parser import Parser
import sys
import subprocess

def run_c_code():
    res = subprocess.run(["gcc", "output.c"], capture_output=True, text=True)
    print("Output:", res.stdout)
    print("Return Code:", res.returncode)

def compile_source(source: str) -> str:
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    ast = p.parse()
    return ast.to_c()

# For at køre skal du være i src mappen (cd src), herefter "python main.py program.mit output.c"
def main():
    print("Program starter...")
    if len(sys.argv) >= 2: #sys.argv = ["main.py", "program.mit", "output.c"]
        with open(sys.argv[1], "r", encoding="utf-8") as file: # r står for read i python
            source = file.read()
    else:
        source = """
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

    c_code = compile_source(source)
    

        
    if len(sys.argv) >= 3:
            with open(sys.argv[2], "w", encoding="utf-8") as file:
                file.write(c_code)
            print (f"Compiled -> {sys.argv[2]}")
            print(f"C kode:\n{c_code}")
    else: 
            print(c_code)

if __name__ == "__main__":
            main()

    

