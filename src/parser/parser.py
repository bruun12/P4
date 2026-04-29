from lexer.token import Token, TokenType
from error_handling import ParserError, ErrorCode
from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    ExpressionStatement,
    IfStatement,
    Literal,
    Program,
    ReturnStatement,
    Statement,
    Unary,
    Variable,
    WhileStatement,
    VarDeclaration,
    Function,
    Parameter,
    ArrayDeclaration,
    ArrayDeclarationEmpty,
    FunctionCall,
    ArrayAccess,
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
        if self.position-1 is None:
            return None
        return self.tokens[self.position-1]

    #Advance position and return previous token
    def advance(self) -> Token:
        if not self.is_at_end():
            self.position+=1
        return self.previous()

    #If token is of specific type; advance position and return previous token.
    #If not of specific type; raise error with argument message.
    def consume(self, token_type: TokenType) -> Token:
        if self.current().type == token_type:
            return self.advance()
        raise self.error(ErrorCode.STRUCTURE_ERROR)

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
        if self.position+1 > len(self.tokens) - 1:
            return None
        return self.tokens[self.position+1]

    #Return parser error with custom message
    def error(self, error_code: ErrorCode) -> ParserError:
        return ParserError(error_code, self.current(), self.previous())


    def parse(self) -> Program:
        functions = []
        while not self.is_at_end():
            functions.append(self.function())
        return Program(functions, self.current().line, self.current().column)

    def function(self) -> Function:
        type = self.consume(TokenType.TYPE)
        name = self.consume(TokenType.IDENTIFIER)
        parameters = self.parameters()
        body = self.statement()
        return Function(type.value, name.value, parameters, body, name.line, name.column)

    def parameters(self) -> list:
        parameters = []
        self.consume(TokenType.LPAREN)
        while self.current().type is not TokenType.RPAREN:
            type = self.consume(TokenType.TYPE)
            name = self.consume(TokenType.IDENTIFIER)
            parameters.append(Parameter(type.value, name.value, name.line, name.column))
            #if we haven't reached the end of the parameters consume the commas 
            if self.current().type is not TokenType.RPAREN:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RPAREN)
        return parameters
            
    def statement(self) -> Statement:
        if self.match(TokenType.LCBRACE):
            return self.block_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()
        
        if self.match(TokenType.TYPE):
            return self.var_declaration()
        
        if self.match(TokenType.IDENTIFIER):
            return self.assign_statement()

        return self.expression_statement()

    def var_declaration(self) -> VarDeclaration | ArrayDeclaration | ArrayDeclarationEmpty:
        type = self.previous()
        name = self.advance() #integer b = a[3]
        
        if self.match(TokenType.LBRACE): 
            if self.match(TokenType.RBRACE): #integer a[] = {1,2,3,4}
                self.consume(TokenType.ASSIGN) 
                if self.check(TokenType.LCBRACE):
                    elements = self.parse_array_literal()
                    self.consume(TokenType.SEMICOLON)
                    return ArrayDeclaration(type.value, name.value, elements, name.line, name.column)
            else: # Integer arr[3]
                size = self.parse_expression()
                self.consume(TokenType.RBRACE)
                self.consume(TokenType.SEMICOLON)
                return ArrayDeclarationEmpty(type.value, name.value, size, name.line, name.column)
        
        
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return VarDeclaration(type.value, name.value, value, name.line, name.column)
    
    def parse_array_literal(self) -> list:
        self.consume(TokenType.LCBRACE)  # spiser {
        elements = []
        if not self.check(TokenType.RCBRACE):
            elements.append(self.parse_expression())
        while self.match(TokenType.COMMA):
            elements.append(self.parse_expression())
        self.consume(TokenType.RCBRACE)  # spiser ]
        return elements
    
    def block_statement(self) -> BlockStatement:
        lbrace = self.previous()
        statements = []
        while not self.check(TokenType.RCBRACE) and not self.is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RCBRACE)
        return BlockStatement(statements, lbrace.line, lbrace.column)

    def while_statement(self) -> WhileStatement:
        while_token = self.previous()
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LCBRACE)
        body = self.block_statement()
        return WhileStatement(condition, body, while_token.line, while_token.column)

    def assign_statement(self) -> AssignStatement:
        #match() advances the the cursor, meaning the name is present on previous instead of present token 
        name = self.previous()
        offset = None
        if self.current().type == TokenType.LBRACE:
            self.consume(TokenType.LBRACE)
            offset = self.parse_expression()
            self.consume(TokenType.RBRACE)
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return AssignStatement(name.value, offset, value, name.line, name.column) 

    def if_statement(self) -> IfStatement:
        if_token = self.previous()
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LCBRACE)
        then_branch = self.block_statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LCBRACE)
            else_branch = self.block_statement()
        
        return IfStatement(condition, then_branch, else_branch, if_token.line, if_token.column)

    def return_statement(self) -> ReturnStatement:
        return_token = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ReturnStatement(value, return_token.line, return_token.column)
    
    def expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        semi = self.consume(TokenType.SEMICOLON)
        return ExpressionStatement(expr, semi.line, semi.column)
    
    #Expressions
    def parse_expression(self):
        print(self.current())

        return self.parse_or()

    def parse_or(self): #self.match do self.advance
        left = self.parse_and()
        while self.match(TokenType.OR):
            op = self.previous()
            left = Binary(left, op.value, self.parse_and(), op.line, op.column)
        return left
    
    def parse_and(self):
        left = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.previous()
            left = Binary(left, op.value, self.parse_equality(), op.line, op.column)
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.previous()
            left = Binary(left, op.value, self.parse_comparison(), op.line, op.column)
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.previous()
            left = Binary(left, op.value, self.parse_additive(), op.line, op.column)
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            left = Binary(left, op.value, self.parse_multiplicative(), op.line, op.column)
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            op = self.previous()
            left = Binary(left, op.value, self.parse_unary(), op.line, op.column)
        return left
    
    def parse_unary(self):
        if self.match(TokenType.NOT):
            op = self.previous()
            return Unary(op.value, self.parse_unary(), op.line, op.column)
        elif self.match(TokenType.MINUS):
            op = self.previous()
            return Unary(op.value, self.parse_unary(),op.line, op.column)
        return self.parse_primary()
    
    def arguments(self) -> list:
        arguments = []
        self.consume(TokenType.LPAREN)
        while self.current().type is not TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current().type is not TokenType.RPAREN:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RPAREN)
        return arguments
    
    def parse_primary(self):
        tok = self.current()

        if self.match(TokenType.INTEGER):
            return Literal(tok.value, tok.line, tok.column)
        
        if self.match(TokenType.FLOAT):
            return Literal(tok.value, tok.line, tok.column)
        
        if self.match(TokenType.TRUE):
            return Literal(True, tok.line, tok.column)
        
        if self.match(TokenType.FALSE):
            return Literal(False, tok.line, tok.column)
        
        if self.match(TokenType.STRING):
            return Literal(tok.value, tok.line, tok.column)
        
        # Array access: a[3]
        if (self.current().type == TokenType.IDENTIFIER 
                and self.peek() is not None 
                and self.peek().type == TokenType.LBRACE):
            name = self.consume(TokenType.IDENTIFIER)
            self.consume(TokenType.LBRACE)
            index = self.parse_expression()
            self.consume(TokenType.RBRACE)
            return ArrayAccess(name.value, index, name.line, name.column)
        
        if self.current().type == TokenType.IDENTIFIER and self.peek().type == TokenType.LPAREN:
            name = self.consume(TokenType.IDENTIFIER)
            arguments = self.arguments() 
            return FunctionCall(name.value, arguments, name.line, name.column)

        if self.match(TokenType.IDENTIFIER):
            return Variable(tok.value, tok.line, tok.column)
        
        #Parenteser
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            if not self.match(TokenType.RPAREN):
                raise self.error(ErrorCode.STRUCTURE_ERROR) 
            return expr

        raise self.error(ErrorCode.UNEXPECTED_TOKEN_ERROR)