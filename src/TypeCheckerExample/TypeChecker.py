from __future__ import annotations

from dataclasses import dataclass


# ============================================================
# MOCK AST NODES
# ============================================================
# These are the same kinds of nodes your original checker used.
# The checker below is written against these node shapes.
# ============================================================

class Node:
    """Base class for every AST node."""
    pass


class Statement(Node):
    """Base class for statements."""
    pass


class Expression(Node):
    """Base class for expressions."""
    pass


@dataclass
class Program(Node):
    statements: list[Statement]


@dataclass
class BlockStatement(Statement):
    statements: list[Statement]
    line: int
    column: int


@dataclass
class VarDeclaration(Statement):
    name: str
    declared_type: str
    initializer: Expression
    line: int
    column: int


@dataclass
class AssignStatement(Statement):
    name: str
    value: Expression
    line: int
    column: int


@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None
    line: int
    column: int


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Statement
    line: int
    column: int


@dataclass
class ReturnStatement(Statement):
    value: Expression | None
    line: int
    column: int


@dataclass
class BreakStatement(Statement):
    line: int
    column: int


@dataclass
class ExpressionStatement(Statement):
    expression: Expression
    line: int
    column: int


@dataclass
class Literal(Expression):
    value: object
    line: int
    column: int


@dataclass
class Variable(Expression):
    name: str
    line: int
    column: int


@dataclass
class Unary(Expression):
    operator: str
    right: Expression
    line: int
    column: int


@dataclass
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression
    line: int
    column: int


@dataclass
class Grouping(Expression):
    expression: Expression
    line: int
    column: int


# ============================================================
# TYPE OBJECTS
# ============================================================
# These are tiny value objects representing language types.
# They are immutable and shared via singleton instances below.
# ============================================================

class Type:
    """Base type object."""
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
    """
    Special internal type used after an error is found.

    This lets the checker continue and report more errors
    instead of crashing or cascading too aggressively.
    """
    pass


INTEGER = IntegerType()
FLOAT = FloatType()
BOOLEAN = BooleanType()
STRING = StringType()
NULL = NullType()
ERROR = ErrorType()


# ============================================================
# CONTROL-FLOW RESULT
# ============================================================
# The type checker also tracks statement flow. This is useful
# for:
#   - detecting unreachable code
#   - understanding returns
#   - handling break statements
#
# definitely_returns:
#   True when the statement definitely returns on all paths.
#
# breaks_loop:
#   True when the statement causes a break from the nearest loop.
#
# unreachable:
#   This can be used by callers to flag dead paths if needed.
#   In this checker, most unreachable reporting is done while
#   iterating statement sequences.
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
# TYPE ERROR + ERROR FORMATTING
# ============================================================

class TypeCheckError(Exception):
    """
    Structured type-checking error.

    We store the message and exact source position so the error
    can later be shown with a caret under the offending code.
    """
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column


