from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.TypeChecker import TypeChecker
from error_handling import LexerError, ParserError, format_compiler_error

source_code = """
integer add(integer a, integer b) {
    return a + b;
}

double average(integer a, integer b) {
    return (a + b) / 2.0;
}

boolean is_positive(integer x) {
    return x > 0;
}

integer main() {
    integer x = add(3, 4);
    double y = average(x, 10);
    boolean ok = is_positive(x);

    integer nums[3] = [1, 2, 3];
    integer more[5];
    string words[3] = ["a", "b", "c"];

    nums[1] = add(x, 1);
    more[4] = nums[1];
    print("x = : ", x);

    x = nums[0];
    y = average(add(1, 2), 8);

    if (is_positive(x)){
        x = 2;
    } else {
        x = 5;
    }

    while (x < 20 AND x < 21) {
        x = add(x, 1);
    }

    words[1] = "updated";
    ok = is_positive(nums[1]);

    return x;
}
"""
source_code1 = """
integer decide(integer a, integer b){
    if (a > b){
        return a;
    } else {
        return b;
    }
    return 1;
}

integer main() {
    integer c = decide(1,2);

    return c;
}
"""


def main():
    source = source_code1
    try:
        # ----------------------------------------------------
        # LEXING
        # ----------------------------------------------------
        lexer = Lexer(source)
        lexer.lexer()

        # If your lexer stores errors instead of raising them
        if hasattr(lexer, "errors") and lexer.errors:
            for err in lexer.errors:
                print(format_compiler_error(err, source.splitlines()))
            return

        # ----------------------------------------------------
        # PARSING
        # ----------------------------------------------------
        parser = Parser(lexer.tokens)
        program = parser.parse()

        print("Parsing succeeded.\n")

        # ----------------------------------------------------
        # TYPE CHECKING
        # ----------------------------------------------------
        checker = TypeChecker(source)
        checker.check(program)

        if checker.errors:
            print("Type check failed:\n")
            for err in checker.formatted_errors():
                print(err)
                print()
        else:
            print("Type check passed.")

    except LexerError as err:
        print(format_compiler_error(err, source.splitlines()))

    except ParserError as err:
        print(format_compiler_error(err, source.splitlines()))


if __name__ == "__main__":
    main()