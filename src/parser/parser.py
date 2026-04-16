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
    VarDeclaration,
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

        if self.check(TokenType.IDENTIFIER) and self.peek().type == TokenType.ASSIGN:
            return self.assign_statement()

        return self.expression_statement()

        

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
        

        if self.check(TokenType.IDENTIFIER) and self.peek and self.peek().type == TokenType.ASSIGN:
            return self.assign_statement()

        return self.expression_statement()

    def var_declaration(self) -> VarDeclaration:
        name = self.advance()
        self.consume()
        

    def block_statement(self) -> BlockStatement:
        statements = []
        while not self.check(TokenType.RCBRACE) and not self.is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RCBRACE, "Expected '}' after")
        return BlockStatement(statements)

    def while_statement(self) -> WhileStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after 'condition'")
        self.consume(TokenType.LCBRACE, "Expected '{' after 'while'")
        body = self.block_statement()
        return WhileStatement(condition, body)

    def assign_statement(self) -> AssignStatement:
        name = self.advance()
        self.consume(TokenType.ASSIGN, "Expected '=' after name")
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return AssignStatement(name.value, value) 

    def if_statement(self) -> IfStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        self.consume(TokenType.LCBRACE, "Expected '{' before if-body")
        then_branch = self.block_statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LCBRACE, "Expected '{' after 'else'")
            else_branch = self.block_statement()
        
        return IfStatement(condition, then_branch, else_branch)

    def return_statement(self) -> ReturnStatement:
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression
        self.consume(TokenType.SEMICOLON, "Excepted ';' after return")
        return ReturnStatement(value)
    
    def expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';'")
        return ExpressionStatement(expr)
    
    
    #Expressions
    def parse_expression(self):
        print(self.current())

        return self.parse_or()

    def parse_or(self): #self.match do self.advance
        left = self.parse_and()
        while self.match(TokenType.OR):
            op = self.previous().value
            left = Binary(left, op, self.parse_and())
        return left
    
    def parse_and(self):
        left = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.previous().value
            left = Binary(left, op, self.parse_equality())
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.previous().value
            left = Binary(left, op, self.parse_comparison())
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.previous().value
            left = Binary(left, op, self.parse_additive())
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().value
            left = Binary(left, op, self.parse_multiplicative())
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.previous().value
            left = Binary(left, op, self.parse_unary())
        return left
    
    def parse_unary(self):
        if self.match(TokenType.NOT):
            op = self.previous().value
            return Unary(op, self.parse_unary())
        return self.parse_primary()
    

    
    def parse_primary(self):
        tok = self.current()

        if self.match(TokenType.INTEGER):
            return Literal(tok.value)
        
        if self.match(TokenType.FLOAT):
            return Literal(tok.value)
        
        if self.match(TokenType.TRUE):
            return Literal(True)
        
        if self.match(TokenType.FALSE):
            return Literal(False)
        
        if self.match(TokenType.STRING):
            return Literal(tok.value)
        
        #Parenteser
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            if not self.match(TokenType.RPAREN):
                raise ParserError("Missing )", tok.line, tok.column)
            return expr

        raise ParserError("Unexpected Token used: '{tok.value}' in expressions", tok.line, tok.column)


