import pytest

from lexer.lexer import Lexer
from parser.parser import Parser
from error_handling import ParserError
from parser.ASTNodes import (
    Program,
    Function,
    BlockStatement,
    VarDeclaration,
    ReturnStatement,
    IfStatement,
    WhileStatement,
    ArrayDeclaration,
    ArrayDeclarationEmpty,
    AssignStatement,
    ExpressionStatement,
    FunctionCall,
    ArrayAccess,
    Binary,
    Unary,
    Variable,
    Literal,
)


def parse_source(source_code: str):
    lexer = Lexer(source_code)
    lexer.lexer()
    parser = Parser(lexer.tokens)
    return parser.parse()


def test_parse_simple_valid_program():
    source_code = """
integer main() {
    integer x = 5;
    return x;
}
"""

    program = parse_source(source_code)

    assert isinstance(program, Program)
    assert len(program.functions) == 1

    fn = program.functions[0]
    assert isinstance(fn, Function)
    assert fn.name == "main"
    assert fn.return_type == "integer"
    assert isinstance(fn.statement, BlockStatement)
    assert len(fn.statement.statements) == 2

    assert isinstance(fn.statement.statements[0], VarDeclaration)
    assert isinstance(fn.statement.statements[1], ReturnStatement)


def test_parse_function_call_program():
    source_code = """
integer add(integer a, integer b) {
    return a + b;
}

integer main() {
    integer x = add(1, 2);
    return x;
}
"""

    program = parse_source(source_code)

    assert isinstance(program, Program)
    assert len(program.functions) == 2

    add_fn = program.functions[0]
    main_fn = program.functions[1]

    assert add_fn.name == "add"
    assert len(add_fn.parameters) == 2

    assert main_fn.name == "main"
    assert isinstance(main_fn.statement, BlockStatement)

    decl_stmt = main_fn.statement.statements[0]
    assert isinstance(decl_stmt, VarDeclaration)
    assert isinstance(decl_stmt.value, FunctionCall)
    assert decl_stmt.value.name == "add"
    assert len(decl_stmt.value.arguments) == 2


def test_parse_nested_function_calls():
    source_code = """
integer add(integer a, integer b) {
    return a + b;
}

integer main() {
    integer x = add(add(1, 2), add(3, 4));
    return x;
}
"""

    program = parse_source(source_code)

    main_fn = program.functions[1]
    decl_stmt = main_fn.statement.statements[0]

    assert isinstance(decl_stmt, VarDeclaration)
    assert isinstance(decl_stmt.value, FunctionCall)
    assert decl_stmt.value.name == "add"
    assert len(decl_stmt.value.arguments) == 2

    left_arg = decl_stmt.value.arguments[0]
    right_arg = decl_stmt.value.arguments[1]

    assert isinstance(left_arg, FunctionCall)
    assert isinstance(right_arg, FunctionCall)
    assert left_arg.name == "add"
    assert right_arg.name == "add"


def test_parse_if_else_and_while_program():
    source_code = """
integer main() {
    integer x = 0;

    while (x < 10) {
        if (x == 5) {
            x = x + 2;
        } else {
            x = x + 1;
        }
    }

    return x;
}
"""

    program = parse_source(source_code)

    assert isinstance(program, Program)
    assert len(program.functions) == 1

    fn = program.functions[0]
    assert fn.name == "main"
    assert isinstance(fn.statement, BlockStatement)

    stmts = fn.statement.statements
    assert len(stmts) == 3

    assert isinstance(stmts[0], VarDeclaration)
    assert isinstance(stmts[1], WhileStatement)
    assert isinstance(stmts[2], ReturnStatement)

    while_stmt = stmts[1]
    assert isinstance(while_stmt.body, BlockStatement)
    assert len(while_stmt.body.statements) == 1
    assert isinstance(while_stmt.body.statements[0], IfStatement)

    if_stmt = while_stmt.body.statements[0]
    assert isinstance(if_stmt.then_branch, BlockStatement)
    assert isinstance(if_stmt.else_branch, BlockStatement)


def test_parse_array_declaration_and_access_program():
    source_code = """
integer main() {
    integer arr[3] = [1, 2, 3];
    integer empty[5];
    arr[1] = 99;
    print(arr[1]);
    return arr[1];
}
"""

    program = parse_source(source_code)

    assert isinstance(program, Program)
    assert len(program.functions) == 1

    fn = program.functions[0]
    stmts = fn.statement.statements

    assert isinstance(stmts[0], ArrayDeclaration)
    assert isinstance(stmts[1], ArrayDeclarationEmpty)
    assert isinstance(stmts[2], AssignStatement)
    assert isinstance(stmts[3], ExpressionStatement)
    assert isinstance(stmts[4], ReturnStatement)

    assign_stmt = stmts[2]
    assert assign_stmt.name == "arr"
    assert assign_stmt.offset is not None

    expr_stmt = stmts[3]
    assert isinstance(expr_stmt.expression, FunctionCall)
    assert expr_stmt.expression.name == "print"
    assert len(expr_stmt.expression.arguments) == 1
    assert isinstance(expr_stmt.expression.arguments[0], ArrayAccess)

    return_stmt = stmts[4]
    assert isinstance(return_stmt.value, ArrayAccess)


