from dataclasses import dataclass

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
    Function,
    Parameter,
    ArrayDeclaration,
    ArrayDeclarationEmpty,
    FunctionCall
)


program = Program(statements=[

    # line 1: integer x = 10;
    VarDeclaration(
        name="x",
        declared_type="integer",
        line=1,
        column=1,

        initializer=Literal(
            value=10,
            line=1,
            column=13
        )
    ),

    # line 2: if (x > 5) { ... }
    IfStatement(
        line=2,
        column=1,

        condition=Binary(
            left=Variable("x", line=2, column=5),
            operator=">",
            right=Literal(5, line=2, column=9),
            line=2,
            column=7
        ),

        then_branch=BlockStatement(
            line=2,
            column=12,
            statements=[

                # line 3: x = x + 1;
                AssignStatement(
                    name="x",
                    line=3,
                    column=5,

                    value=Binary(
                        left=Variable("x", line=3, column=9),
                        operator="+",
                        right=Literal(1, line=3, column=13),
                        line=3,
                        column=11
                    )
                ),

                # line 4: return x;
                ReturnStatement(
                    value=Variable("x", line=4, column=12),
                    line=4,
                    column=5
                ),
            ]
        ),

        else_branch=BlockStatement(
            line=5,
            column=8,
            statements=[
                ReturnStatement(
                    value=Literal(0, line=6, column=12),
                    line=6,
                    column=5
                )
            ]
        )
    )
])