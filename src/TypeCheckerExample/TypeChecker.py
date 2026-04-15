"""
A simple type checker for the AST produced by your parser.

This checker is intentionally beginner-friendly:
- lots of comments
- simple data structures
- no advanced type inference
- easy to extend later

It walks the AST and checks whether expressions and statements
are type-correct.

------------------------------------------------------------
What this checker supports
------------------------------------------------------------

Primitive types:
- int
- float
- bool
- string
- null

Expressions:
- Literal
- Variable
- Grouping
- Unary
- Binary

Statements:
- Program
- BlockStatement
- LetStatement
- AssignStatement
- IfStatement
- WhileStatement
- ReturnStatement
- ExpressionStatement

------------------------------------------------------------
What this checker does NOT do yet
------------------------------------------------------------

- user-defined functions
- function calls
- arrays / lists
- objects / structs
- implicit numeric promotion rules beyond simple cases
- full control-flow analysis
- unreachable code detection

This is a clean starting point you can grow later.
"""

try:
    from parserExample.ASTNodes import (
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
    from parserExample.ASTNodes import (
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
# TYPE ERROR
# ============================================================
# This is the error our checker will raise whenever it finds
# an invalid type usage.
#
# Example:
#   x = "hello";
#   x + 1;
#
# That should fail because string + int is not allowed in
# this small language.
# ============================================================

class TypeCheckError(Exception):
    pass


# ============================================================
# TYPE OBJECTS
# ============================================================
# We represent language types as Python objects.
#
# Why not just use strings like "int" and "bool"?
# You *could*, but using small classes scales better once
# your language grows.
#
# For a small checker, either approach is fine.
# ============================================================

class Type:
    """
    Base class for all types.

    Mostly used so all types share a common parent.
    """
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


# Singleton-like reusable type values.
# This is just convenient so we don't keep writing IntType().
INT = IntType()
FLOAT = FloatType()
BOOL = BoolType()
STRING = StringType()
NULL = NullType()


# ============================================================
# HELPER: DISPLAY TYPES NICELY
# ============================================================
# Error messages are much easier to read if we print types as:
#   int
#   float
#   bool
# instead of:
#   IntType()
#   FloatType()
# ============================================================

def type_name(t: Type) -> str:
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
    return repr(t)


# ============================================================
# TYPE ENVIRONMENT
# ============================================================
# The environment stores variable names and their types.
#
# Example:
#   {
#       "x": int,
#       "flag": bool
#   }
#
# When the checker sees Variable("x"), it looks inside the
# environment to find x's type.
# ============================================================

class TypeEnvironment:
    """
    A scoped variable environment.

    This supports nested blocks:
        {
            let x = 1;
            {
                let y = true;
            }
        }

    Inner scopes can see outer variables.
    Outer scopes cannot see variables declared only inside
    inner scopes.
    """

    def __init__(self, parent: "TypeEnvironment | None" = None):
        self.parent = parent
        self.values: dict[str, Type] = {}

    def define(self, name: str, typ: Type) -> None:
        """
        Create a new variable in the current scope.

        Example:
            let x = 10;
        """
        self.values[name] = typ

    def contains_in_current_scope(self, name: str) -> bool:
        """
        Return True only if the variable is declared in THIS
        scope, not parent scopes.
        """
        return name in self.values

    def assign(self, name: str, typ: Type) -> None:
        """
        Update an existing variable's type location.

        Important:
        This does NOT change the variable's declared type.
        It only finds where the variable lives.

        Example:
            let x = 1;
            x = 2;

        If x exists in an outer scope, assignment should update
        that existing binding, not create a new one.
        """
        if name in self.values:
            self.values[name] = typ
            return

        if self.parent is not None:
            self.parent.assign(name, typ)
            return

        raise TypeCheckError(f"Undefined variable '{name}'.")

    def get(self, name: str) -> Type:
        """
        Look up a variable in the current scope chain.

        This searches:
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
# TYPE COMPATIBILITY HELPERS
# ============================================================
# These small helpers keep the main checker logic cleaner.
# ============================================================

def is_numeric(t: Type) -> bool:
    """
    True for int and float.
    """
    return t == INT or t == FLOAT


def same_type(a: Type, b: Type) -> bool:
    """
    Basic exact equality check between types.

    In a more advanced checker, this could become more complex
    (subtyping, generics, unions, etc.).
    """
    return a == b


def can_assign(target: Type, value: Type) -> bool:
    """
    Return True if a value of type 'value' can be assigned to
    a variable of type 'target'.

    Right now we keep this simple:
    - exact same types are allowed
    - null can only go into null variables

    You can relax or extend this later.
    """
    if target == value:
        return True

    return False


def numeric_result_type(left: Type, right: Type) -> Type:
    """
    Decide the result type of a numeric operation.

    Rules:
    - int + int -> int
    - int + float -> float
    - float + int -> float
    - float + float -> float

    Same rule can be used for -, *, /
    though some languages make / always return float.
    """
    if left == FLOAT or right == FLOAT:
        return FLOAT
    return INT


# ============================================================
# TYPE CHECKER
# ============================================================
# This is the main engine.
#
# It contains two big responsibilities:
#
# 1. check_statement(...)
#    Validates statements.
#
# 2. check_expression(...)
#    Infers / returns the type of an expression.
#
# The two work together recursively.
# ============================================================

class TypeChecker:
    """
    A simple recursive type checker.

    Parameters
    ----------
    expected_return_type:
        Used when checking return statements.

        For example, if later you add functions, you could
        type check a function body with:
            expected_return_type = INT

        Then:
            return 123;    # OK
            return true;   # error

        For now, if you check a top-level program and do not
        want returns, leave this as None.
    """

    def __init__(self, expected_return_type: Type | None = None):
        self.expected_return_type = expected_return_type

    # --------------------------------------------------------
    # Public entry point
    # --------------------------------------------------------

    def check(self, program: Program) -> None:
        """
        Type check the whole program.

        If something is invalid, raise TypeCheckError.
        If no error is raised, the program is type-correct
        under the rules of this checker.
        """
        env = TypeEnvironment()
        self.check_program(program, env)

    # --------------------------------------------------------
    # Program / statement checking
    # --------------------------------------------------------

    def check_program(self, program: Program, env: TypeEnvironment) -> None:
        """
        Check each top-level statement in order.

        Statement order matters because later statements may
        depend on variables introduced earlier.
        """
        for stmt in program.statements:
            self.check_statement(stmt, env)

    def check_statement(self, stmt: Statement, env: TypeEnvironment) -> None:
        """
        Dispatch based on statement type.

        Each statement kind has its own typing rules.
        """

        # ----------------------------------------------------
        # BlockStatement
        # ----------------------------------------------------
        # A block creates a new nested scope.
        #
        # Example:
        # {
        #     let x = 1;
        # }
        #
        # Variables declared inside the block should not leak
        # outside the block.
        # ----------------------------------------------------
        if isinstance(stmt, BlockStatement):
            block_env = TypeEnvironment(parent=env)
            for inner_stmt in stmt.statements:
                self.check_statement(inner_stmt, block_env)
            return

        # ----------------------------------------------------
        # LetStatement
        # ----------------------------------------------------
        # Rule:
        #   let x = expr;
        #
        # We type-check the initializer expression first,
        # then bind x to that type in the current scope.
        # ----------------------------------------------------
        if isinstance(stmt, LetStatement):
            value_type = self.check_expression(stmt.initializer, env)

            # Optional safety rule:
            # forbid duplicate declaration in the same scope
            if env.contains_in_current_scope(stmt.name):
                raise TypeCheckError(
                    f"Variable '{stmt.name}' is already declared in this scope."
                )

            env.define(stmt.name, value_type)
            return

        # ----------------------------------------------------
        # AssignStatement
        # ----------------------------------------------------
        # Rule:
        #   x = expr;
        #
        # We require:
        # - x already exists
        # - expr type matches x's declared type
        # ----------------------------------------------------
        if isinstance(stmt, AssignStatement):
            variable_type = env.get(stmt.name)
            value_type = self.check_expression(stmt.value, env)

            if not can_assign(variable_type, value_type):
                raise TypeCheckError(
                    f"Cannot assign value of type {type_name(value_type)} "
                    f"to variable '{stmt.name}' of type {type_name(variable_type)}."
                )

            # We keep the existing declared type.
            # No need to change env unless your language wants
            # flow-sensitive typing.
            return

        # ----------------------------------------------------
        # IfStatement
        # ----------------------------------------------------
        # Rule:
        #   if (condition) then_branch else else_branch
        #
        # The condition must be bool.
        #
        # Each branch is checked in its own nested scope.
        # This is often the cleanest model for a small language.
        # ----------------------------------------------------
        if isinstance(stmt, IfStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != BOOL:
                raise TypeCheckError(
                    f"If condition must be bool, got {type_name(condition_type)}."
                )

            then_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.then_branch, then_env)

            if stmt.else_branch is not None:
                else_env = TypeEnvironment(parent=env)
                self.check_statement(stmt.else_branch, else_env)

            return

        # ----------------------------------------------------
        # WhileStatement
        # ----------------------------------------------------
        # Rule:
        #   while (condition) body
        #
        # The condition must be bool.
        # The body is checked in a nested scope.
        # ----------------------------------------------------
        if isinstance(stmt, WhileStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != BOOL:
                raise TypeCheckError(
                    f"While condition must be bool, got {type_name(condition_type)}."
                )

            body_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.body, body_env)
            return

        # ----------------------------------------------------
        # ReturnStatement
        # ----------------------------------------------------
        # Rule:
        #   return;
        #   return expr;
        #
        # If expected_return_type is None, we treat top-level
        # return as invalid.
        # ----------------------------------------------------
        if isinstance(stmt, ReturnStatement):
            if self.expected_return_type is None:
                raise TypeCheckError(
                    "Return statement is not allowed here (no expected return type set)."
                )

            # Bare return: return;
            if stmt.value is None:
                if self.expected_return_type != NULL:
                    raise TypeCheckError(
                        f"Expected return type {type_name(self.expected_return_type)}, "
                        f"but got bare return."
                    )
                return

            value_type = self.check_expression(stmt.value, env)

            if not can_assign(self.expected_return_type, value_type):
                raise TypeCheckError(
                    f"Return type mismatch: expected {type_name(self.expected_return_type)}, "
                    f"got {type_name(value_type)}."
                )

            return

        # ----------------------------------------------------
        # ExpressionStatement
        # ----------------------------------------------------
        # Example:
        #   x + 1;
        #
        # We still type-check the expression, even if the result
        # is ignored.
        # ----------------------------------------------------
        if isinstance(stmt, ExpressionStatement):
            self.check_expression(stmt.expression, env)
            return

        raise TypeCheckError(f"Unknown statement node: {stmt!r}")

    # --------------------------------------------------------
    # Expression checking
    # --------------------------------------------------------

    def check_expression(self, expr: Expression, env: TypeEnvironment) -> Type:
        """
        Return the type of an expression.

        This is the heart of the checker for expressions.
        """

        # ----------------------------------------------------
        # Literal
        # ----------------------------------------------------
        # Determine the language type from the Python value
        # stored inside Literal.
        #
        # NOTE:
        # In Python, bool is a subclass of int.
        # So we must check bool BEFORE int.
        # ----------------------------------------------------
        if isinstance(expr, Literal):
            value = expr.value

            if value is None:
                return NULL

            if isinstance(value, bool):
                return BOOL

            if isinstance(value, int):
                return INT

            if isinstance(value, float):
                return FLOAT

            if isinstance(value, str):
                return STRING

            raise TypeCheckError(
                f"Unsupported literal value {value!r} of Python type {type(value).__name__}."
            )

        # ----------------------------------------------------
        # Variable
        # ----------------------------------------------------
        # Look up the variable in the environment.
        # ----------------------------------------------------
        if isinstance(expr, Variable):
            return env.get(expr.name)

        # ----------------------------------------------------
        # Grouping
        # ----------------------------------------------------
        # Parentheses do not change type.
        # They only change parsing structure / precedence.
        # ----------------------------------------------------
        if isinstance(expr, Grouping):
            return self.check_expression(expr.expression, env)

        # ----------------------------------------------------
        # Unary
        # ----------------------------------------------------
        # Supported unary operators:
        #   -x   numeric negation
        #   !x   boolean not
        # ----------------------------------------------------
        if isinstance(expr, Unary):
            right_type = self.check_expression(expr.right, env)

            if expr.operator == "-":
                if not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Unary '-' requires int or float, got {type_name(right_type)}."
                    )
                return right_type

            if expr.operator == "!":
                if right_type != BOOL:
                    raise TypeCheckError(
                        f"Unary '!' requires bool, got {type_name(right_type)}."
                    )
                return BOOL

            raise TypeCheckError(f"Unknown unary operator '{expr.operator}'.")

        # ----------------------------------------------------
        # Binary
        # ----------------------------------------------------
        # This is where most type rules live.
        # ----------------------------------------------------
        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            # ------------------------------------------------
            # Arithmetic: + - * / %
            # ------------------------------------------------
            if op in {"+", "-", "*", "/", "%"}:
                # Special case:
                # allow string + string for concatenation
                if op == "+" and left_type == STRING and right_type == STRING:
                    return STRING

                if not is_numeric(left_type) or not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Operator '{op}' requires numeric operands "
                        f"(or string + string for '+'), got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )

                # If either side is float, result is float.
                # Otherwise int.
                return numeric_result_type(left_type, right_type)

            # ------------------------------------------------
            # Comparisons: < <= > >=
            # ------------------------------------------------
            # For this simple language, we only allow numeric
            # comparison.
            # ------------------------------------------------
            if op in {"<", "<=", ">", ">="}:
                if not is_numeric(left_type) or not is_numeric(right_type):
                    raise TypeCheckError(
                        f"Operator '{op}' requires numeric operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                return BOOL

            # ------------------------------------------------
            # Equality: == !=
            # ------------------------------------------------
            # Simple rule:
            # both sides must have the same type.
            #
            # You could later relax this if you want int == float.
            # ------------------------------------------------
            if op in {"==", "!="}:
                if not same_type(left_type, right_type):
                    raise TypeCheckError(
                        f"Operator '{op}' requires both sides to have the same type, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                return BOOL

            # ------------------------------------------------
            # Logical operators: && ||
            # ------------------------------------------------
            if op in {"&&", "||"}:
                if left_type != BOOL or right_type != BOOL:
                    raise TypeCheckError(
                        f"Operator '{op}' requires bool operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                return BOOL

            raise TypeCheckError(f"Unknown binary operator '{op}'.")

        raise TypeCheckError(f"Unknown expression node: {expr!r}")