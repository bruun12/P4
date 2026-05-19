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
  
    """
    checker = TypeChecker(source)
    checker.check(ast)

    if checker.errors:
        for err in checker.formatted_errors():
            print(err, file=sys.stderr)
        return sys.exit(ErrorCode.TYPECHECKER_ERROR)
    """
    
    return ast.to_c()


def main():  
    if len(sys.argv) >= 2: #sys.argv = ["main.py", "program.cimple", "output.c"]
        with open(sys.argv[1], "r", encoding="utf-8") as file: # read the file
            source = file.read()

        if source is None:
            print("source is empty")
            return sys.exit(ErrorCode.EMPTY_SOURCE_ERROR)
    else:
        print("no input provided")
        return  sys.exit(ErrorCode.ARGUMENT_ERROR)

    try:  
        c_code = interprete_source(source)

        if c_code is None:
            return sys.exit(ErrorCode.EMPTY_SOURCE_ERROR)

        if len(sys.argv) >= 3:
            with open(sys.argv[2], "w", encoding="utf-8") as file:
                file.write(c_code)


        # current working directory (src) 
        cwd_path = os.path.join(os.path.dirname(__file__), "")

    
        cToExecutable = subprocess.run(
            ["gcc", sys.argv[2], "-o", "output"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path
        )

        if cToExecutable.returncode != 0:
            return cToExecutable
        
        executeC = subprocess.run(
            ["./output"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd_path
        )

        print(executeC.stdout, file=sys.stdout)

        return sys.exit(0)

    except LexerError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        return sys.exit(ErrorCode.LEXER_ERROR)

    except ParserError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        return sys.exit(ErrorCode.PARSER_ERROR)
    




if __name__ == "__main__":
    main()