"""
advanced_typechecker.py

An advanced type checker for the AST shape produced by your parser.

This version is more sophisticated than the beginner version because it adds:

1. A richer type system:
   - int
   - float
   - bool
   - string
   - null
   - nullable[T]

2. Assignment compatibility rules:
   - exact type matches
   - int can be assigned to float
   - null can be assigned to nullable[T]

3. Proper lexical block scoping

4. Return-flow analysis:
   - we track whether statements definitely return
   - this helps detect missing returns in function-like contexts

5. Better helper methods and clearer structure

This is still not a full compiler-grade type checker, but it is much closer
to one than the minimal tutorial version.

--------------------------------------------------------------------
IMPORTANT LIMITATION
--------------------------------------------------------------------
Your AST currently has no function declaration node and no explicit type
annotation syntax.

That means:
- variable types come from initializer inference
- return checking only works if the caller tells the checker what the
  expected return type is

For example, if you later add function nodes, you could type-check a
function body using:
    checker = TypeChecker(expected_return_type=INT, require_all_paths_return=True)

For now, you can still use that manually on a Program or BlockStatement.
"""

try:
    from .ASTNodes import (
        AssignStatement,
        Binary,
        BlockStatement,
        Expression,
        ExpressionStatement,
        Grouping,
        IfStatement,
        LetStatement,
        Literal,
        Program,
        ReturnStatement,
        Statement,
        Unary,
        Variable,
        WhileStatement,
    )
except ImportError:
    from ASTNodes import (
        AssignStatement,
        Binary,
        BlockStatement,
        Expression,
        ExpressionStatement,
        Grouping,
        IfStatement,
        LetStatement,
        Literal,
        Program,
        ReturnStatement,
        Statement,
        Unary,
        Variable,
        WhileStatement,
    )

from dataclasses import dataclass


# ============================================================
# TYPE CHECK ERROR
# ============================================================
# Raised whenever the program violates a typing rule.
# ============================================================

class TypeCheckError(Exception):
    pass


# ============================================================
# TYPE SYSTEM
# ============================================================
# We represent language types as Python dataclasses.
#
# This is nicer than raw strings once the checker gets bigger.
# It lets us represent richer structures like nullable[T].
# ============================================================

class Type:
    """Base class for all types."""
    pass


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


@dataclass(frozen=True)
class NullableType(Type):
    """
    Represents a nullable version of another type.

    Examples:
        nullable[int]
        nullable[string]

    This lets us express "null is allowed here" in a more explicit way
    than just treating null as compatible with everything.
    """
    inner: Type


# Reusable singleton-like values for primitive types.
INT = IntType()
FLOAT = FloatType()
BOOL = BoolType()
STRING = StringType()
NULL = NullType()


# ============================================================
# TYPE DISPLAY HELPERS
# ============================================================
# Makes error messages readable.
# ============================================================

def type_to_string(t: Type) -> str:
    """Convert a type object into a friendly readable string."""
    if t == INT:
        return "int"
    if t == FLOAT:
        return "float"
    if t == BOOL:
        return "bool"
    if t == STRING:
        return "string"
    if t == NULL:
        return "null"
    if isinstance(t, NullableType):
        return f"nullable[{type_to_string(t.inner)}]"
    return repr(t)


def is_numeric(t: Type) -> bool:
    """Return True if the type is int or float."""
    return t == INT or t == FLOAT


def is_nullable_type(t: Type) -> bool:
    """Return True if the type is explicitly nullable."""
    return isinstance(t, NullableType)


def unwrap_nullable(t: Type) -> Type:
    """
    If t is nullable[T], return T.
    Otherwise return t unchanged.

    Useful in places where we want to look at the underlying type.
    """
    if isinstance(t, NullableType):
        return t.inner
    return t


# ============================================================
# TYPE COMPATIBILITY
# ============================================================
# These rules define what assignments and operations are allowed.
# ============================================================

def same_type(a: Type, b: Type) -> bool:
    """
    Structural type equality.

    Because these are dataclasses, == already works well, but wrapping
    the check in a helper gives us one place to change the behavior later.
    """
    return a == b


