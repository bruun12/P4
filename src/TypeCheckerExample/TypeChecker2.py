from __future__ import annotations

from dataclasses import dataclass


# ============================================================
# AST NODES
# ============================================================
# These AST nodes are rewritten to fix the structural problems
# in the previous version.
#
# IMPORTANT CHANGES APPLIED HERE:
#
# 1. Every concrete node now stores line/column properly.
#    This fixes the earlier issue where several nodes did not
#    call Node.__init__ and therefore had no source position.
#
# 2. Program, Function, Parameter, VarDeclaration,
#    ArrayDeclaration, ArrayDeclarationEmpty, and Literal now
#    all carry line/column.
#
# 3. VarDeclaration now correctly stores its declared type.
#    The earlier version accepted a type but did not store it.
#
# 4. Literal now carries line/column so diagnostics can point
#    to the exact literal location.
#
# 5. Parameter uses "param_type" instead of "type" to avoid
#    shadowing Python's built-in name "type".
#
# 6. Function uses "body" instead of "statement" because
#    "body" is clearer and more conventional.
# ============================================================


# ------------------------------------------------------------
# Base node classes
# ------------------------------------------------------------

class Node:
    """
    Base AST node.

    Every node carries line/column so the type checker can
    report precise diagnostics.
    """
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


class Statement(Node):
    """Base class for all statement nodes."""
    pass


class Expression(Node):
    """Base class for all expression nodes."""
    pass


# ------------------------------------------------------------
# Program / function-level nodes
# ------------------------------------------------------------

class Program(Node):
    """
    Top-level program node.

    CHANGE APPLIED:
    The program is now function-centered. A program contains
    functions, because your language design now treats functions
    as the top-level units.
    """
    def __init__(self, functions: list["Function"], line: int = 1, column: int = 1):
        super().__init__(line, column)
        self.functions = functions


class Function(Node):
    """
    Function declaration.

    CHANGE APPLIED:
    - now calls super().__init__(line, column)
    - uses 'body' instead of 'statement'
    """
    def __init__(
        self,
        return_type: str,
        name: str,
        parameters: list["Parameter"],
        body: Statement,
        line: int,
        column: int,
    ):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body


class Parameter(Node):
    """
    Function parameter.

    CHANGE APPLIED:
    - now calls super().__init__(line, column)
    - field renamed from 'type' to 'param_type'
    """
    def __init__(self, param_type: str, name: str, line: int, column: int):
        super().__init__(line, column)
        self.param_type = param_type
        self.name = name


# ------------------------------------------------------------
# Statement nodes
# ------------------------------------------------------------

class BlockStatement(Statement):
    def __init__(self, statements: list[Statement], line: int, column: int):
        super().__init__(line, column)
        self.statements = statements


