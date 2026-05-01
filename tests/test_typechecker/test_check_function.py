
from lexer.lexer import Lexer
from parser.parser import Parser
from type_checker.TypeChecker import TypeChecker
from parser.ASTNodes import (
    Binary,
    BlockStatement,
    Function,
    Literal,
    Parameter,
    ReturnStatement,
    Variable,
    VarDeclaration,
)

import pytest

source_code_correct = """        
    double average(integer a, integer b) {
    return (a + b) / 2.0;
    }
    """

#average_function_correct = Function(
#    return_type="double",
#    name="average",
#    parameters=[
#        Parameter("integer", "a", line=5, column=15),
#        Parameter("integer", "b", line=5, column=26),
#    ],
#    statement=BlockStatement(
#        statements=[
#            ReturnStatement(
#                value=Binary(
#                    left=Binary(
#                        left=Variable("a", line=6, column=13),
#                        operator="+",
#                        right=Variable("b", line=6, column=17),
#                        line=6,
#                        column=15,
#                    ),
#                    operator="/",
#                    right=Literal(2.0, line=6, column=23),
#                    line=6,
#                    column=20,
#                ),
#                line=6,
#                column=5,
#            )
#        ],
#        line=5,
#        column=37,
#    ),
#    line=5,
#    column=1,
#)
source_code_nested_return = """        
    double average(integer a, integer b) {
    return (a + b) / 2.0;
    integer x = 5;
    }
    """
#average_function_nested_return = Function(
#    return_type="double",
#    name="average",
#    parameters=[
#        Parameter("integer", "a", line=5, column=15),
#        Parameter("integer", "b", line=5, column=26),
#    ],
#    statement=BlockStatement(
#        statements=[
#            ReturnStatement(
#                value=Binary(
#                    left=Binary(
#                        left=Variable("a", line=6, column=13),
#                        operator="+",
#                        right=Variable("b", line=6, column=17),
#                        line=6,
#                        column=15,
#                    ),
#                    operator="/",
#                    right=Literal(2.0, line=6, column=23),
#                    line=6,
#                    column=20,
#                ),
#                line=6,
#                column=5,
#            ),
#            VarDeclaration(
#                    type="integer",
#                    name="x",
#                    value=Literal(5, )
#                    ),
#                    line=14,
#                    column=5,
#                )
#        ],
#        line=5,
#        column=37,
#    ),
#    line=5,
#    column=1,
#)

def test_check_function_has_no_errors():
    lexer = Lexer(source_code_correct)
    lexer.lexer()
    parser = Parser(lexer.tokens)
    program = parser.parse()
    
    type_checker = TypeChecker(source_code=source_code_correct)
    type_checker.check_function(program)
    assert len(type_checker.errors) == 0

        
        
