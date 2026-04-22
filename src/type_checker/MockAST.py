from dataclasses import dataclass

from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    Expression,
    ExpressionStatement,
    Grouping,
    IfStatement,
    Literal,
    Node,
    ParserError,
    Program,
    ReturnStatement,
    BreakStatement,
    Statement,
    Unary,
    Variable,
    WhileStatement,
    VarDeclaration,
    Function,
    Parameter,
    ArrayDeclaration,
    ArrayDeclarationEmpty,
    FunctionCall,
    Grouping
)
from TypeChecker.TypeChecker2 import TypeChecker
    
# DEMO PROGRAM

def build_functioncall_demo_program() -> Program:
    """
    Build a hand-written AST for this mock program:

        integer add(integer a, integer b) {
            return a + b;
        }

        float average(integer a, integer b) {
            return (a + b) / 2.0;
        }

        boolean is_positive(integer x) {
            return x > 0;
        }

        integer main() {
            integer x = add(3, 4);
            float y = average(x, 10);
            boolean ok = is_positive(x);

            x = add(x, 1);
            y = average(add(1, 2), 8);

            if (is_positive(x)) {
                x = add(x, 100);
            } else {
                x = add(x, 0);
            }

            add(1);               // wrong number of arguments
            average("hi", 2);     // wrong argument type
            mystery(1, 2);        // undefined function

            return x;
        }
    """

    # --------------------------------------------------------
    # function add(integer a, integer b) -> integer
    # --------------------------------------------------------
    add_function = Function(
        return_type="integer",
        name="add",
        parameters=[
            Parameter("integer", "a", line=1, column=13),
            Parameter("integer", "b", line=1, column=24),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Binary(
                        left=Variable("a", line=2, column=12),
                        operator="+",
                        right=Variable("b", line=2, column=16),
                        line=2,
                        column=14,
                    ),
                    line=2,
                    column=5,
                )
            ],
            line=1,
            column=35,
        ),
        line=1,
        column=1,
    )

    # --------------------------------------------------------
    # function average(integer a, integer b) -> float
    # --------------------------------------------------------
    average_function = Function(
        return_type="float",
        name="average",
        parameters=[
            Parameter("integer", "a", line=5, column=15),
            Parameter("integer", "b", line=5, column=26),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Binary(
                        left=Grouping(
                            expression=Binary(
                                left=Variable("a", line=6, column=13),
                                operator="+",
                                right=Variable("b", line=6, column=17),
                                line=6,
                                column=15,
                            ),
                            line=6,
                            column=12,
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

    # --------------------------------------------------------
    # function is_positive(integer x) -> boolean
    # --------------------------------------------------------
    is_positive_function = Function(
        return_type="boolean",
        name="is_positive",
        parameters=[
            Parameter("integer", "x", line=9, column=21),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Binary(
                        left=Variable("x", line=10, column=12),
                        operator=">",
                        right=Literal(0, line=10, column=16),
                        line=10,
                        column=14,
                    ),
                    line=10,
                    column=5,
                )
            ],
            line=9,
            column=32,
        ),
        line=9,
        column=1,
    )

    # --------------------------------------------------------
    # function main() -> integer
    # --------------------------------------------------------
    main_function = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                # integer x = add(3, 4);
                VarDeclaration(
                    type="integer",
                    name="x",
                    value=FunctionCall(
                        name="add",
                        arguments=[
                            Literal(3, line=14, column=21),
                            Literal(4, line=14, column=24),
                        ],
                        line=14,
                        column=17,
                    ),
                    line=14,
                    column=5,
                ),

                # float y = average(x, 10);
                VarDeclaration(
                    type="float",
                    name="y",
                    value=FunctionCall(
                        name="average",
                        arguments=[
                            Variable("x", line=15, column=23),
                            Literal(10, line=15, column=26),
                        ],
                        line=15,
                        column=15,
                    ),
                    line=15,
                    column=5,
                ),

                # boolean ok = is_positive(x);
                VarDeclaration(
                    type="boolean",
                    name="ok",
                    value=FunctionCall(
                        name="is_positive",
                        arguments=[
                            Variable("x", line=16, column=30),
                        ],
                        line=16,
                        column=18,
                    ),
                    line=16,
                    column=5,
                ),

                # x = add(x, 1);
                AssignStatement(
                    name="x",
                    value=FunctionCall(
                        name="add",
                        arguments=[
                            Variable("x", line=18, column=13),
                            Literal(1, line=18, column=16),
                        ],
                        line=18,
                        column=9,
                    ),
                    line=18,
                    column=5,
                ),

                # y = average(add(1, 2), 8);
                AssignStatement(
                    name="y",
                    value=FunctionCall(
                        name="average",
                        arguments=[
                            FunctionCall(
                                name="add",
                                arguments=[
                                    Literal(1, line=19, column=21),
                                    Literal(2, line=19, column=24),
                                ],
                                line=19,
                                column=17,
                            ),
                            Literal(8, line=19, column=29),
                        ],
                        line=19,
                        column=9,
                    ),
                    line=19,
                    column=5,
                ),

                # if (is_positive(x)) { x = add(x, 100); } else { x = add(x, 0); }
                IfStatement(
                    condition=FunctionCall(
                        name="is_positive",
                        arguments=[
                            Variable("x", line=21, column=21),
                        ],
                        line=21,
                        column=9,
                    ),
                    then_branch=BlockStatement(
                        statements=[
                            AssignStatement(
                                name="x",
                                value=FunctionCall(
                                    name="add",
                                    arguments=[
                                        Variable("x", line=22, column=17),
                                        Literal(100, line=22, column=20),
                                    ],
                                    line=22,
                                    column=13,
                                ),
                                line=22,
                                column=9,
                            )
                        ],
                        line=21,
                        column=25,
                    ),
                    else_branch=BlockStatement(
                        statements=[
                            AssignStatement(
                                name="x",
                                value=FunctionCall(
                                    name="add",
                                    arguments=[
                                        Variable("x", line=24, column=17),
                                        Literal(0, line=24, column=20),
                                    ],
                                    line=24,
                                    column=13,
                                ),
                                line=24,
                                column=9,
                            )
                        ],
                        line=23,
                        column=12,
                    ),
                    line=21,
                    column=5,
                ),

                # add(1);   -> wrong number of arguments
                ExpressionStatement(
                    expression=FunctionCall(
                        name="add",
                        arguments=[
                            Literal(1, line=27, column=9),
                        ],
                        line=27,
                        column=5,
                    ),
                    line=27,
                    column=5,
                ),

                # average("hi", 2);   -> wrong argument type
                ExpressionStatement(
                    expression=FunctionCall(
                        name="average",
                        arguments=[
                            Literal("hi", line=28, column=13),
                            Literal(2, line=28, column=19),
                        ],
                        line=28,
                        column=5,
                    ),
                    line=28,
                    column=5,
                ),

                # mystery(1, 2);   -> undefined function
                ExpressionStatement(
                    expression=FunctionCall(
                        name="mystery",
                        arguments=[
                            Literal(1, line=29, column=13),
                            Literal(2, line=29, column=16),
                        ],
                        line=29,
                        column=5,
                    ),
                    line=29,
                    column=5,
                ),

                # return x;
                ReturnStatement(
                    value=Variable("x", line=31, column=12),
                    line=31,
                    column=5,
                ),
            ],
            line=13,
            column=16,
        ),
        line=13,
        column=1,
    )

    return Program(
        functions=[
            add_function,
            average_function,
            is_positive_function,
            main_function,
        ],
        line=1,
        column=1,
    )
def functioncall_demo_source() -> str:
    return """integer add(integer a, integer b) {
    return a + b;
}

float average(integer a, integer b) {
    return (a + b) / 2.0;
}

boolean is_positive(integer x) {
    return x > 0;
}

integer main() {
    integer x = add(3, 4);
    float y = average(x, 10);
    boolean ok = is_positive(x);

    x = add(x, 1);
    y = average(add(1, 2), 8);

    if (is_positive(x)) {
        x = add(x, 100);
    } else {
        x = add(x, 0);
    }

    add(1);
    average("hi", 2);
    mystery(1, 2);

    return x;
}"""

if __name__ == "__main__":
    source_code = functioncall_demo_source()
    program = build_functioncall_demo_program()

    checker = TypeChecker(source_code)
    checker.check(program)

    if checker.errors:
        print("Type check failed:\n")
        for err in checker.formatted_errors():
            print(err)
            print()
    else:
        print("Type check passed.")

