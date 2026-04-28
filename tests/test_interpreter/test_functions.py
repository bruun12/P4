from lexer.lexer import Lexer
from parser.parser import Parser

def lineTrimFunction(lexerString: str):
    lex = Lexer(lexerString)
    lex.lexer()
    node = Parser(lex.tokens).parse()
    correctLines2 = []
    for func in node.functions:
        lines = func.to_c().split("\n")
        for line in lines:
            if line.strip() != "":
                correctLines2.append(line.strip())
    return correctLines2

def test_function_to_c():
    result = lineTrimFunction("integer foobar(integer x, integer y) { return x; }")
    assert result == ["integer foobar(int x,int y) {", "return x;", "}"]

def test_two_functions_to_c():
    result = lineTrimFunction(
        "integer foobar(integer x) { return x; } "
        "integer piphans(integer y) { return y; }"
    )
    assert result == [
        "integer foobar(int x) {",
        "return x;",
        "}",
        "integer piphans(int y) {",
        "return y;",
        "}"
    ]

def test_three_functions_to_c():
    result = lineTrimFunction(
        "integer foobar(integer x) { return x; } "
        "integer piphans(integer y) { return y; } "
        "integer wallah(integer z) { return z; }"
    )
    assert result == [
        "integer foobar(int x) {",
        "return x;",
        "}",
        "integer piphans(int y) {",
        "return y;",
        "}",
        "integer wallah(int z) {",
        "return z;",
        "}"
    ]