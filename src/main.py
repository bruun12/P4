import sys
from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.TypeChecker import TypeChecker
from error_handling import LexerError, ParserError, format_compiler_error

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
    if len(sys.argv) >= 2: #sys.argv = ["main.py", "program.cimple", "output.c"]
        with open(sys.argv[1], "r", encoding="utf-8") as file: # r står for read i python
            source = file.read()

        if source is None:
            print("source is empty")
            return 1
    else:
        return "no input provided"

    try:  
        c_code = interprete_source(source)

        if c_code is None:
            return sys.exit(1)

        if len(sys.argv) >= 3:
            with open(sys.argv[2], "w", encoding="utf-8") as file:
                file.write(c_code)
    

    except LexerError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        return sys.exit(1)

    except ParserError as err:
        print(format_compiler_error(err, source.splitlines()), file=sys.stderr)
        return sys.exit(1)
    




if __name__ == "__main__":
    main()