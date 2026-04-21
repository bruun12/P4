import pytest

from lexer.lexer import Lexer
from error_handling import ParserError
from parser.parser import Parser
from parser.ASTNodes import BlockStatement

def parse_function(source: str):
    lex = Lexer(source)
    lex.lexer()
    p = Parser(lex.tokens)
    return p.function()

def test_function_main():
    func = parse_function(""" 
                integer main(){
                string hi = "Hello world";
                return 0;
                }""")
    body = func.statement 
    assert func.return_type == "integer"
    assert func.name == "main"
    assert len(func.parameters) == 0
    assert isinstance(body, BlockStatement)

def test_function_say_hi():
    func = parse_function(""" 
                string say_hi(boolean x){
                    string s = "";
                    if (x){
                        s = "Hello world";
                    } else {
                        s = "hi";      
                    }
                    return s;
                }""")
    body = func.statement 
    assert func.return_type == "string"
    assert func.name == "say_hi"
    assert len(func.parameters) == 1
    assert func.parameters[0].type == "boolean"
    assert func.parameters[0].name == "x"
    assert isinstance(body, BlockStatement)

def test_function_syntax_error_in_func_declaration():
    with pytest.raises(ParserError):
        parse_function(""" 
                        string say_hi(boolean x)){
                            if (x){
                                return "Hello world";
                            } else {
                                return "hi";      
                            }
                                
                        }""")


def test_function_syntax_error_in_body():
    with pytest.raises(ParserError):
        parse_function(""" 
                        string say_hi(boolean x){
                            if (boolean x){
                                return "Hello world";
                            } else {
                                return "hi";      
                            }
                                
                        }""")