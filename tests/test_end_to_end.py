from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode

import pytest

def test_valid_program():
    source_code = """
    integer main() {
        integer x = 5;
        print("x = ", x);
        return 0;
    }
    """

    lexer = Lexer(source_code)
    lexer.lexer()

    parser = Parser(lexer.tokens)
    program = parser.parse()

    checker = TypeChecker(source_code)
    checker.check(program)

    assert checker.errors == []

def test_invalid_program():
    source_code = """
    integer main() {
        integer x = "hello";
        return x;
    }
    """

    lexer = Lexer(source_code)
    lexer.lexer()

    parser = Parser(lexer.tokens)
    program = parser.parse()

    checker = TypeChecker(source_code)
    checker.check(program)

    assert any(err.error_code == ErrorCode.CANNOT_ASSIGN for err in checker.errors)