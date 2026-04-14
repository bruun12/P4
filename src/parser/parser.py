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
    

    #Expressions
    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.match(TokenType.OR):
            op = self.advance().value
            left = Binary(left, op, self.parse_and())
        return left
    
    def parse_and(self):
        left = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.advance().value
            left = Binary(left, op, self.parse_equality())
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.advance().value
            left = Binary(left, op, self.parse_comparison())
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.advance.value
            left = Binary(left, op, self.parse_additive())
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance.value
            left = Binary(left, op, self.parse_multiplicative())
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.advance.value
            left = Binary(left, op, self.parse_unary())
        return left
    
    def parse_unary(self):
        if self.match(TokenType.NOT):
            op = self.advance().value
            return Unary(op, self.parse_unary())
        return self.parse_primary()
    
    def parse_primary(self):
        tok = self.current()

        if tok.type == TokenType.INTEGER:
            self.advance
            return Literal(tok.value)
        
        if tok.type == TokenType.FLOAT:
            self.advance
            return Literal(tok.value)
        
        if tok.type == TokenType.TRUE:
            self.advance
            return Literal(True)
        
        if tok.type == TokenType.FALSE:
            self.advance
            return Literal(False)
        
        if tok.type == TokenType.STRING:
            self.advance
            return Literal(tok.value)
        
        #Parenteser
        if tok.type == TokenType.LPAREN:
            self.advance
            expr = self.parse_expression()
            self.check(TokenType.RPAREN)
            return expr
      


        raise ParserError("Unexpected Token used: '{tok.value}' in expressions", tok.line, tok.column)
    


