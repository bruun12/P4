
from type_checker.TypeChecker import TypeChecker
from parser.ASTNodes import (
    Binary,
    BlockStatement,
    Function,
    Literal,
    Parameter,
    ReturnStatement,
    Variable,
)

import pytest

source_code = """        
    double average(integer a, integer b) {
    return (a + b) / 2.0;
    }
    """

average_function = Function(
    return_type="double",
    name="average",
    parameters=[
        Parameter("integer", "a", line=5, column=15),
        Parameter("integer", "b", line=5, column=26),
    ],
    statement=BlockStatement(
        statements=[
            ReturnStatement(
                value=Binary(
                    left=Binary(
                        left=Variable("a", line=6, column=13),
                        operator="+",
                        right=Variable("b", line=6, column=17),
                        line=6,
                        column=15,
                    ),
                    operator="/",
                    right=Literal(2.0, line=6, column=23),
                    line=6,
                    column=20,
                ),
                line=6,
                column=5,
            )
        ],
        line=5,
        column=37,
    ),
    line=5,
    column=1,
)

def test_check_function_has_no_errors():
    type_checker = TypeChecker(source_code=source_code)
    type_checker.check_function(average_function)
    assert len(type_checker.errors) == 0

        
        
