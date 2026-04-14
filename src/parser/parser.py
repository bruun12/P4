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

    def peek(self) -> Token | None:

        if self.position+1 > len(self.tokens):
            return None
        return self.tokens[self.position+1]

    #Return parser error with costum message
    def error(self, token: Token, message: str) -> ParserError:
        return ParserError(
            f"[line {token.line}, col {token.column}] Error at {token.value!r}: {message}"
        )

    def parse(self) -> Program:
        statements = []

        while not self.is_at_end():
            statements.append(self.statement())
        return Program(statements)

    def statement(self) -> Statement:
        if self.match(TokenType.LCBRACE):
            return self.block_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()

        if self.check(TokenType.IDENTIFIER) and self.peek() == TokenType.ASSIGN:
            return self.assign_statement()

        return self.expression_statement()

    def block_statement(self) -> BlockStatement:
        statements = []
        while not self.check(TokenType.RCBRACE) and self.is_at_end():
            statements.append(self.statement())
        self.comsume(TokenType.RCBRACE)


    def while_statement(self) -> WhileStatement:
        return

    def assign_statement(self) -> AssignStatement:
        return 

    def if_statement(self) -> IfStatement:
        return
    
    def return_statement(self) -> ReturnStatement:
        return
    
    def expression_statement(self) -> ExpressionStatement:
        return
    
    
    