def can_assign(target: Type, value: Type) -> bool:
    """
    Return True if a value of type 'value' can be assigned to a variable
    or return slot of type 'target'.

    Current rules:
    - exact match: allowed
    - int -> float: allowed
    - null -> nullable[T]: allowed
    - T -> nullable[T]: allowed
    """
    # Exact match always works.
    if same_type(target, value):
        return True

    # Numeric widening: int can be stored in float.
    if target == FLOAT and value == INT:
        return True

    # null may be assigned only to nullable types.
    if isinstance(target, NullableType) and value == NULL:
        return True

    # A non-null T can be assigned into nullable[T].
    if isinstance(target, NullableType) and can_assign(target.inner, value):
        return True

    return False


def common_numeric_type(left: Type, right: Type) -> Type:
    """
    Determine the result type of a numeric expression involving left/right.

    Rules:
    - int + int -> int
    - int + float -> float
    - float + int -> float
    - float + float -> float
    """
    if left == FLOAT or right == FLOAT:
        return FLOAT
    return INT


# ============================================================
# FLOW RESULT
# ============================================================
# Instead of having statement checking return nothing, we return a small
# object that tells us whether control definitely returns from that statement.
#
# This is very useful for:
# - if/else return analysis
# - checking whether all paths return in a function body
# ============================================================

@dataclass(frozen=True)
class FlowResult:
    """
    Result of checking a statement.

    definitely_returns:
        True if execution cannot continue past this statement because all
        possible paths return.

    Example:
        return 1;                    -> definitely_returns = True
        x = 1;                       -> definitely_returns = False
        if (...) return 1; else return 2;
                                    -> definitely_returns = True
    """
    definitely_returns: bool


NO_RETURN = FlowResult(definitely_returns=False)
ALWAYS_RETURNS = FlowResult(definitely_returns=True)


# ============================================================
# TYPE ENVIRONMENT
# ============================================================
# Stores variable names and their declared types, with lexical scoping.
# ============================================================

class TypeEnvironment:
    """
    A nested scope environment.

    Each environment has:
    - a current-scope dictionary
    - an optional parent environment

    Lookup walks outward through parents.
    """

    def __init__(self, parent: "TypeEnvironment | None" = None):
        self.parent = parent
        self.values: dict[str, Type, line] = {}

    def define(self, name: str, typ: Type) -> None:
        """
        Define a variable in the current scope.

        Example:
            let x = 10;
        """
        self.values[name] = typ

    def contains_in_current_scope(self, name: str) -> bool:
        """
        True only if the variable exists in THIS scope, not parent scopes.
        """
        return name in self.values

    def get(self, name: str) -> Type:
        """
        Look up a variable type by name.

        Search order:
        - current scope
        - parent scope
        - parent's parent
        - ...
        """
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise TypeCheckError(f"Undefined variable '{name}'.")



# ============================================================
# TYPE CHECKER
# ============================================================

