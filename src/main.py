import sys
import os
import subprocess
from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.TypeChecker import TypeChecker
from error_handling import LexerError, ParserError, format_compiler_error, ErrorCode

def interprete_source(source: str) -> str:
    lexer = Lexer(source)
    lexer.lexer()
    
    parser = Parser(lexer.tokens)
    ast = parser.parse()
  
    checker = TypeChecker(source)
    checker.check(ast)

    if checker.errors:
        for err in checker.formatted_errors():
            print(err, file=sys.stderr)
        return None
    
    return ast.to_c()


def main():  
    if "--help" in sys.argv:
        print("""
OBS: This program require that have gcc avaiable in this folder
              
Usage: cimple CIMPLEFILE EXECUTABLE [Optionals]
              
Optionals:
    -r      Runs the program once it has compiled
    -k      Keeps the transpiled c-file followed by c-file exmaple: -k output.c
              
Example:
cimple cimple.cimple exec -r -k exec.c
""", file=sys.stdout)
        sys.exit(0) 
    
    autoRun = False
    cFileName = None

    if len(sys.argv) >= 3: #sys.argv = ["main.py", "program.cimple", "output"]
        if "-r" in sys.argv[3:]: #update the flags
            autoRun = True
        if "-k" in sys.argv[3:]:
            cFileName = sys.argv[sys.argv.index("-k") + 1]
            if not cFileName.endswith(".c"):
                print("The c file needs to end with .c", file=sys.stderr)
                sys.exit(1)
        
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as file: # read the file
                source = file.read()
        except FileNotFoundError:
            print("No file is found.\n\nTo get help:\ncimple --help", file=sys.stderr)
            sys.exit(1)

        if source is None:
            print("The provided file is empty. Try another file", file=sys.stderr)
            sys.exit(ErrorCode.EMPTY_SOURCE_ERROR.value)
    else:
        print("not the valid arguments. \n\nTo get help:\ncimple --help")
        sys.exit(ErrorCode.ARGUMENT_ERROR.value)

    try:  
        c_code = interprete_source(source)

        #if the program finds typechecker errors
        if c_code is None:
            sys.exit(ErrorCode.TYPECHECKER_ERROR.value)

        with open("output.c" if cFileName is None else cFileName, "w", encoding="utf-8") as file:
            file.write(c_code)


        # current working directory (src) 
        cwd_path = os.path.join(os.path.dirname(__file__), "")

    
        cToExecutable = subprocess.run(
            ["gcc", "output.c" if cFileName is None else cFileName, "-o", sys.argv[2]],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path
        )

        if cToExecutable.returncode != 0:
            print("This program requies you to have gcc avaiable in this folder", file=sys.stderr)
            sys.exit(cToExecutable.returncode)
        
        # Deletes output.c if name is not specified
        if cFileName is None:
            os.remove("output.c")
        
        # Only execute the program if it is instructed
        if autoRun:
            executeC = subprocess.run(
                [f"./{sys.argv[2]}"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=cwd_path
            )

            print(executeC.stdout, file=sys.stdout)

        return sys.exit(0)

    except LexerError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        sys.exit(ErrorCode.LEXER_ERROR.value)

    except ParserError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        sys.exit(ErrorCode.PARSER_ERROR.value)

if __name__ == "__main__":
    main()