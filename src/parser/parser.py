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
        return self.tokens[self.position]

    #Return previous token
    def previous(self) -> Token:
        return self.tokens[self.position-1]

    #Advance position and return previous token
    def advance(self) -> Token:
        if not self.is_at_end():
            self.position+=1
        return self.previous()

    #If token is of specific type; advance position and return previous token.
    #If not of specific type; raise error with argument message.
    def consume(self, token_type: TokenType, message: str) -> Token:
        if self.current().type == token_type:
            return self.advance()
        raise self.error(token_type, message)

    #Return true if current token is of type "EOF"
    def is_at_end(self) -> bool: 
        if self.current().type == TokenType.EOF:
            return True
        return False

    #Return true if current token is of specific type
    def check(self, token_type: TokenType) -> bool:
        if self.current().type == token_type:
            return True
        return False 

    #Return true if current token is of specific types
    def match(self, *types: TokenType) -> bool:
        
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    #Return parser error with costum message
    def error(self, token: Token, message: str) -> ParserError:
        return ParserError(
            f"[line {token.line}, col {token.column}] Error at {token.value!r}: {message}"
        ) 

    def parse(self) -> Program:
        statements = []
        return Program(statements)