class TypeChecker:
    """
    Advanced type checker.

    Parameters
    ----------
    expected_return_type:
        If not None, return statements are allowed and must match this type.

    require_all_paths_return:
        If True, then after checking a whole program/body, the checker will
        require that control cannot fall off the end.

        This is mostly useful when checking function bodies.
    """

    def __init__(
        self,
        expected_return_type: Type | None = None,
        require_all_paths_return: bool = False,
    ):
        self.expected_return_type = expected_return_type
        self.require_all_paths_return = require_all_paths_return

    # --------------------------------------------------------
    # Public entry point
    # --------------------------------------------------------

    def check(self, program: Program) -> None:
        """
        Type-check the whole program.

        If the program is invalid, raise TypeCheckError.
        If not, return successfully.
        """
        env = TypeEnvironment()
        flow = self.check_program(program, env)

        # If we are simulating a function body and every path is required
        # to return, then the final flow result must say so.
        if self.require_all_paths_return and not flow.definitely_returns:
            if self.expected_return_type is None:
                raise TypeCheckError(
                    "Internal checker configuration error: "
                    "require_all_paths_return=True but no expected return type set."
                )
            raise TypeCheckError(
                f"Not all control paths return a value of type "
                f"{type_to_string(self.expected_return_type)}."
            )

    # --------------------------------------------------------
    # Program checking
    # --------------------------------------------------------

    def check_program(self, program: Program, env: TypeEnvironment) -> FlowResult:
        """
        Check all top-level statements in order.

        Flow behavior:
        - if a statement definitely returns, everything after it is unreachable
          in a strict compiler.
        - here we simply stop and return ALWAYS_RETURNS.

        You could later upgrade this to also report unreachable code.
        """
        for stmt in program.statements:
            flow = self.check_statement(stmt, env)
            if flow.definitely_returns:
                return ALWAYS_RETURNS

        return NO_RETURN

    # --------------------------------------------------------
    # Statement checking
    # --------------------------------------------------------

    def check_statement(self, stmt: Statement, env: TypeEnvironment) -> FlowResult:
        """
        Check one statement and return flow information.
        """

        # ====================================================
        # BLOCK STATEMENT
        # ====================================================
        # A block creates a child scope.
        #
        # Important:
        # If the block has no statements, the for-loop runs zero times,
        # which is perfectly valid.
        #
        # Flow rule:
        # - if any statement definitely returns, then the whole block
        #   definitely returns from that point onward
        # ====================================================
        if isinstance(stmt, BlockStatement):
            block_env = TypeEnvironment(parent=env)

            for inner_stmt in stmt.statements:
                flow = self.check_statement(inner_stmt, block_env)
                if flow.definitely_returns:
                    return ALWAYS_RETURNS

            return NO_RETURN

        # ====================================================
        # LET STATEMENT
        # ====================================================
        # Syntax:
        #   let x = initializer;
        #
        # We infer x's type from the initializer.
        # ====================================================
        if isinstance(stmt, LetStatement):
            init_type = self.check_expression(stmt.initializer, env)

            if env.contains_in_current_scope(stmt.name):
                raise TypeCheckError(
                    f"Variable '{stmt.name}' is already declared in this scope."
                )

            env.define(stmt.name, init_type)
            return NO_RETURN

        # ====================================================
        # ASSIGN STATEMENT
        # ====================================================
        # Syntax:
        #   x = value;
        #
        # Rules:
        # - x must already exist
        # - value type must be assignable to x's declared type
        # ====================================================
        if isinstance(stmt, AssignStatement):
            target_type = env.get(stmt.name)
            value_type = self.check_expression(stmt.value, env)

            if not can_assign(target_type, value_type):
                raise TypeCheckError(
                    f"Cannot assign value of type {type_to_string(value_type)} "
                    f"to variable '{stmt.name}' of type {type_to_string(target_type)}."
                )

            return NO_RETURN

        # ====================================================
        # IF STATEMENT
        # ====================================================
        # Syntax:
        #   if (condition) then_branch else else_branch
        #
        # Rules:
        # - condition must be bool
        # - then / else are checked in child scopes
        #
        # Flow rule:
        # - if both branches definitely return, then the if-statement
        #   definitely returns
        # - if there is no else branch, it cannot definitely return
        # ====================================================
        if isinstance(stmt, IfStatement):
            cond_type = self.check_expression(stmt.condition, env)

            if cond_type != BOOL:
                raise TypeCheckError(
                    f"If condition must be bool, got {type_to_string(cond_type)}."
                )

            then_env = TypeEnvironment(parent=env)
            then_flow = self.check_statement(stmt.then_branch, then_env)

            if stmt.else_branch is None:
                return NO_RETURN

            else_env = TypeEnvironment(parent=env)
            else_flow = self.check_statement(stmt.else_branch, else_env)

            if then_flow.definitely_returns and else_flow.definitely_returns:
                return ALWAYS_RETURNS

            return NO_RETURN

        # ====================================================
        # WHILE STATEMENT
        # ====================================================
        # Syntax:
        #   while (condition) body
        #
        # Rules:
        # - condition must be bool
        #
        # Flow analysis note:
        # Even if the loop body returns, we generally do NOT say the whole
        # while definitely returns, because the loop may execute zero times.
        #
        # Example:
        #   while (false) { return 1; }
        #
        # So the safe rule is:
        #   while never definitely returns
        # ====================================================
        if isinstance(stmt, WhileStatement):
            cond_type = self.check_expression(stmt.condition, env)

            if cond_type != BOOL:
                raise TypeCheckError(
                    f"While condition must be bool, got {type_to_string(cond_type)}."
                )

            body_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.body, body_env)
            return NO_RETURN

        # ====================================================
        # RETURN STATEMENT
        # ====================================================
        # Syntax:
        #   return;
        #   return value;
        #
        # Rules:
        # - allowed only if expected_return_type is set
        # - bare return is only valid if expected return type is null
        # - returned expression must be assignable to expected type
        #
        # Flow:
        # - return definitely returns
        # ====================================================
        if isinstance(stmt, ReturnStatement):
            if self.expected_return_type is None:
                raise TypeCheckError(
                    "Return statement is not allowed here because no expected "
                    "return type was provided to the checker."
                )

            # Bare return: return;
            if stmt.value is None:
                if not can_assign(self.expected_return_type, NULL):
                    raise TypeCheckError(
                        f"Bare return is not compatible with expected return type "
                        f"{type_to_string(self.expected_return_type)}."
                    )
                return ALWAYS_RETURNS

            value_type = self.check_expression(stmt.value, env)

            if not can_assign(self.expected_return_type, value_type):
                raise TypeCheckError(
                    f"Return type mismatch: expected "
                    f"{type_to_string(self.expected_return_type)}, got "
                    f"{type_to_string(value_type)}."
                )

            return ALWAYS_RETURNS

        # ====================================================
        # EXPRESSION STATEMENT
        # ====================================================
        # Syntax:
        #   expression;
        #
        # We still type-check the expression even though its value is discarded.
        # ====================================================
        if isinstance(stmt, ExpressionStatement):
            self.check_expression(stmt.expression, env)
            return NO_RETURN

        raise TypeCheckError(f"Unknown statement node: {stmt!r}")

    # --------------------------------------------------------
    # Expression checking
    # --------------------------------------------------------

    def check_expression(self, expr: Expression, env: TypeEnvironment) -> Type:
        """
        Infer and return the type of an expression.
        """

        # ====================================================
        # LITERAL
        # ====================================================
        # We inspect the Python value inside Literal(value) and map it
        # to one of our language types.
        #
        # IMPORTANT:
        # In Python, bool is a subclass of int.
        # So we must check bool BEFORE int.
        # ====================================================
        if isinstance(expr, Literal):
            value = expr.value

            if value is None:
                return NULL

            if isinstance(value, bool):
                return BoolType(expr.line, expr.column)

            if isinstance(value, int):
                return INT

            if isinstance(value, float):
                return FLOAT

            if isinstance(value, str):
                return STRING

            raise TypeCheckError(
                f"Unsupported literal value {value!r} "
                f"of Python type {type(value).__name__}."
            )

        # ====================================================
        # VARIABLE
        # ====================================================
        # Look up the variable's declared type from the environment.
        # ====================================================
        if isinstance(expr, Variable):
            return env.get(expr.name)

        # ====================================================
        # GROUPING
        # ====================================================
        # Parentheses do not change the type; they only affect parsing.
        # ====================================================
        if isinstance(expr, Grouping):
            return self.check_expression(expr.expression, env)

        # ====================================================
        # UNARY
        # ====================================================
        # Supported operators:
        #   -x   numeric negation
        #   !x   boolean negation
        #
        # Rules:
        # - '-' requires int or float; returns same type
        # - '!' requires bool; returns bool
        # ====================================================
        if isinstance(expr, Unary):
            right_type = self.check_expression(expr.right, env)

            if expr.operator == "-":
                if not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Unary '-' requires int or float, got "
                        f"{type_to_string(right_type)}."
                    )
                return right_type

            if expr.operator == "!":
                if right_type != BOOL:
                    raise TypeCheckError(
                        f"Unary '!' requires bool, got "
                        f"{type_to_string(right_type)}."
                    )
                return BOOL

            raise TypeCheckError(f"Unknown unary operator '{expr.operator}'.")

        # ====================================================
        # BINARY
        # ====================================================
        # This is where most expression typing rules live.
        # ====================================================
        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            # ------------------------------------------------
            # ARITHMETIC
            # ------------------------------------------------
            # Operators:
            #   + - * / %
            #
            # Rules:
            # - string + string -> string
            # - numeric op numeric -> numeric result
            #
            # Note:
            # We do not allow string * int or similar in this language.
            # ------------------------------------------------
            if op in {"+", "-", "*", "/", "%"}:
                # Special case for string concatenation
                if op == "+" and left_type == STRING and right_type == STRING:
                    return STRING

                if not is_numeric(left_type) or not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Operator '{op}' requires numeric operands "
                        f"(except string + string), got "
                        f"{type_to_string(left_type)} and "
                        f"{type_to_string(right_type)}."
                    )

                # Division policy:
                # For a more advanced language, you might choose:
                #   int / int -> float
                # But here we keep the same promotion rule used by the
                # other numeric operators.
                return common_numeric_type(left_type, right_type)

            # ------------------------------------------------
            # COMPARISON
            # ------------------------------------------------
            # Operators:
            #   < <= > >=
            #
            # Rules:
            # - both sides must be numeric
            # - result is bool
            # ------------------------------------------------
            if op in {"<", "<=", ">", ">="}:
                if not is_numeric(left_type) or not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Operator '{op}' requires numeric operands, got "
                        f"{type_to_string(left_type)} and "
                        f"{type_to_string(right_type)}."
                    )
                return BOOL

            # ------------------------------------------------
            # EQUALITY
            # ------------------------------------------------
            # Operators:
            #   == !=
            #
            # More advanced than the beginner version:
            # - exact type match is allowed
            # - int and float may be compared
            # - nullable[T] may be compared with null
            # - T may be compared with nullable[T]
            #
            # This is still intentionally conservative.
            # ------------------------------------------------
            if op in {"==", "!="}:
                if self.are_comparable_for_equality(left_type, right_type):
                    return BOOL

                raise TypeCheckError(
                    f"Operator '{op}' cannot compare values of type "
                    f"{type_to_string(left_type)} and "
                    f"{type_to_string(right_type)}."
                )

            # ------------------------------------------------
            # LOGICAL
            # ------------------------------------------------
            # Operators:
            #   && ||
            #
            # Both sides must be bool.
            # ------------------------------------------------
            if op in {"&&", "||"}:
                if left_type != BOOL or right_type != BOOL:
                    raise TypeCheckError(
                        f"Operator '{op}' requires bool operands, got "
                        f"{type_to_string(left_type)} and "
                        f"{type_to_string(right_type)}."
                    )
                return BOOL

            raise TypeCheckError(f"Unknown binary operator '{op}'.")

        raise TypeCheckError(f"Unknown expression node: {expr!r}")

    # --------------------------------------------------------
    # Equality comparability helper
    # --------------------------------------------------------

    def are_comparable_for_equality(self, left: Type, right: Type) -> bool:
        """
        Return True if two types may be compared with == or !=.

        Rules:
        - same types are comparable
        - int and float are comparable
        - nullable[T] and null are comparable
        - T and nullable[T] are comparable if T fits inside nullable[T]

        This is stricter than some languages, but more flexible than
        the beginner checker.
        """
        if same_type(left, right):
            return True

        # int == float and float == int
        if is_numeric(left) and is_numeric(right):
            return True

        # nullable[T] == null
        if isinstance(left, NullableType) and right == NULL:
            return True

        if isinstance(right, NullableType) and left == NULL:
            return True

        # T == nullable[T] or nullable[T] == T
        if isinstance(left, NullableType) and can_assign(left, right):
            return True

        if isinstance(right, NullableType) and can_assign(right, left):
            return True

        return False