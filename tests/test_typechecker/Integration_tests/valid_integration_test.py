from parser.ASTNodes import (
    Binary,
    BlockStatement,
    Function,
    FunctionCall,
    Literal,
    Parameter,
    Program,
    ReturnStatement,
    VarDeclaration,
    Variable,
)
from type_checker.TypeChecker import TypeChecker


def test_typechecker_valid_program_integration():
    source_code = """
integer add(integer a, integer b) {
    return a + b;
}

integer main() {
    integer x = add(3, 4);
    return x;
}
"""

    add_function = Function(
        return_type="integer",
        name="add",
        parameters=[
            Parameter("integer", "a", line=2, column=21),
            Parameter("integer", "b", line=2, column=32),
        ],
        statement=BlockStatement(
            statements=[
                ReturnStatement(
                    value=Binary(
                        left=Variable("a", line=3, column=12),
                        operator="+",
                        right=Variable("b", line=3, column=16),
                        line=3,
                        column=14,
                    ),
                    line=3,
                    column=5,
                )
            ],
            line=2,
            column=35,
        ),
        line=2,
        column=1,
    )

    main_function = Function(
        return_type="integer",
        name="main",
        parameters=[],
        statement=BlockStatement(
            statements=[
                VarDeclaration(
                    type="integer",
                    name="x",
                    value=FunctionCall(
                        name="add",
                        arguments=[
                            Literal(3, line=7, column=21),
                            Literal(4, line=7, column=24),
                        ],
                        line=7,
                        column=17,
                    ),
                    line=7,
                    column=5,
                ),
                ReturnStatement(
                    value=Variable("x", line=8, column=12),
                    line=8,
                    column=5,
                ),
            ],
            line=6,
            column=16,
        ),
        line=6,
        column=1,
    )

    program = Program(
        functions=[add_function, main_function],
        line=1,
        column=1,
    )

    checker = TypeChecker(source_code)
    checker.check(program)

    assert checker.errors == []