def test_parse_assignment_and_expression_statement_program():
    source_code = """
void main() {
    integer x = 1;
    x = x + 2;
    print(x);
    return;
}
"""

    program = parse_source(source_code)

    assert isinstance(program, Program)
    assert len(program.functions) == 1

    fn = program.functions[0]
    stmts = fn.statement.statements

    assert isinstance(stmts[0], VarDeclaration)
    assert isinstance(stmts[1], AssignStatement)
    assert isinstance(stmts[2], ExpressionStatement)
    assert isinstance(stmts[3], ReturnStatement)


def test_parse_unary_expression_in_condition():
    source_code = """
integer main() {
    boolean x = true;
    if (!x) {
        return 1;
    } else {
        return 0;
    }
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    if_stmt = fn.statement.statements[1]

    assert isinstance(if_stmt, IfStatement)
    assert isinstance(if_stmt.condition, Unary)
    assert if_stmt.condition.operator == "!"


def test_parse_logical_and_or_conditions():
    source_code = """
integer main() {
    boolean x = true;
    boolean y = false;
    if (x AND y OR x) {
        return 1;
    } else {
        return 0;
    }
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    if_stmt = fn.statement.statements[2]

    assert isinstance(if_stmt, IfStatement)
    assert isinstance(if_stmt.condition, Binary)

    assert if_stmt.condition.operator == "OR"

    left = if_stmt.condition.left
    right = if_stmt.condition.right

    assert isinstance(left, Binary)
    assert left.operator == "AND"
    assert isinstance(left.left, Variable)
    assert isinstance(left.right, Variable)
    assert isinstance(right, Variable)


def test_parse_mod_operator():
    source_code = """
integer main() {
    integer x = 10 MOD 3;
    return x;
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    decl_stmt = fn.statement.statements[0]

    assert isinstance(decl_stmt, VarDeclaration)
    assert isinstance(decl_stmt.value, Binary)
    assert decl_stmt.value.operator == "MOD"


def test_parse_print_with_string_literals_and_variables():
    source_code = """
void main() {
    integer x = 5;
    integer y = 7;
    print("x = : ", x, "and y is = : ", y);
    return;
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    expr_stmt = fn.statement.statements[2]

    assert isinstance(expr_stmt, ExpressionStatement)
    assert isinstance(expr_stmt.expression, FunctionCall)
    assert expr_stmt.expression.name == "print"
    assert len(expr_stmt.expression.arguments) == 4

    assert isinstance(expr_stmt.expression.arguments[0], Literal)
    assert isinstance(expr_stmt.expression.arguments[1], Variable)
    assert isinstance(expr_stmt.expression.arguments[2], Literal)
    assert isinstance(expr_stmt.expression.arguments[3], Variable)


def test_parse_empty_parameter_list():
    source_code = """
integer main() {
    return 0;
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    assert fn.name == "main"
    assert fn.parameters == []


def test_parse_multiple_parameters():
    source_code = """
integer add(integer a, integer b, integer c) {
    return a + b + c;
}
"""

    program = parse_source(source_code)

    fn = program.functions[0]
    assert fn.name == "add"
    assert len(fn.parameters) == 3
    assert fn.parameters[0].name == "a"
    assert fn.parameters[1].name == "b"
    assert fn.parameters[2].name == "c"


def test_parse_missing_semicolon_raises_parser_error():
    source_code = """
integer main() {
    integer x = 5
    return x;
}
"""

    with pytest.raises(ParserError):
        parse_source(source_code)


def test_parse_missing_right_paren_raises_parser_error():
    source_code = """
integer main() {
    integer x = (1 + 2;
    return x;
}
"""

    with pytest.raises(ParserError):
        parse_source(source_code)


def test_parse_malformed_function_header_raises_parser_error():
    source_code = """
integer main( {
    return 0;
}
"""

    with pytest.raises(ParserError):
        parse_source(source_code)


def test_parse_bad_if_syntax_raises_parser_error():
    source_code = """
integer main() {
    if x < 5) {
        return 1;
    }
    return 0;
}
"""

    with pytest.raises(ParserError):
        parse_source(source_code)


def test_parse_bad_array_assignment_syntax_raises_parser_error():
    source_code = """
integer main() {
    integer arr[3] = [1, 2, 3];
    arr[1 = 5;
    return 0;
}
"""

    with pytest.raises(ParserError):
        parse_source(source_code)