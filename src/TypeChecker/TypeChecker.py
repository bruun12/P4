from lexer.token import Token, TokenType
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
IntType()
FloatType()
BoolType()
StringType()
NullType()

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

#Helper function when printing error message. 
def type_to_string(t: Type) -> str:
    return 

#Function to return true if type is int or float
def is_numeric(t: Type) -> bool:
    return t == TokenType.INT or t == TokenType.FLOAT

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


