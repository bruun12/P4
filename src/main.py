from lexer.lexer import Lexer
from parser.parser import Parser
import sys
import subprocess

def run_c_code():
    res = subprocess.run(["gcc", "output.c", "-o", "output", "&&", "./output"], capture_output=True, text=True)
    return res


def compile_source(source: str) -> str:
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    ast = p.parse()
    return ast.to_c()

# For at køre skal du være i src mappen (cd src), herefter "python main.py program.mit output.c"
def main():
    


    if len(sys.argv) >= 2: #sys.argv = ["main.py", "program.cimple", "output.c"]
        with open(sys.argv[1], "r", encoding="utf-8") as file: # r står for read i python
            source = file.read()
    else:
        return "no input provided"

    c_code = compile_source(source)
    
    if len(sys.argv) >= 3:
            with open(sys.argv[2], "w", encoding="utf-8") as file:
                file.write(c_code)

    run_c_code()    


if __name__ == "__main__":
            main()

    

