import pytest

from lexer.lexer import Lexer
from parser.ASTNodes import ParserError
from parser.parser import Parser


# Helper function - Har ændret i denne, ved ikke om vores parser skal bruges til at tjekke efter for mange tokens
def parse_expr(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    expr = p.parse_expression()
    
    return expr


# Empty / missing expressions

def test_empty_expression_raises():
    with pytest.raises(ParserError):
        parse_expr("")

def test_only_plus_raises():
    with pytest.raises(ParserError):
        parse_expr("+")

def test_only_star_raises():
    with pytest.raises(ParserError):
        parse_expr("*")

def test_only_and_raises():
    with pytest.raises(ParserError):
        parse_expr("AND")

def test_only_or_raises():
    with pytest.raises(ParserError):
        parse_expr("OR")


#Missing right operand

def test_missing_right_operand_plus():
    with pytest.raises(ParserError):
        parse_expr("1 + ")

def test_missing_right_operand_minus():
    with pytest.raises(ParserError):
        parse_expr("5 -")

def test_missing_right_operand_star():
    with pytest.raises(ParserError):
        parse_expr("3 *")

def test_missing_right_operand_slash():
    with pytest.raises(ParserError):
        parse_expr("10 /")

def test_missing_right_operand_mod():
    # MOD is a keyword -> TokenType.PERCENT
    with pytest.raises(ParserError):
        parse_expr("7 MOD")

def test_missing_right_operand_and():
    with pytest.raises(ParserError):
        parse_expr("true AND")

def test_missing_right_operand_or():
    with pytest.raises(ParserError):
        parse_expr("false OR")

def test_missing_right_operand_lt():
    with pytest.raises(ParserError):
        parse_expr("x <")

def test_missing_right_operand_le():
    with pytest.raises(ParserError):
        parse_expr("x <=")

def test_missing_right_operand_gt():
    with pytest.raises(ParserError):
        parse_expr("x >")

def test_missing_right_operand_ge():
    with pytest.raises(ParserError):
        parse_expr("x >=")

def test_missing_right_operand_eq():
    with pytest.raises(ParserError):
        parse_expr("x ==")

def test_missing_right_operand_ne():
    with pytest.raises(ParserError):
        parse_expr("x !=")


#Double operator

def test_double_plus_raises():
    with pytest.raises(ParserError):
        parse_expr("1 + + 2")

def test_double_star_raises():
    with pytest.raises(ParserError):
        parse_expr("2 * * 3")

def test_double_lt_raises():
    with pytest.raises(ParserError):
        parse_expr("1 < < 2")

def test_double_eq_raises():
    with pytest.raises(ParserError):
        parse_expr("1 == == 2")

def test_double_and_raises():
    with pytest.raises(ParserError):
        parse_expr("true AND AND false")


#Parenthesis errors

def test_missing_rparen_raises():
    with pytest.raises(ParserError):
        parse_expr("( 42")

def test_empty_parens_raises():
    with pytest.raises(ParserError):
        parse_expr("()")

def test_nested_missing_rparen_raises():
    with pytest.raises(ParserError):
        parse_expr("( ( 1 + 2 )")
