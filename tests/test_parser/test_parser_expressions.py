import pytest
from error_handling import ParserError
from lexer.lexer import Lexer
from parser.ASTNodes import (
    Binary,
    Literal,
    Unary,
    Variable,
    ArrayAccess,
)
from parser.parser import Parser

# Helper function 
def parse_expr(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    expr = p.parse_expression()
    
    return expr


# Empty / missing expressions
###############################################################################################

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
###############################################################################################

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
###############################################################################################

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
###############################################################################################

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

# Primary
###############################################################################################
def test_expression_integer_literal():
    node = parse_expr("42")

    assert isinstance(node, Literal)
    assert node.value == 42

def test_expression_float_literal():
    node = parse_expr("42.11")

    assert isinstance(node, Literal)
    assert node.value == 42.11

def test_expression_true_literal():
    node = parse_expr("true")

    assert isinstance(node, Literal)
    assert node.value

def test_expression_false_literal():
    node = parse_expr("false")

    assert isinstance(node, Literal)
    assert node.value == False

def test_expression_string_literal():
    node = parse_expr('"Hello";')

    assert isinstance(node, Literal)
    assert node.value == "Hello"

def test_expression_identifier():
    node = parse_expr("x")

    assert isinstance(node, Variable)
    assert node.name == "x"

def test_expression_None():
    lex = Lexer("return;")
    lex.lexer()
    node = Parser(lex.tokens).statement()

    assert node.value is None

# Unary
###################################################################################################

def test_expression_unary_not():
    node = parse_expr("!true;")

    assert isinstance(node, Unary)
    assert node.operator == "!"
    assert isinstance(node.right, Literal)
    assert node.right.value is True

def test_expression_unary_minus():
    node = parse_expr("-5;")

    assert isinstance(node, Unary)
    assert node.operator == "-"
    assert isinstance(node.right, Literal)
    assert node.right.value


#Multiplicative, Division and Modulo
######################################################################################################

def test_expression_multiplicative():
    node = parse_expr("x * 2;")

    assert isinstance(node, Binary)
    assert node.operator == "*"
    assert isinstance(node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 2

def test_expression_division():
    node = parse_expr("x / 2;")

    assert isinstance(node, Binary)
    assert node.operator == "/"

def test_expression_modulo():
    node = parse_expr(" x MOD 2;")

    assert isinstance(node, Binary)
    assert node.operator == "MOD"

# Additive
########################################################################################################

def test_expression_addition():
    node = parse_expr("x + 2;")

    assert isinstance(node, Binary)
    assert node.operator == "+"
    assert isinstance(node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 2

def test_expression_subtration():
    node = parse_expr("x - 2;")

    assert isinstance(node, Binary)
    assert node.operator == "-"
    assert isinstance(node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 2

# Comparison
#############################################################################################################

def test_expression_less_than(): 
    node = parse_expr("x < 10")

    assert isinstance(node, Binary)
    assert node.operator == "<"
    assert isinstance(node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 10

def test_expression_less_than_or_equal():
    node = parse_expr("x <= 10")

    assert isinstance(node, Binary)
    assert node.operator == "<="
    assert isinstance (node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 10

def test_expression_greater_than():
    node = parse_expr("x > 10")

    assert isinstance(node, Binary)
    assert node.operator == ">"
    assert isinstance(node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 10

def test_expression_greater_than_or_equal():
    node = parse_expr("x >= 10")

    assert isinstance(node, Binary)
    assert node.operator == ">="
    assert isinstance (node.left, Variable)
    assert node.left.name == "x"
    assert isinstance(node.right, Literal)
    assert node.right.value == 10

# Equality
##########################################################################################################

def test_expression_equals():
    node = parse_expr("x == 5")

    assert isinstance(node, Binary)
    assert node.operator == "=="
    assert isinstance(node.right, Literal)
    assert node.right.value == 5

def test_expression_not_equals():
    node = parse_expr("x != 5")

    assert isinstance(node, Binary)
    assert node.operator == "!="

# AND / OR 
##################################################################################################################

def test_expression_and():
    node = parse_expr("x == 1 AND y == 2")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)   
    assert isinstance(node.right, Binary)  

def test_expression_or():
    node = parse_expr("x == 1 OR y == 2")

    assert isinstance(node, Binary)
    assert node.operator == "OR"

def test_expression_and_before_than_or():
    # x OR y AND z  bør parses som  x OR (y AND z)
    node = parse_expr("x == 1 OR y == 2 AND z == 3")

    assert node.operator == "OR"           
    assert node.right.operator == "AND"    

#Precedence
#############################################################################################################

def test_expression_precedence_mul_over_add():
    node = parse_expr(" x + y * 2;")

    assert node.operator == "+"
    assert node.right.operator == "*"

def test_expression_precedence_min_over_add():
    node = parse_expr("x - y + 2;")
    
    assert node.operator == "+"
    assert node.left.operator == "-"

#Chaining
#############################################################################################################

def test_chaining_less_than():
    node = parse_expr("2 < 10 < 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == "<"
    assert node.left.left.value == 2
    assert node.left.right.value == 10
    assert isinstance(node.right, Binary)
    assert node.right.operator == "<"
    assert node.right.left.value == 10
    assert node.right.right.value == 9

def test_chaining_greater_than():
    node = parse_expr("2 > 10 > 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == ">"
    assert isinstance(node.right, Binary)
    assert node.right.operator == ">"

def test_chaining_less_great():
    node = parse_expr("2 < 10 > 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == "<"
    assert isinstance(node.right, Binary)
    assert node.right.operator == ">"

def test_chaining_great_less():
    node = parse_expr("2 > 10 < 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == ">"
    assert isinstance(node.right, Binary)
    assert node.right.operator == "<"

def test_chaining_leq():
    node = parse_expr("2 <= 10 <= 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == "<="
    assert isinstance(node.right, Binary)
    assert node.right.operator == "<="

def test_chaining_geq():
    node = parse_expr("2 >= 10 >= 9")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == ">="
    assert isinstance(node.right, Binary)
    assert node.right.operator == ">="

def test_chaining_four():
    node = parse_expr("2 < 10 < 9 < 8")

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == "AND"
    assert isinstance(node.right, Binary)
    assert node.right.operator == "<"
    assert node.left.left.operator == "<"
    assert node.left.right.operator == "<"

def test_chaining_five():
    # 2 < 10 AND 10 < 9 AND 9 < 8 AND 8 < 7
    node = parse_expr("2 < 10 < 9 < 8 < 7")
    print(node)

    assert isinstance(node, Binary)
    assert node.operator == "AND"
    assert isinstance(node.left, Binary)
    assert node.left.operator == "AND"
    assert isinstance(node.left.left, Binary)
    assert node.left.left.operator == "AND"
    assert isinstance(node.left.right, Binary)
    assert node.left.right.operator == "<"
    assert isinstance(node.left.left.left, Binary)
    assert node.left.left.left.operator == "<"
    assert isinstance(node.left.left.right, Binary)
    assert node.left.left.right.operator == "<"
    assert isinstance(node.right, Binary)
    assert node.right.operator == "<"


#ArrayAccess
###########################################################################################################

def test_array_access_integer_index():
    node = parse_expr("a[3]")

    assert isinstance(node, ArrayAccess)
    assert node.name == "a"
    assert isinstance(node.offset, Literal)
    assert node.offset.value == 3

def test_array_access_variable_index():
    node = parse_expr("a[i]")

    assert isinstance(node, ArrayAccess)
    assert node.name == "a"
    assert isinstance(node.offset, Variable)
    assert node.offset.name == "i"

def test_array_access_expression_index():
    node = parse_expr("a[i + 1]")

    assert isinstance(node, ArrayAccess)
    assert isinstance(node.offset, Binary)
    assert node.offset.operator == "+"

def test_array_access_to_c():
    node = parse_expr("a[3]")

    assert node.to_c() == "a[3]"

# Errors
def test_array_access_missing_index_raises():
    with pytest.raises(ParserError):
        parse_expr("a[]")

def test_array_access_missing_rbrace_raises():
    with pytest.raises(ParserError):
        parse_expr("a[3")