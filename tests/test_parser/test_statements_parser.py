from lexer.lexer import Lexer
from error_handling import ParserError
from parser.parser import Parser
import pytest

def test_statements_if_and_blockStatement_match():
    lex = Lexer(""" 
                {
                if (true)
                {x = 4;} else {
                x = 3;}
                }""")
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

def test_statements_while_match():
    lex = Lexer("""
                {
                while(true)
                {x = 4;
                if(true){y=3;}
                y =5;}
                }""")
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

def test_statements_return_match(): 
    lex = Lexer("""
                return x +2;
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

def test_statements_assign_match():
    lex = Lexer("""
                x = 2;
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

def test_statements_var_declaration():
    lex = Lexer("""
                integer x = 2; 
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

def test_statements_expression():
    lex = Lexer("""
                "Wallah"; 
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    parser.statement()

# Array declaration
def test_statements_array_declaration_with_values():
    lex = Lexer("""
                integer arr = [1,2,3];
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    node = parser.statement()
    assert node.type == "integer"
    assert node.name == "arr"
    assert node.size == 3

def test_statements_array_declaration_empty():
    lex = Lexer("""
                double arr[3];
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    node = parser.statement()
    assert node.type == "double"
    assert node.name == "arr"
    assert node.size == 3


def test_statements_array_declaration_single_element():
    lex = Lexer("""
                integer arr = [1];
                """)
    lex.lexer()
    parser = Parser(lex.tokens)
    node = parser.statement()
    assert node.type == "integer"
    assert node.name == "arr"
    assert node.size == 1

# Errors for statements
def parse_stmt(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    statements = p.statement()
    return statements

# Var declaration
def test_var_decl_missing_assign():
    with pytest.raises(ParserError):
        parse_stmt("integer x")

def test_var_decl_missing_semicolon():
    with pytest.raises(ParserError):
        parse_stmt("integer m = 1")

# Block statement
def test_block_statement_missing_closing_brace():
    with pytest.raises(ParserError):
        parse_stmt("{integer m = 1;")

# While statement
def test_while_missing_lparen():
    with pytest.raises(ParserError):
        parse_stmt("while x < 3){}")

def test_while_missing_rparen():
    with pytest.raises(ParserError):
        parse_stmt("while (x > {}")

def test_while_missing_lcbrace():
    with pytest.raises(ParserError):
        parse_stmt("while (x <3)")

# Assign statement
def test_assign_missing_assign_operator():
    with pytest.raises(ParserError):
        parse_stmt("x 5;")

def test_assign_missing_semicolon():
    with pytest.raises(ParserError):
        parse_stmt("x = 5")

# IF statement 
def test_if_missing_lparen():
    with pytest.raises(ParserError):
        parse_stmt("if x<3){}")

def test_if_missing_rparen():
    with pytest.raises(ParserError):
        parse_stmt("if (x<3 {}")

def test_if_missing_lcbrace():
    with pytest.raises(ParserError):
        parse_stmt("if (x<3)")

def test_if_else_missing_lcbrace():
    with pytest.raises(ParserError):
        parse_stmt("if (x > 0) {} else integer y = 1;")

# Return
def test_return_missing_semicolon():
    with pytest.raises(ParserError):
        parse_stmt("return x + 2")

# Errors for array declaration
def test_array_declaration_missing_semicolon():
    with pytest.raises(ParserError):
        parse_stmt("integer arr = [1,2,3]")

def test_array_declaration_missing_closing_bracket():
    with pytest.raises(ParserError):
        parse_stmt("integer arr = [1,2,3;")

def test_array_declaration_empty_missing_closing_bracket():
    with pytest.raises(ParserError):
        parse_stmt("integer arr[3;")

def test_array_declaration_empty_missing_semicolon():
    with pytest.raises(ParserError):
        parse_stmt("integer arr[3]")