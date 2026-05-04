import sys
import subprocess
from lexer.lexer import Lexer
from parser.parser import Parser


def run_c_code():
    res = subprocess.run(["gcc", "output.c", "-o", "output", "&&", "./output"], capture_output=True, text=True)
    return res

def interprete_source(source: str) -> str {
    lexer = Lexer(source)
    lexer.lexer()
    
    # If your lexer stores errors instead of raising them
    if hasattr(lexer, "errors") and lexer.errors:
        for err in lexer.errors:
            print(format_compiler_error(err, source_code.splitlines()))
        return 
  
    parser = Parser(lexer.tokens)
    program = parser.parse()
  
    
    checker = TypeChecker(source)
    checker.check(program)

    if checker.errors:
        print("Type check failed:\n")
        for err in checker.formatted_errors():
            print(err)    
        return
    
    return program.to_c()
}


def main():
  
  
    if len(sys.argv) >= 2: #sys.argv = ["main.py", "program.cimple", "output.c"]
        with open(sys.argv[1], "r", encoding="utf-8") as file: # r står for read i python
            source = file.read()
    else:
        return "no input provided"
      
      
    try:
      c_code = interprete_source(source)
    
    except LexerError as err:
        print(format_compiler_error(err, source_code.splitlines()))

    except ParserError as err:
        print(format_compiler_error(err, source_code.splitlines()))
        
            
    if len(sys.argv) >= 3:
            with open(sys.argv[2], "w", encoding="utf-8") as file:
                file.write(c_code)


if __name__ == "__main__":
    main()