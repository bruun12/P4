from dataclasses import dataclass

# -------------------------
# Base marker classes
# -------------------------
class Node:
    pass


class Statement(Node):
    pass


class Expression(Node):
    pass


# -------------------------
# Statement nodes
# -------------------------

@dataclass
class Program(Node):
    # The whole file / whole parsed input
    statements: list


@dataclass
class BlockStatement(Statement):
    # A sequence of statements inside { ... }
    statements: list


@dataclass
class LetStatement(Statement):
    # Example: let x = 5;
    name: str
    initializer: Expression


@dataclass
class AssignStatement(Statement):
    # Example: x = 10;
    name: str
    value: Expression


@dataclass
class IfStatement(Statement):
    # Example:
    # if (condition) { ... } else { ... }
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None


@dataclass
class WhileStatement(Statement):
    # Example: while (condition) { ... }
    condition: Expression
    body: Statement


@dataclass
class ReturnStatement(Statement):
    # Example: return x + 1;
    value: Expression | None


@dataclass
class ExpressionStatement(Statement):
    # Example: foo + 1;
    # This is an expression used as a statement.
    expression: Expression


# -------------------------
# Expression nodes
# -------------------------

@dataclass
class Literal(Expression):
    # Example: 123, 3.14, "hello", true, false, null
    value: object


@dataclass
class Variable(Expression):
    # Example: x
    name: str


@dataclass
class Unary(Expression):
    # Example: -x, !flag
    operator: str
    right: Expression


@dataclass
class Binary(Expression):
    # Example: a + b, x * y, x == y
    left: Expression
    operator: str
    right: Expression


@dataclass
class Grouping(Expression):
    # Example: (x + y)
    expression: Expression


# ============================================================
# PARSER ERROR
# ============================================================

class ParserError(Exception):
    pass
