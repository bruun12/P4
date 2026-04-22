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

def parse_program(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    return p.parse()

def test_parser_program_with_one_function():
    prog = parse_program("""
                integer main(){
                string hi = "Hello world";
                return 0;
                }
                 """)
    assert len(prog.functions) == 1
    assert prog.functions[0].name == "main"
    assert prog.functions[0].statement.statements[0].name == "hi"
    assert prog.functions[0].statement.statements[1].value.value == 0

def test_parser_program_with_two_functions():
    prog = parse_program("""
                string say_hi(boolean x){
                    string s = "";
                    if (x){
                        s = "Hello world";
                    } else {
                        s = "hi";      
                    }
                    return s;
                }

                integer main(){
                string hi = "Hello world";
                return 0;
                }            
                    """)
    assert len(prog.functions) == 2
    assert prog.functions[0].name == "say_hi"
    assert prog.functions[0].statement.statements[0].name == "s"
    assert prog.functions[0].statement.statements[2].value.name == "s"

    assert prog.functions[1].name == "main"
    assert prog.functions[1].statement.statements[0].name == "hi"
    assert prog.functions[1].statement.statements[1].value.value == 0

def test_parser_program_with_three_functions():
    prog = parse_program("""
                boolean var_is_true(boolean x, double y){
                    boolean b = false;
                    if (x AND y > 1.5){
                        b = true;     
                    }
                    return b;
                }         

                string say_hi(boolean x){
                    string s = "";
                    if (var_is_true(x, 2.99)){
                        s = "Hello world";
                    } else {
                        s = "hi";      
                    }
                    return s;
                }
                         
                integer main(){
                    string hi = say_hi(true);
                    return 0;
                }   
                """)
    assert len(prog.functions) == 3
    assert prog.functions[0].name == "var_is_true"
    assert prog.functions[0].statement.statements[0].name == "b"
    assert prog.functions[0].statement.statements[2].value.name == "b"

    assert prog.functions[1].name == "say_hi"
    assert prog.functions[1].statement.statements[0].name == "s"
    assert prog.functions[1].statement.statements[2].value.name == "s"

    assert prog.functions[2].name == "main"
    assert prog.functions[2].statement.statements[0].name == "hi"
    assert prog.functions[2].statement.statements[1].value.value == 0