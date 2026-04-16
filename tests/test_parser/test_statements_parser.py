from lexer.lexer import Lexer
from parser.ASTNodes import ParserError
from parser.parser import Parser

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
                {x = 4;}
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


# Lav hvor du forventer errors
# 