class VarDeclaration(Statement):
    """
    Variable declaration.

    CHANGE APPLIED:
    The earlier version accepted a declared type but did not
    store it. This version stores it correctly in self.var_type.
    """
    def __init__(self, var_type: str, name: str, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.value = value


class AssignStatement(Statement):
    def __init__(self, name: str, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.value = value


class IfStatement(Statement):
    def __init__(
        self,
        condition: Expression,
        then_branch: Statement,
        else_branch: Statement | None,
        line: int,
        column: int,
    ):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement, line: int, column: int):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class ReturnStatement(Statement):
    def __init__(self, value: Expression | None, line: int, column: int):
        super().__init__(line, column)
        self.value = value


class BreakStatement(Statement):
    def __init__(self, line: int, column: int):
        super().__init__(line, column)


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression


class ArrayDeclaration(Statement):
    """
    Array declaration with explicit elements.

    Example:
        integer[] arr = [1, 2, 3];

    CHANGE APPLIED:
    - stores line/column
    - stores declared element type as array_type
    """
    def __init__(self, array_type: str, name: str, elements: list[Expression], line: int, column: int):
        super().__init__(line, column)
        self.array_type = array_type
        self.name = name
        self.elements = elements


class ArrayDeclarationEmpty(Statement):
    """
    Empty-sized array declaration.

    Example:
        integer[] arr[3];

    CHANGE APPLIED:
    - stores line/column
    """
    def __init__(self, array_type: str, name: str, size: Expression, line: int, column: int):
        super().__init__(line, column)
        self.array_type = array_type
        self.name = name
        self.size = size


# ------------------------------------------------------------
# Expression nodes
# ------------------------------------------------------------

class Literal(Expression):
    """
    Literal value.

    CHANGE APPLIED:
    Literal now carries line/column, so errors involving a
    literal can point to the exact source position.
    """
    def __init__(self, value: object, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def get_value(self):
        return self.value


class Variable(Expression):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(line, column)
        self.name = name


class Unary(Expression):
    def __init__(self, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.operator = operator
        self.right = right


class Binary(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expression):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression


# ============================================================
# TYPE OBJECTS
# ============================================================

class Type:
    pass


@dataclass(frozen=True)
class IntegerType(Type):
    pass


@dataclass(frozen=True)
class FloatType(Type):
    pass


@dataclass(frozen=True)
class BooleanType(Type):
    pass


@dataclass(frozen=True)
class StringType(Type):
    pass


@dataclass(frozen=True)
class NullType(Type):
    pass


@dataclass(frozen=True)
class ErrorType(Type):
    pass


@dataclass(frozen=True)
class ArrayType(Type):
    """
    Array type with an element type.

    Example:
        ArrayType(INTEGER)
    """
    element_type: Type


@dataclass(frozen=True)
class FunctionType(Type):
    """
    Function signature type.

    CHANGE APPLIED IN TYPECHECKER DESIGN:
    Because programs are now function-centered, the checker
    stores function signatures separately from local variables.
    """
    parameter_types: tuple[Type, ...]
    return_type: Type


INTEGER = IntegerType()
FLOAT = FloatType()
BOOLEAN = BooleanType()
STRING = StringType()
NULL = NullType()
ERROR = ErrorType()


# ============================================================
# FLOW RESULT
# ============================================================

@dataclass(frozen=True)
class FlowResult:
    definitely_returns: bool
    breaks_loop: bool
    unreachable: bool


NO_FLOW = FlowResult(
    definitely_returns=False,
    breaks_loop=False,
    unreachable=False,
)

RETURNS = FlowResult(
    definitely_returns=True,
    breaks_loop=False,
    unreachable=False,
)

BREAKS = FlowResult(
    definitely_returns=False,
    breaks_loop=True,
    unreachable=False,
)

UNREACHABLE = FlowResult(
    definitely_returns=False,
    breaks_loop=False,
    unreachable=True,
)


# ============================================================
# TYPE ERROR + FORMATTING
# ============================================================

class TypeCheckError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column


def format_type_error(error: TypeCheckError, source_lines: list[str]) -> str:
    """
    Pretty-print a type error with source context.
    """
    line = error.line
    column = error.column

    if line < 1 or line > len(source_lines):
        return f"Type error: {error.message} [line {line}, col {column}]"

    code_line = source_lines[line - 1]
    caret_line = " " * max(column - 1, 0) + "^"

    return (
        f"Type error: {error.message}\n"
        f" --> line {line}, col {column}\n"
        f"  |\n"
        f"{line} | {code_line}\n"
        f"  | {caret_line}"
    )


# ============================================================
# ENVIRONMENTS
# ============================================================

class TypeEnvironment:
    """
    Nested variable environment for parameters and local variables.
    """
    def __init__(self, parent: "TypeEnvironment | None" = None):
        self.parent = parent
        self.values: dict[str, Type] = {}

    def define(self, name: str, typ: Type) -> None:
        self.values[name] = typ

    def contains_in_current_scope(self, name: str) -> bool:
        return name in self.values

    def get(self, name: str) -> Type:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise TypeCheckError(f"Undefined variable '{name}'.", 0, 0)


class FunctionEnvironment:
    """
    Global function environment.

    CHANGE APPLIED:
    Functions are now top-level program nodes, so they get their
    own environment separate from variable scopes.
    """
    def __init__(self):
        self.values: dict[str, FunctionType] = {}

    def define(self, name: str, typ: FunctionType) -> None:
        self.values[name] = typ

    def contains(self, name: str) -> bool:
        return name in self.values

    def get(self, name: str) -> FunctionType:
        if name in self.values:
            return self.values[name]
        raise TypeCheckError(f"Undefined function '{name}'.", 0, 0)


# ============================================================
# HELPERS
# ============================================================

def type_name(t: Type) -> str:
    if t == INTEGER:
        return "integer"
    if t == FLOAT:
        return "float"
    if t == BOOLEAN:
        return "boolean"
    if t == STRING:
        return "string"
    if t == NULL:
        return "null"
    if t == ERROR:
        return "<error>"
    if isinstance(t, ArrayType):
        return f"{type_name(t.element_type)}[]"
    if isinstance(t, FunctionType):
        # 1. Convert each type object into its string name (e.g., [integer, float])
        name_list = []
        for p in t.parameter_types:
            name_list.append(type_name(p))

        # 2. Join them with commas (e.g., "integer, float")
        params_string = ", ".join(name_list)

        # 3. Build the final function signature
        return f"function({params_string}) -> {type_name(t.return_type)}"
    return repr(t)


def is_numeric(t: Type) -> bool:
    return t == INTEGER or t == FLOAT


def can_assign(target: Type, value: Type) -> bool:
    """
    Assignment compatibility.

    Rules:
    - exact same type is allowed
    - integer can be assigned to float
    - arrays must have matching element type
    """
    if target == value:
        return True

    if target == FLOAT and value == INTEGER:
        return True

    if isinstance(target, ArrayType) and isinstance(value, ArrayType):
        return can_assign(target.element_type, value.element_type)

    return False


def numeric_result_type(left: Type, right: Type) -> Type:
    if left == FLOAT or right == FLOAT:
        return FLOAT
    return INTEGER


def parse_declared_type(declared_type: str) -> Type:
    """
    Parse a declared primitive type string.
    """
    if declared_type == "integer":
        return INTEGER
    if declared_type == "float":
        return FLOAT
    if declared_type == "boolean":
        return BOOLEAN
    if declared_type == "string":
        return STRING
    if declared_type == "null":
        return NULL

    raise TypeCheckError(f"Unknown declared type '{declared_type}'.", 0, 0)


# ============================================================
# TYPE CHECKER
# ============================================================
# This checker is rewritten around the corrected AST.
#
# MAJOR DESIGN CHANGE APPLIED:
# The top-level driver no longer iterates through program
# statements. It now:
#   1. collects function signatures
#   2. checks each function body
#
# This matches your updated language design much better.
# ============================================================

class TypeChecker:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.errors: list[TypeCheckError] = []

        # Global function signatures live here.
        self.function_env = FunctionEnvironment()

        # These are set while checking a function body.
        self.current_function_name: str | None = None
        self.expected_return_type: Type | None = None

    # --------------------------------------------------------
    # Error helpers
    # --------------------------------------------------------

    def report(self, node: Node, message: str) -> None:
        self.errors.append(TypeCheckError(message, node.line, node.column))

    def formatted_errors(self) -> list[str]:
        return [format_type_error(err, self.source_lines) for err in self.errors]

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    # --------------------------------------------------------
    # Type parsing helper
    # --------------------------------------------------------

    def parse_type_node(self, declared_type: str, node: Node) -> Type:
        """
        Parse a declared type and tie errors to the node that
        declared it.
        """
        try:
            return parse_declared_type(declared_type)
        except TypeCheckError as err:
            self.errors.append(TypeCheckError(err.message, node.line, node.column))
            return ERROR
    # --------------------------------------------------------
    # Public entry point
    # --------------------------------------------------------

    def check(self, program: Program) -> None:
        """
        Type-check a complete program.

        CHANGE APPLIED:
        Program is function-centered, so checking now happens in
        two passes:
          pass 1: collect all function signatures
          pass 2: check each function body
        """
        self.collect_function_signatures(program)
        self.check_all_functions(program)

    # --------------------------------------------------------
    # Pass 1: collect function signatures
    # --------------------------------------------------------

    def collect_function_signatures(self, program: Program) -> None:
        for function in program.functions:
            if self.function_env.contains(function.name):
                self.report(function, f"Function '{function.name}' is already declared.")
                continue

            return_type = self.parse_type_node(function.return_type, function)

            parameter_types: list[Type] = []
            for parameter in function.parameters:
                param_type = self.parse_type_node(parameter.param_type, parameter)
                parameter_types.append(param_type)

            self.function_env.define(
                function.name,
                FunctionType(
                    parameter_types=tuple(parameter_types),
                    return_type=return_type,
                )
            )

    # --------------------------------------------------------
    # Pass 2: check each function body
    # --------------------------------------------------------

    def check_all_functions(self, program: Program) -> None:
        for function in program.functions:
            self.check_function(function)

    def check_function(self, function: Function) -> None:
        """
        Type-check one function.

        CHANGE APPLIED:
        Parameters are introduced into a fresh function-local
        environment, and the function's body is checked with its
        declared expected return type.
        """
        previous_function_name = self.current_function_name
        previous_expected_return_type = self.expected_return_type

        self.current_function_name = function.name
        self.expected_return_type = self.parse_type_node(function.return_type, function)

        local_env = TypeEnvironment()

        # Add parameters as local variables
        for parameter in function.parameters:
            param_type = self.parse_type_node(parameter.param_type, parameter)

            if local_env.contains_in_current_scope(parameter.name):
                self.report(parameter, f"Duplicate parameter '{parameter.name}' in function '{function.name}'.")
                continue

            local_env.define(parameter.name, param_type)

        flow = self.check_statement(function.body, local_env, inside_loop=False)

        # Enforce that the function returns on all paths.
        if self.expected_return_type != NULL and not flow.definitely_returns:
            self.report(
                function,
                f"Function '{function.name}' may not return a value on all paths."
            )

        self.current_function_name = previous_function_name
        self.expected_return_type = previous_expected_return_type

    # --------------------------------------------------------
    # Statement checking
    # --------------------------------------------------------

    def check_statement(
        self,
        stmt: Statement,
        env: TypeEnvironment,
        inside_loop: bool,
    ) -> FlowResult:

        # ----------------------------------------------------
        # BlockStatement
        # ----------------------------------------------------
        if isinstance(stmt, BlockStatement):
            block_env = TypeEnvironment(parent=env)
            saw_terminal_flow = False

            for inner_stmt in stmt.statements:
                if saw_terminal_flow:
                    self.report(inner_stmt, "Unreachable statement.")
                    continue

                flow = self.check_statement(inner_stmt, block_env, inside_loop)

                if flow.unreachable:
                    self.report(inner_stmt, "Unreachable statement.")

                if flow.definitely_returns:
                    saw_terminal_flow = True
                    return RETURNS

                if flow.breaks_loop:
                    saw_terminal_flow = True
                    return BREAKS

            return NO_FLOW

        # ----------------------------------------------------
        # VarDeclaration
        # ----------------------------------------------------
        if isinstance(stmt, VarDeclaration):
            declared_type = self.parse_type_node(stmt.var_type, stmt)
            value_type = self.check_expression(stmt.value, env)

            if env.contains_in_current_scope(stmt.name):
                self.report(stmt, f"Variable '{stmt.name}' is already declared in this scope.")

            if declared_type != ERROR and value_type != ERROR:
                if not can_assign(declared_type, value_type):
                    self.report(
                        stmt.value,
                        f"Cannot initialize variable '{stmt.name}' of type "
                        f"{type_name(declared_type)} with value of type {type_name(value_type)}."
                    )

            env.define(stmt.name, declared_type)
            return NO_FLOW

        # ----------------------------------------------------
        # ArrayDeclaration
        # ----------------------------------------------------
        if isinstance(stmt, ArrayDeclaration):
            element_type = self.parse_type_node(stmt.array_type, stmt)
            array_type = ArrayType(element_type)

            if env.contains_in_current_scope(stmt.name):
                self.report(stmt, f"Variable '{stmt.name}' is already declared in this scope.")

            for element in stmt.elements:
                element_expr_type = self.check_expression(element, env)
                if element_type != ERROR and element_expr_type != ERROR:
                    if not can_assign(element_type, element_expr_type):
                        self.report(
                            element,
                            f"Cannot place element of type {type_name(element_expr_type)} "
                            f"into array '{stmt.name}' of element type {type_name(element_type)}."
                        )

            env.define(stmt.name, array_type)
            return NO_FLOW

        # ----------------------------------------------------
        # ArrayDeclarationEmpty
        # ----------------------------------------------------
        if isinstance(stmt, ArrayDeclarationEmpty):
            element_type = self.parse_type_node(stmt.array_type, stmt)
            array_type = ArrayType(element_type)

            if env.contains_in_current_scope(stmt.name):
                self.report(stmt, f"Variable '{stmt.name}' is already declared in this scope.")

            size_type = self.check_expression(stmt.size, env)
            if size_type != ERROR and size_type != INTEGER:
                self.report(
                    stmt.size,
                    f"Array size must be integer, got {type_name(size_type)}."
                )

            env.define(stmt.name, array_type)
            return NO_FLOW

        # ----------------------------------------------------
        # AssignStatement
        # ----------------------------------------------------
        if isinstance(stmt, AssignStatement):
            try:
                target_type = env.get(stmt.name)
            except TypeCheckError:
                self.report(stmt, f"Undefined variable '{stmt.name}'.")
                target_type = ERROR

            value_type = self.check_expression(stmt.value, env)

            if target_type != ERROR and value_type != ERROR:
                if not can_assign(target_type, value_type):
                    self.report(
                        stmt.value,
                        f"Cannot assign value of type {type_name(value_type)} "
                        f"to variable '{stmt.name}' of type {type_name(target_type)}."
                    )

            return NO_FLOW

        # ----------------------------------------------------
        # IfStatement
        # ----------------------------------------------------
        if isinstance(stmt, IfStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != ERROR and condition_type != BOOLEAN:
                self.report(
                    stmt.condition,
                    f"If condition must be boolean, got {type_name(condition_type)}."
                )

            then_env = TypeEnvironment(parent=env)
            then_flow = self.check_statement(stmt.then_branch, then_env, inside_loop)

            if stmt.else_branch is None:
                return NO_FLOW

            else_env = TypeEnvironment(parent=env)
            else_flow = self.check_statement(stmt.else_branch, else_env, inside_loop)

            return FlowResult(
                definitely_returns=(
                    then_flow.definitely_returns and else_flow.definitely_returns
                ),
                breaks_loop=(
                    then_flow.breaks_loop and else_flow.breaks_loop
                ),
                unreachable=False,
            )

        # ----------------------------------------------------
        # WhileStatement
        # ----------------------------------------------------
        if isinstance(stmt, WhileStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != ERROR and condition_type != BOOLEAN:
                self.report(
                    stmt.condition,
                    f"While condition must be boolean, got {type_name(condition_type)}."
                )

            body_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.body, body_env, inside_loop=True)

            # Conservative choice:
            # we do not claim that a while-loop definitely returns
            # because it may execute zero times, many times, or end
            # via break.
            return NO_FLOW

        # ----------------------------------------------------
        # ReturnStatement
        # ----------------------------------------------------
        if isinstance(stmt, ReturnStatement):
            if self.expected_return_type is None:
                self.report(stmt, "Return statement is not allowed here.")
                return RETURNS

            if stmt.value is None:
                self.report(stmt, "Return statement must include a value.")
                return RETURNS

            value_type = self.check_expression(stmt.value, env)

            if value_type != ERROR and not can_assign(self.expected_return_type, value_type):
                self.report(
                    stmt.value,
                    f"Return type mismatch in function '{self.current_function_name}': "
                    f"expected {type_name(self.expected_return_type)}, got {type_name(value_type)}."
                )

            return RETURNS

        # ----------------------------------------------------
        # BreakStatement
        # ----------------------------------------------------
        if isinstance(stmt, BreakStatement):
            if not inside_loop:
                self.report(stmt, "'break' used outside of a loop.")
            return BREAKS

        # ----------------------------------------------------
        # ExpressionStatement
        # ----------------------------------------------------
        if isinstance(stmt, ExpressionStatement):
            self.check_expression(stmt.expression, env)
            return NO_FLOW

        self.report(stmt, f"Unknown statement node: {stmt!r}")
        return NO_FLOW

    # --------------------------------------------------------
    # Expression checking
    # --------------------------------------------------------

    def check_expression(self, expr: Expression, env: TypeEnvironment) -> Type:
        if isinstance(expr, Literal):
            value = expr.value

            if value is None:
                return NULL

            # bool before int because Python bool is a subclass of int
            if isinstance(value, bool):
                return BOOLEAN

            if isinstance(value, int):
                return INTEGER

            if isinstance(value, float):
                return FLOAT

            if isinstance(value, str):
                return STRING

            self.report(expr, f"Unsupported literal value {value!r}.")
            return ERROR

        if isinstance(expr, Variable):
            try:
                return env.get(expr.name)
            except TypeCheckError:
                self.report(expr, f"Undefined variable '{expr.name}'.")
                return ERROR

        if isinstance(expr, Grouping):
            return self.check_expression(expr.expression, env)

        if isinstance(expr, Unary):
            right_type = self.check_expression(expr.right, env)

            if right_type == ERROR:
                return ERROR

            if expr.operator == "-":
                if not is_numeric(right_type):
                    self.report(
                        expr,
                        f"Unary '-' requires integer or float, got {type_name(right_type)}."
                    )
                    return ERROR
                return right_type

            if expr.operator == "!":
                if right_type != BOOLEAN:
                    self.report(
                        expr,
                        f"Unary '!' requires boolean, got {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            self.report(expr, f"Unknown unary operator '{expr.operator}'.")
            return ERROR

        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            if left_type == ERROR or right_type == ERROR:
                return ERROR

            # Arithmetic
            if op in {"+", "-", "*", "/", "%"}:
                if op == "+" and left_type == STRING and right_type == STRING:
                    return STRING

                if not is_numeric(left_type) or not is_numeric(right_type):
                    self.report(
                        expr,
                        f"Operator '{op}' requires numeric operands "
                        f"(or string + string for '+'), got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR

                return numeric_result_type(left_type, right_type)

            # Comparison
            if op in {"<", "<=", ">", ">="}:
                if not is_numeric(left_type) or not is_numeric(right_type):
                    self.report(
                        expr,
                        f"Operator '{op}' requires numeric operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Equality
            if op in {"==", "!="}:
                if left_type != right_type:
                    self.report(
                        expr,
                        f"Operator '{op}' requires both sides to have the same type, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Logical
            if op in {"&&", "||"}:
                if left_type != BOOLEAN or right_type != BOOLEAN:
                    self.report(
                        expr,
                        f"Operator '{op}' requires boolean operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            self.report(expr, f"Unknown binary operator '{op}'.")
            return ERROR

        self.report(expr, f"Unknown expression node: {expr!r}")
        return ERROR




# ============================================================
# OPTIONAL CONVENIENCE RUNNER
# ============================================================
# The earlier extra helper functions are no longer central to
# the design, because the important notion of "functions" is
# now represented in the AST itself. A small runner like this is
# enough for most use cases.
# ============================================================

def run_typecheck(program: Program, source_code: str) -> None:
    checker = TypeChecker(source_code)
    checker.check(program)

    if checker.errors:
        for err in checker.formatted_errors():
            print(err)
            print()
    else:
        print("Type check passed.")
        
# ============================================================
# DEMO PROGRAM
# ============================================================

def build_error_program() -> Program:
    """
    Build this invalid program:

        integer main() {
            integer x = 10;
            x = "hello";
            return true;
        }
    """
    main_function = Function(
        return_type="integer",
        name="main",
        parameters=[],
        body=BlockStatement(
            statements=[
                VarDeclaration(
                    var_type="integer",
                    name="x",
                    value=Literal(10, line=2, column=17),
                    line=2,
                    column=5,
                ),
                AssignStatement(
                    name="x",
                    value=Literal("hello", line=3, column=9),
                    line=3,
                    column=5,
                ),
                ReturnStatement(
                    value=Literal(True, line=4, column=12),
                    line=4,
                    column=5,
                ),
            ],
            line=1,
            column=16,
        ),
        line=1,
        column=1,
    )

    return Program(
        functions=[main_function],
        line=1,
        column=1,
    )


def error_source_code() -> str:
    return """integer main() {
    integer x = 10;
    x = "hello";
    return true;
}"""

if __name__ == "__main__":
    source_code = error_source_code()
    program = build_error_program()

    checker = TypeChecker(source_code)
    checker.check(program)

    if checker.errors:
        print("Type check failed:\n")
        for err in checker.formatted_errors():
            print(err)
            print()
    else:
        print("Type check passed.")