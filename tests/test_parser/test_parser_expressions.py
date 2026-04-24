import pytest
from error_handling import ParserError
from lexer.lexer import Lexer
from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    Expression,
    ExpressionStatement,
    IfStatement,
    Literal,
    Node,
    Program,
    ReturnStatement,
    Statement,
    Unary,
    Variable,
    WhileStatement,
    VarDeclaration,
)
from parser.parser import Parser
from error_handling import ParserError

# Helper function - Har ændret i denne, ved ikke om vores parser skal bruges til at tjekke efter for mange tokens
def parse_expr(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    expr = p.parse_expression()
    
    return expr

# Lav hvor vi ikke forventer errors

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

def test_expr():
    print(parse_expr("2").value)
    print("test")

# Expression, is it working?

# Primary
###############################################################################################
def test_expression_integer_literal():
    lex = Lexer("return 42;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Literal)
    assert node.value.value == 42

def test_expression_float_literal():
    lex = Lexer("return 42.11;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Literal)
    assert node.value.value == 42.11

def test_expression_true_literal():
    lex = Lexer("return true;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Literal)
    assert node.value.value

def test_expression_false_literal():
    lex = Lexer("return false;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Literal)
    assert node.value.value == False

def test_expression_string_literal():
    lex = Lexer('return "Hello";')
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Literal)
    assert node.value.value

def test_expression_identifier():
    lex = Lexer("return x;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Variable)
    assert node.value.name == "x"

# Unary
###################################################################################################

def test_expression_unary_not():
    lex = Lexer("return !true;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Unary)
    assert node.value.operator == "!"
    assert isinstance(node.value.right, Literal)
    assert node.value.right.value

def test_expression_unary_minus():
    lex = Lexer("return -5;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Unary)
    assert node.value.operator == "-"
    assert isinstance(node.value.right, Literal)
    assert node.value.right.value


#Multiplicative
######################################################################################################

def test_expression_multiplicative():
    lex = Lexer("return x * 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, ReturnStatement)
    assert isinstance(node.value, Binary)
    assert node.value.operator == "*"
    assert isinstance(node.value.left, Variable)
    assert node.value.left.name == "x"
    assert isinstance(node.value.right, Literal)
    assert node.value.right.value == 2

def test_expression_division():
    lex = Lexer("return x / 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.value, Binary)
    assert node.value.operator == "/"

def test_expression_modulo():
    lex = Lexer("return x MOD 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.value, Binary)
    assert node.value.operator == "MOD"

# Additive
########################################################################################################

def test_expression_addition():
    lex = Lexer("return x + 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.value, Binary)
    assert node.value.operator == "+"
    assert isinstance(node.value.left, Variable)
    assert node.value.left.name == "x"
    assert isinstance(node.value.right, Literal)
    assert node.value.right.value == 2

def test_expression_subtration():
    lex = Lexer("return x - 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.value, Binary)
    assert node.value.operator == "-"
    assert isinstance(node.value.left, Variable)
    assert node.value.left.name == "x"
    assert isinstance(node.value.right, Literal)
    assert node.value.right.value == 2

# Comparison
#############################################################################################################

def test_expression_less_than(): 
    lex = Lexer("if (x < 10) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, IfStatement)
    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "<"
    assert isinstance(node.condition.left, Variable)
    assert node.condition.left.name == "x"
    assert isinstance(node.condition.right, Literal)
    assert node.condition.right.value == 10

def test_expression_less_than_or_equal():
    lex = Lexer("if (x <= 10) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, IfStatement)
    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "<="
    assert isinstance (node.condition.left, Variable)
    assert node.condition.left.name == "x"
    assert isinstance(node.condition.right, Literal)
    assert node.condition.right.value == 10

def test_expression_greater_than():
    lex = Lexer("if (x > 10) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, IfStatement)
    assert isinstance(node.condition, Binary)
    assert node.condition.operator == ">"
    assert isinstance(node.condition.left, Variable)
    assert node.condition.left.name == "x"
    assert isinstance(node.condition.right, Literal)
    assert node.condition.right.value == 10

def test_expression_greater_than_or_equal():
    lex = Lexer("if (x >= 10) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node, IfStatement)
    assert isinstance(node.condition, Binary)
    assert node.condition.operator == ">="
    assert isinstance (node.condition.left, Variable)
    assert node.condition.left.name == "x"
    assert isinstance(node.condition.right, Literal)
    assert node.condition.right.value == 10

# Equality
##########################################################################################################

def test_expression_equals():
    lex = Lexer("if (x == 5) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "=="
    assert isinstance(node.condition.right, Literal)
    assert node.condition.right.value == 5

def test_expression_not_equals():
    lex = Lexer("if (x != 5) { y = 1; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "!="

# AND / OR 
##################################################################################################################

def test_expression_and():
    lex = Lexer("if (x == 1 AND y == 2) { z = 0; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "AND"
    assert isinstance(node.condition.left, Binary)   
    assert isinstance(node.condition.right, Binary)  

def test_expression_or():
    lex = Lexer("if (x == 1 OR y == 2) { z = 0; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert isinstance(node.condition, Binary)
    assert node.condition.operator == "OR"

def test_expression_and_before_than_or():
    # x OR y AND z  bør parses som  x OR (y AND z)
    lex = Lexer("if (x == 1 OR y == 2 AND z == 3) { w = 0; }")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert node.condition.operator == "OR"           
    assert node.condition.right.operator == "AND"    

#Precedence
#############################################################################################################

def test_expression_precedence_mul_over_add():
    lex = Lexer("return x + y * 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert node.value.operator == "+"
    assert node.value.right.operator == "*"

def test_expression_precedence_min_over_add():
    lex = Lexer("return x - y + 2;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert node.value.operator == "+"
    assert node.value.left.operator == "-"