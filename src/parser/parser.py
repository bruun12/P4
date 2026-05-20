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
    # Properties within the parser
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0
        self.errors: list[ParserError] = []

    # Function to return current token
    def current(self) -> Token:
        return self.tokens[self.position]

    # Function to return previous token
    def previous(self) -> Token:
        if self.position == 0:
            return None
        return self.tokens[self.position-1]

    # Function to advance position and return previous token
    def advance(self) -> Token:
        if not self.is_at_end():
            self.position+=1
        return self.previous()

    # If token is of specific type; advance position, and return previous token through advance().
    # If not of specific type; raise error with argument message.
    def consume(self, token_type: TokenType) -> Token:
        if self.current().type == token_type:
            return self.advance()
        raise self.error(
            f"Parser Error: Unexpected '{self.current().value}' after '{self.previous().value}'",
            ErrorCode.STRUCTURE_ERROR
        )

    # Function to return true if current token is of type "EOF"
    def is_at_end(self) -> bool:
        if self.current().type == TokenType.EOF:
            return True
        return False

    # Function to return true if current token is of specific type
    def check(self, token_type: TokenType) -> bool:
        if self.current().type == token_type:
            return True
        return False

    # Function to return true if current token is of specific types
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    # Function to check the next token 
    def peek(self) -> Token | None:
        if self.position+1 > len(self.tokens) - 1:
            return None
        return self.tokens[self.position+1]

    # Function to return parser error with custom message
    def error(self, message: str, error_code: ErrorCode):
        return ParserError(message, error_code, self.current().line, self.current().column)

    # Function to parse the full program
    def parse(self) -> Program:
        functions = []
        try:
            while not self.is_at_end():
                functions.append(self.function())
            return Program(functions, self.current().line, self.current().column)
        except ParserError as err:
            self.errors.append(err)
            raise
    
    # Function to return a function
    def function(self) -> Function:
        type = self.consume(TokenType.TYPE)
        name = self.consume(TokenType.IDENTIFIER)
        parameters = self.parameters()
        body = self.statement()

        return Function(type.value, name.value, parameters, body, name.line, name.column)

    # Function to return a list of parameters
    def parameters(self) -> list:
        parameters = []
        self.consume(TokenType.LPAREN)

        # If the char is not a right parenthesis, then check and append the parameter to the list of parameters
        while self.current().type is not TokenType.RPAREN:
            type = self.consume(TokenType.TYPE)
            name = self.consume(TokenType.IDENTIFIER)
            parameters.append(Parameter(type.value, name.value, name.line, name.column))

            #if we haven't reached the end of the parameters, consume the commas 
            if self.current().type is not TokenType.RPAREN:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RPAREN)

        return parameters
    
    # Function to return a specific statement 
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
        
        if self.current().type == TokenType.IDENTIFIER and self.peek().type == TokenType.LPAREN:
            return self.expression_statement()
        
        if self.current().type == TokenType.IDENTIFIER and self.peek().type != TokenType.ASSIGN and self.peek().type != TokenType.LBRACE:
            return self.expression_statement()
        
        if self.match(TokenType.IDENTIFIER):
            return self.assign_statement()

        return self.expression_statement()

    # Function to return a variable declaration, array declaration or an empty array declaration
    def var_declaration(self) -> VarDeclaration | ArrayDeclaration | ArrayDeclarationEmpty:
        type = self.previous()
        name = self.advance() # example; integer b = a[3]
        
        # Checks if it is an array declaration
        if self.match(TokenType.LBRACE):
            size = self.parse_expression()
            self.consume(TokenType.RBRACE)

            if self.match(TokenType.ASSIGN): # example; integer a[] = [1,2,3,4]
                if self.check(TokenType.LBRACE):
                    elements = self.parse_array_literal()
                    self.consume(TokenType.SEMICOLON)

                    # Return the properties to the array declaration with content
                    return ArrayDeclaration(type.value, name.value, elements, size, name.line, name.column)
            else: # integer arr[3]
                self.consume(TokenType.SEMICOLON)

                # If it has no content, return the properties of the empty array
                return ArrayDeclarationEmpty(type.value, name.value, size, name.line, name.column)
        
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)

        # Return the properties of the variable declaration
        return VarDeclaration(type.value, name.value, value, name.line, name.column)
    
    # Function to parse array elements
    def parse_array_literal(self) -> list:
        self.consume(TokenType.LBRACE) 
        elements = []

        # If it isn't a right bracket, then append the array elements,
        # and see if there is a comma between elements
        if not self.check(TokenType.RBRACE):
            elements.append(self.parse_expression())

        while self.match(TokenType.COMMA):
            elements.append(self.parse_expression())

        self.consume(TokenType.RBRACE)
        
        return elements
    
    # Function to return block statements 
    def block_statement(self) -> BlockStatement:
        lbrace = self.previous()
        statements = []

        # As long as there isn't a right brace and it isn't at the end, 
        # then append the statement to the list of statements
        while not self.check(TokenType.RCBRACE) and not self.is_at_end():
            statements.append(self.statement())
        self.consume(TokenType.RCBRACE)

        # Return the properties of the block statement
        return BlockStatement(statements, lbrace.line, lbrace.column)

    # Function to return a while statement
    def while_statement(self) -> WhileStatement:
        while_token = self.previous()
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LCBRACE)
        body = self.block_statement()

        # Return the properties of the while statement
        return WhileStatement(condition, body, while_token.line, while_token.column)

    # Function to return an assignement statement
    def assign_statement(self) -> AssignStatement:
        name = self.previous()
        offset = None

        # Checks if the statement contains a left brace, 
        # then check its content
        if self.current().type == TokenType.LBRACE:
            self.consume(TokenType.LBRACE)
            offset = self.parse_expression()
            self.consume(TokenType.RBRACE)
        
        # Consume the given assign and semicolon symbols
        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)

        # Return the properties of the assignement statement
        return AssignStatement(name.value, offset, value, name.line, name.column) 

    # Function to return an if-statement
    def if_statement(self) -> IfStatement:
        # Checks if the statement contains () and {
        if_token = self.previous()
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.LCBRACE)
        then_branch = self.block_statement()

        else_branch = None

        # If else-statement, then consume } and make it a blockstmt
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LCBRACE)
            else_branch = self.block_statement()
        
        # Return the properties of the if-statement
        return IfStatement(condition, then_branch, else_branch, if_token.line, if_token.column)

    # Function to return a return statement
    def return_statement(self) -> ReturnStatement:
        return_token = self.previous()
        value = None

        # Checks to make sure there is an end ;
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)

        # Return the properties of the return statement
        return ReturnStatement(value, return_token.line, return_token.column)
    
    def expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        semi = self.consume(TokenType.SEMICOLON)
        return ExpressionStatement(expr, semi.line, semi.column)
    

