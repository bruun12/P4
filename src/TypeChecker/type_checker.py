from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    Expression,
    ExpressionStatement,
    Grouping,
    IfStatement,
    VarDeclaration,
    Literal,
    Node,
    ParserError,
    Program,
    ReturnStatement,
    Statement,
    Unary,
    Variable,
    WhileStatement,
)

from dataclasses import dataclass

class TypeCheckError(Exception):
    pass

#Base class for all types
@dataclass(frozen=True)
class Type:
    line: int
    column: int

@dataclass(frozen=True)
class IntType(Type):
    pass


@dataclass(frozen=True)
class FloatType(Type):
    pass


@dataclass(frozen=True)
class BoolType(Type):
    pass


@dataclass(frozen=True)
class StringType(Type):
    pass


@dataclass(frozen=True)
class NullType(Type):
    pass


# Reusable singleton-like values for primitive types.
INTEGER = IntType()
FLOAT = FloatType()
BOOLEAN = BoolType()
STRING = StringType()
NULL = NullType()

@dataclass(frozen=True)
class FlowResult:
    guaranteed_returns: bool
    breaks_loop: bool
    unreachable: bool

NO_GUARANTEED_RETURN = FlowResult(
    guaranteed_returns=False,
    breaks_loop=False,
    unreachable=False
)
GUARANTEED_RETURN = FlowResult(
    guaranteed_returns=True,
    breaks_loop=False,
    unreachable=False
)
HAS_BREAK = FlowResult(
    guaranteed_returns=False,
    breaks_loop=True,
    unreachable=False
)
IS_UNREACHABLE = FlowResult(
    guaranteed_returns=False,
    breaks_loop=False,
    unreachable=True
)
#!!Maybe include HAS_NO_BREAK and IS_REACHABLE

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
#   if t == ERROR:
#       return "<error>"


#Helper function when printing error message. 
def type_to_string(t: Type) -> str:
    return 

#Function to return true if type is int or float
def is_numeric(t: Type) -> bool:
    return t == INTEGER or t == FLOAT

#Function to return true if types are the same
def same_type(a: Type, b: Type) -> bool:
    return a == b

#Function to return true if a value is allowed to get assigned to a target variable
def can_assign(target: Type, value: Type) -> bool:
    return 

#Function to check expected result type of an arithmetic operation
def common_numeric_type(left: Type, right: Type) -> Type:
    return 


class TypeEnvironment:
    def __init__(self, parent: "TypeEnvironment | None" = None):
        self.parent = parent
        self.values: dict[str, Type] = {}
        
    def define(self, name: str, type: Type):
        self.values[name] = type


## skal tjekke for: 
### typer (int, float, fs, bool)
### expression
### statements


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