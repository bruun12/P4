from parser.ASTNodes import VarDeclaration, Literal, Program, Function, Parameter, BlockStatement, ReturnStatement, Binary, Variable
from error_handling import ErrorCode
from type_checker.TypeChecker import TypeChecker, TypeEnvironment, INTEGER, VOID, ERROR
from lexer.lexer import Lexer
from parser.parser import Parser
import pytest

def build_ast(program: str) -> Program:
    lexer = Lexer(program)
    lexer.lexer()
    
    parser = Parser(lexer.tokens)
    return parser.parse()

def test_nested_block_statements_variable_declaration():

    program = """
        integer function(integer b, integer c){
            integer d = 5;
            if(d <= 6){
                d = 6;
                b = 5;
                if(d <= 7){
                    string d = "hello world";
                    boolean c = true;
                    if(d == "hello world"){
                        integer d = 1; 
                    }
                }
            }
            return 1;
        }
    """
    ast = build_ast(program)
    checker = TypeChecker(program)
    checker.check(ast)
    assert checker.errors == []
    
def invalid_type_comparison():
    program = """
        if(true == 1){
            print("something");
        }
    """
    ast = build_ast(program)
    checker = TypeChecker(program)
    checker.check(ast)
    assert any(err.error_code == ErrorCode.TYPE_MISMATCH_ERROR for err in checker.errors)
    assert checker.errors != []
    
def test_enforced_scoping_rules():

    program = """
        integer function(){
            integer d = 5;
            if(d <= 6){
                d = 6;
                if(d <= 7){
                    string d = "hello world";
                    if(d == "hello world"){
                        integer d = 1; 
                    }
                }
            }
            return d + 1;
        }
    """
    ast = build_ast(program)
    checker = TypeChecker(program)
    checker.check(ast)
    assert checker.errors == []