# Functions that returns all the expressions
    def parse_expression(self):
        return self.parse_or()

    # Arithmetic OR
    def parse_or(self): #self.match do self.advance
        left = self.parse_and()
        while self.match(TokenType.OR):
            op = self.previous()
            left = Binary(left, op.value, self.parse_and(), op.line, op.column)
        return left
    
    # Arithmetic AND
    def parse_and(self):
        left = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.previous()
            left = Binary(left, op.value, self.parse_equality(), op.line, op.column)
        return left
    
    # Arithmetic OR
    def parse_equality(self):
        left = self.parse_comparison()
        while self.match(TokenType.EQ, TokenType.NE):
            op = self.previous()
            left = Binary(left, op.value, self.parse_comparison(), op.line, op.column)
        return left
    
    # Comparison expressions (<, <=, >, >=)
    def parse_comparison(self):
        left = self.parse_additive()
        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.previous()
            right = self.parse_additive()
            comparison = Binary(left, op.value, right, op.line, op.column)
            left = self.parse_chain(comparison, right) 
        return left
    
    def parse_chain(self, comparison, left):
        if not self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            return comparison
        op = self.previous()
        right = self.parse_additive()
        new_comparison = Binary(left, op.value, right, op.line, op.column)
        combined = Binary(comparison, 'AND', new_comparison, op.line, op.column)
        return self.parse_chain(combined, right)


    
    # Arithmetic operators (+, -)
    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous()
            left = Binary(left, op.value, self.parse_multiplicative(), op.line, op.column)
        return left
    
    # Arithmetic operators (*, /, MOD)
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.MOD):
            op = self.previous()
            left = Binary(left, op.value, self.parse_unary(), op.line, op.column)
        return left
    
    # Unary (NOT, -)
    def parse_unary(self):
        if self.match(TokenType.NOT):
            op = self.previous()
            return Unary(op.value, self.parse_unary(), op.line, op.column)
        elif self.match(TokenType.MINUS):
            op = self.previous()
            return Unary(op.value, self.parse_unary(),op.line, op.column)
        return self.parse_primary()
    
    # Function to parse arguments in functionCall
    def arguments(self) -> list:
        arguments = []
        self.consume(TokenType.LPAREN)
        while self.current().type is not TokenType.RPAREN:
            arguments.append(self.parse_expression())
            if self.current().type is not TokenType.RPAREN:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RPAREN)
        return arguments
    
    # Function to parse a primary value (ex. 5, True, 'hello') 
    def parse_primary(self):
        tok = self.current()

        if self.match(TokenType.INTEGER):
            return Literal(tok.value, tok.line, tok.column)
        
        if self.match(TokenType.DOUBLE):
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
                raise self.error(
                    f"Parser Error: Unexpected '{self.current().value}' after '{self.previous().value}'",
                    ErrorCode.STRUCTURE_ERROR
                    ) 
            return expr

        raise self.error(
            f"Parser Error: Unexpected Token '{self.current().value}'",
            ErrorCode.UNEXPECTED_TOKEN_ERROR
            )