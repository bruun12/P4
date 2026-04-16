from lexer.token import Token, TokenType
from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    Expression,
    ExpressionStatement,
    Grouping,
    IfStatement,
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
class Type:
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



#Helper function when printing error message. 
def type_to_string(t: Type) -> str:
    return

#Function to return true if type is int or float
def is_numeric(t: Type) -> bool:
    return

#Function to return true if types are the same
def same_type(a: Type, b: Type) -> bool:
    return

#Function to return true if a value is allowed to get assigned to a target variable
def can_assign(target: Type, value: Type) -> bool:
    return

#Function to check expected result type of an arithmetic operation
def common_numeric_type(left: Type, right: Type) -> Type:
    return

