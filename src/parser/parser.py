from lexer.token import TokenType, Token
from parser.ASTNodes import (
    Program, 
    BlockStatement, 
    AssignStatement, 
    IfStatement, 
    WhileStatement, 
    ReturnStatement, 
    ExpressionStatement,
    Literal, 
    Variable, 
    Unary, 
    Binary, 
    Grouping,
    Node,
    Statement,
    Expression,
    ParserError
)

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    #Return current token
    def current(self) -> Token:
        return

    #Return previous token
    def previous(self) -> Token:
        return

    #Advance position and return previous token
    def advance(self) -> Token:
        return

    #Advance position and return previous token if token is of specific type.
    #If not of specific type, raise error with argument message.
    def consume(self, token_type: TokenType, message: str) -> Token:
        return

    #Return true if current token is of type "EOF"
    def is_at_end(self) -> bool:
        return

    #Return true if current token is of specific type
    def check(self, token_type: TokenType) -> bool:
        return

    #Return true if current token is of specific types
    def match(self, *types: TokenType) -> bool:
        return

    #Return parser error with costum message
    def error(self, token: Token, message: str) -> ParserError:
        return

    def parse(self) -> Program:
        statements = []
        return Program(statements)