def format_type_error(error: TypeCheckError, source_lines: list[str]) -> str:
    """
    Format a single error with source context.

    Example:

    Type error: Cannot assign string to integer.
     --> line 3, col 11
      |
    3 | x = y + "hello";
      |           ^
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
# TYPE ENVIRONMENT
# ============================================================
# The environment is a chain of scopes.
#
# Each scope contains variables defined in that block. A lookup
# first checks the current scope, then walks upward to parents.
# ============================================================

class TypeEnvironment:
    def __init__(self, parent: TypeEnvironment | None = None):
        self.parent = parent
        self.values: dict[str, Type] = {}

    def define(self, name: str, typ: Type) -> None:
        """Define a new variable in the current scope."""
        self.values[name] = typ

    def contains_in_current_scope(self, name: str) -> bool:
        """Check whether a variable name is already declared here."""
        return name in self.values

    def get(self, name: str) -> Type:
        """
        Look up a variable, searching outward through parent scopes.

        Raises:
            TypeCheckError: if the variable does not exist.
        """
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise TypeCheckError(f"Undefined variable '{name}'.", 0, 0)


# ============================================================
# TYPE HELPERS
# ============================================================

def type_name(t: Type) -> str:
    """Convert an internal type object into a readable name."""
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
    return repr(t)


def parse_type_name(name: str) -> Type:
    """
    Convert a declared type string into its internal Type object.

    Raises:
        TypeCheckError: if the declared type name is unknown.
    """
    if name == "integer":
        return INTEGER
    if name == "float":
        return FLOAT
    if name == "boolean":
        return BOOLEAN
    if name == "string":
        return STRING
    if name == "null":
        return NULL

    raise TypeCheckError(f"Unknown declared type '{name}'.", 0, 0)


def is_numeric(t: Type) -> bool:
    """True for integer and float."""
    return t == INTEGER or t == FLOAT


def can_assign(target: Type, value: Type) -> bool:
    """
    Decide whether a value of one type can be assigned to another.

    Supported widening:
      integer -> float
    """
    if target == value:
        return True

    if target == FLOAT and value == INTEGER:
        return True

    return False


def numeric_result_type(left: Type, right: Type) -> Type:
    """
    Result type for a numeric binary operator.

    If either side is float, the result is float.
    Otherwise it is integer.
    """
    if left == FLOAT or right == FLOAT:
        return FLOAT
    return INTEGER


# ============================================================
# TYPE CHECKER
# ============================================================
# This class performs the real work.
#
# Design goals of this rewrite:
#   - clean separation between statement and expression checks
#   - lots of comments and small helpers
#   - continue after errors so multiple diagnostics are reported
#   - public utility methods for common use cases
# ============================================================

class TypeChecker:
    def __init__(self, source_code: str, expected_return_type: Type | None = None):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.expected_return_type = expected_return_type
        self.errors: list[TypeCheckError] = []

    # --------------------------------------------------------
    # Error helpers
    # --------------------------------------------------------

    def reset(self) -> None:
        """Clear any previously collected errors."""
        self.errors.clear()

    def make_error(self, node: Node, message: str) -> TypeCheckError:
        """
        Create a TypeCheckError from a node.

        This assumes the node has line/column attributes, which
        all concrete AST nodes in this file do.
        """
        return TypeCheckError(message, node.line, node.column)

    def report(self, node: Node, message: str) -> None:
        """Record an error but do not stop checking."""
        self.errors.append(self.make_error(node, message))

    def has_errors(self) -> bool:
        """Convenience method for checking whether errors exist."""
        return len(self.errors) > 0

    def formatted_errors(self) -> list[str]:
        """Return all errors already formatted for display."""
        return [format_type_error(err, self.source_lines) for err in self.errors]

    # --------------------------------------------------------
    # Public entry points
    # --------------------------------------------------------

    def check(self, program: Program) -> FlowResult:
        """
        Type-check a full program from a fresh top-level scope.

        Returns:
            FlowResult for the program as a whole.
        """
        self.reset()
        env = TypeEnvironment()
        return self.check_program(program, env)

    def check_program(self, program: Program, env: TypeEnvironment) -> FlowResult:
        """
        Check all top-level statements in order.

        We also detect unreachable statements after a guaranteed
        terminal flow (return/break outside loop context).
        """
        saw_terminal_flow = False

        for stmt in program.statements:
            if saw_terminal_flow:
                self.report(stmt, "Unreachable statement.")
                continue

            flow = self.check_statement(stmt, env, inside_loop=False)

            if flow.unreachable:
                self.report(stmt, "Unreachable statement.")

            if flow.breaks_loop:
                # A top-level break has nowhere valid to break to.
                self.report(stmt, "'break' used outside of a loop.")

            if flow.definitely_returns or flow.breaks_loop:
                saw_terminal_flow = True

        return NO_FLOW

    # --------------------------------------------------------
    # Statement checking
    # --------------------------------------------------------

    def check_statement(
        self,
        stmt: Statement,
        env: TypeEnvironment,
        inside_loop: bool,
    ) -> FlowResult:
        """
        Check a single statement.

        The returned FlowResult tells the caller how this
        statement behaves with respect to control flow.
        """

        # ----------------------------------------------------
        # BlockStatement
        # ----------------------------------------------------
        # A block creates a new nested scope. Variables declared
        # inside the block do not leak outward.
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
        # Example:
        #   integer x = 10;
        #
        # Rules:
        #   - the declared type name must be known
        #   - duplicate declaration in the same scope is an error
        #   - initializer type must be assignable to declared type
        # ----------------------------------------------------
        if isinstance(stmt, VarDeclaration):
            try:
                declared_type = parse_type_name(stmt.declared_type)
            except TypeCheckError:
                self.report(stmt, f"Unknown declared type '{stmt.declared_type}'.")
                declared_type = ERROR

            initializer_type = self.check_expression(stmt.initializer, env)

            if env.contains_in_current_scope(stmt.name):
                self.report(
                    stmt,
                    f"Variable '{stmt.name}' is already declared in this scope."
                )

            if (
                declared_type != ERROR
                and initializer_type != ERROR
                and not can_assign(declared_type, initializer_type)
            ):
                self.report(
                    stmt.initializer,
                    f"Cannot initialize variable '{stmt.name}' of type "
                    f"{type_name(declared_type)} with value of type "
                    f"{type_name(initializer_type)}."
                )

            # We still define the variable if the declared type is valid.
            # This reduces secondary "undefined variable" noise later.
            if declared_type != ERROR:
                env.define(stmt.name, declared_type)

            return NO_FLOW

        # ----------------------------------------------------
        # AssignStatement
        # ----------------------------------------------------
        # Example:
        #   x = 42;
        #
        # Rules:
        #   - variable must already exist
        #   - assigned value type must be assignable to variable type
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
        # Rules:
        #   - condition must be boolean
        #   - each branch is checked in its own nested scope
        #   - if both branches definitely return, the whole if returns
        #   - if both branches break, the whole if breaks
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

            definitely_returns = (
                then_flow.definitely_returns and else_flow.definitely_returns
            )
            breaks_loop = (
                then_flow.breaks_loop and else_flow.breaks_loop
            )

            return FlowResult(
                definitely_returns=definitely_returns,
                breaks_loop=breaks_loop,
                unreachable=False,
            )

        # ----------------------------------------------------
        # WhileStatement
        # ----------------------------------------------------
        # Rules:
        #   - condition must be boolean
        #   - body is checked with inside_loop=True
        #   - break inside the body is considered consumed by the loop
        #
        # This checker does not try to prove infinite loops or
        # guaranteed returns through while loops.
        # ----------------------------------------------------
        if isinstance(stmt, WhileStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != ERROR and condition_type != BOOLEAN:
                self.report(
                    stmt.condition,
                    f"While condition must be boolean, got {type_name(condition_type)}."
                )

            body_env = TypeEnvironment(parent=env)
            _body_flow = self.check_statement(stmt.body, body_env, inside_loop=True)

            return NO_FLOW

        # ----------------------------------------------------
        # ReturnStatement
        # ----------------------------------------------------
        # Rules:
        #   - not allowed unless a return type is expected
        #   - this language version requires a value on return
        #   - returned expression must match expected return type
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
                    f"Return type mismatch: expected "
                    f"{type_name(self.expected_return_type)}, got {type_name(value_type)}."
                )

            return RETURNS

        # ----------------------------------------------------
        # BreakStatement
        # ----------------------------------------------------
        # Rules:
        #   - valid only inside a loop
        # ----------------------------------------------------
        if isinstance(stmt, BreakStatement):
            if not inside_loop:
                self.report(stmt, "'break' used outside of a loop.")
            return BREAKS

        # ----------------------------------------------------
        # ExpressionStatement
        # ----------------------------------------------------
        # Expression statements are checked only for type validity.
        # ----------------------------------------------------
        if isinstance(stmt, ExpressionStatement):
            self.check_expression(stmt.expression, env)
            return NO_FLOW

        # ----------------------------------------------------
        # Unknown statement
        # ----------------------------------------------------
        self.report(stmt, f"Unknown statement node: {stmt!r}")
        return NO_FLOW

    # --------------------------------------------------------
    # Expression checking
    # --------------------------------------------------------

    def check_expression(self, expr: Expression, env: TypeEnvironment) -> Type:
        """
        Compute the type of an expression.

        On error, report the issue and return ERROR so checking can continue.
        """

        # ----------------------------------------------------
        # Literal
        # ----------------------------------------------------
        if isinstance(expr, Literal):
            value = expr.value

            if value is None:
                return NULL

            # Important:
            # In Python, bool is a subclass of int, so bool must be
            # checked before int or True/False would look like integers.
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

        # ----------------------------------------------------
        # Variable
        # ----------------------------------------------------
        if isinstance(expr, Variable):
            try:
                return env.get(expr.name)
            except TypeCheckError:
                self.report(expr, f"Undefined variable '{expr.name}'.")
                return ERROR

        # ----------------------------------------------------
        # Grouping
        # ----------------------------------------------------
        if isinstance(expr, Grouping):
            return self.check_expression(expr.expression, env)

        # ----------------------------------------------------
        # Unary
        # ----------------------------------------------------
        # Supported operators:
        #   - numeric negation: -
        #   - logical not: !
        # ----------------------------------------------------
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

        # ----------------------------------------------------
        # Binary
        # ----------------------------------------------------
        # Supported categories:
        #   - arithmetic: + - * / %
        #   - comparison: < <= > >=
        #   - equality: == !=
        #   - logical: && ||
        # ----------------------------------------------------
        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            if left_type == ERROR or right_type == ERROR:
                return ERROR

            # Arithmetic operators
            if op in {"+", "-", "*", "/", "%"}:
                # string + string is allowed as concatenation
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

            # Comparison operators
            if op in {"<", "<=", ">", ">="}:
                if not is_numeric(left_type) or not is_numeric(right_type):
                    self.report(
                        expr,
                        f"Operator '{op}' requires numeric operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Equality operators
            if op in {"==", "!="}:
                if left_type != right_type:
                    self.report(
                        expr,
                        f"Operator '{op}' requires both sides to have the same type, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Logical operators
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

        # ----------------------------------------------------
        # Unknown expression
        # ----------------------------------------------------
        self.report(expr, f"Unknown expression node: {expr!r}")
        return ERROR

    # --------------------------------------------------------
    # Extra helper / convenience methods
    # --------------------------------------------------------

    def infer_expression_type(
        self,
        expr: Expression,
        env: TypeEnvironment | None = None,
    ) -> Type:
        """
        Infer the type of a single expression.

        This is useful if you want to type-check expressions outside
        a full program. Errors are still collected in self.errors.
        """
        if env is None:
            env = TypeEnvironment()
        return self.check_expression(expr, env)

    def collect_errors_as_text(self) -> str:
        """
        Join all formatted errors into a single string.
        Handy for testing or CLI output.
        """
        return "\n\n".join(self.formatted_errors())


# ============================================================
# EXTRA TOP-LEVEL FUNCTIONS
# ============================================================
# These are the extra public functions I added because your
# message ended after “includes functions:”.
# They make the checker easier to reuse from other code.
# ============================================================

def check_program_types(
    program: Program,
    source_code: str,
    expected_return_type: Type | None = None,
) -> tuple[TypeChecker, FlowResult]:
    """
    Type-check a program and return both the checker and flow result.

    This is useful when the caller wants:
      - the flow information
      - the accumulated errors
      - access to formatting helpers
    """
    checker = TypeChecker(source_code, expected_return_type=expected_return_type)
    flow = checker.check(program)
    return checker, flow


def collect_type_errors(
    program: Program,
    source_code: str,
    expected_return_type: Type | None = None,
) -> list[TypeCheckError]:
    """
    Type-check a program and return the raw TypeCheckError objects.
    """
    checker, _ = check_program_types(
        program,
        source_code,
        expected_return_type=expected_return_type,
    )
    return checker.errors


def typecheck_and_format(
    program: Program,
    source_code: str,
    expected_return_type: Type | None = None,
) -> list[str]:
    """
    Type-check a program and return already formatted diagnostics.
    """
    checker, _ = check_program_types(
        program,
        source_code,
        expected_return_type=expected_return_type,
    )
    return checker.formatted_errors()


def has_type_errors(
    program: Program,
    source_code: str,
    expected_return_type: Type | None = None,
) -> bool:
    """
    Quick yes/no function for callers that only care whether the
    program passed type-checking.
    """
    checker, _ = check_program_types(
        program,
        source_code,
        expected_return_type=expected_return_type,
    )
    return checker.has_errors()


def infer_expression_type(
    expr: Expression,
    source_code: str = "",
    env: TypeEnvironment | None = None,
) -> tuple[Type, list[TypeCheckError]]:
    """
    Infer the type of one expression outside a full program.

    Returns:
        (inferred_type, errors)
    """
    checker = TypeChecker(source_code)
    inferred = checker.infer_expression_type(expr, env=env)
    return inferred, checker.errors


# ============================================================
# DEMO SOURCE + DEMO PROGRAM
# ============================================================

source_code = """integer x = 10;
if (x > 5) {
    x = y + 1;
    return x;
} else {
    return "b";
}"""


program = Program(statements=[
    VarDeclaration(
        name="x",
        declared_type="integer",
        line=1,
        column=1,
        initializer=Literal(
            value=10,
            line=1,
            column=13,
        ),
    ),

    IfStatement(
        line=2,
        column=1,

        condition=Binary(
            left=Variable("x", line=2, column=5),
            operator=">",
            right=Literal(5, line=2, column=9),
            line=2,
            column=7,
        ),

        then_branch=BlockStatement(
            line=2,
            column=12,
            statements=[
                AssignStatement(
                    name="x",
                    line=3,
                    column=5,
                    value=Binary(
                        left=Variable("y", line=3, column=9),
                        operator="+",
                        right=Literal(1, line=3, column=13),
                        line=3,
                        column=11,
                    ),
                ),
                ReturnStatement(
                    value=Variable("x", line=4, column=12),
                    line=4,
                    column=5,
                ),
            ],
        ),

        else_branch=BlockStatement(
            line=5,
            column=8,
            statements=[
                ReturnStatement(
                    value=Literal("b", line=6, column=12),
                    line=6,
                    column=5,
                ),
            ],
        ),
    ),
])


# ============================================================
# RUNNER
# ============================================================

def run_typecheck(
    program: Program,
    source_code: str,
    expected_return_type: Type | None = None,
) -> None:
    """
    Small runner for manual testing.
    """
    checker, flow = check_program_types(
        program,
        source_code,
        expected_return_type=expected_return_type,
    )

    if checker.errors:
        for err_text in checker.formatted_errors():
            print(err_text)
            print()
    else:
        print("Type check passed.")
        print("Flow result:", flow)


if __name__ == "__main__":
    run_typecheck(program, source_code, expected_return_type=INTEGER)