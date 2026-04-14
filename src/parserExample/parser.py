#class Parser:
#    def __init__(self, tokens):
#        self.tokens = tokens
#        self.pos = 0
#    
#    def current_token(self):
#        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
#    
#    def advance(self):
#        self.pos += 1
#    
#    #functions that runs recursively until we have the whole tree
try:
    from .ASTNodes import AssignStatement, Binary, BlockStatement, Expression, ExpressionStatement, Grouping, IfStatement, LetStatement, Literal, ParserError, Program, ReturnStatement, Statement, Unary, Variable, WhileStatement
except ImportError:
    from ASTNodes import AssignStatement, Binary, BlockStatement, Expression, ExpressionStatement, Grouping, IfStatement, LetStatement, Literal, ParserError, Program, ReturnStatement, Statement, Unary, Variable, WhileStatement

from lexer.token import TokenType, Token
from enum import Enum, auto
from dataclasses import dataclass


# ============================================================
# TOKEN TYPES
# ============================================================
# These are the categories of tokens the lexer can produce.
# The parser reads these token types and decides what grammar
# rule to apply.
# ============================================================


# ============================================================
# TOKEN OBJECT
# ============================================================
# A token stores:
# - its type
# - its exact source text/value
# - where it appeared in the source
# ============================================================


# ============================================================
# AST NODES
# ============================================================
# These classes define the shapes of the parsed program.
#
# We split them into:
# - statements
# - expressions
#
# This is very common in parsers.
# ============================================================




# ============================================================
# PARSER
# ============================================================
# This parser uses "recursive descent".
#
# That means:
# - there is one method per grammar level
# - methods call each other in precedence order
#
# The parser reads a list of tokens, keeps a current position,
# and builds AST nodes.
# ============================================================

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    # --------------------------------------------------------
    # Utility methods
    # --------------------------------------------------------

    def current(self) -> Token:
        """
        Return the current token.
        If pos somehow goes past the end, return the last token.
        In a normal token stream, the last token should be EOF.
        """
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def previous(self) -> Token:
        """
        Return the token just before the current one.
        Useful after advance().
        """
        return self.tokens[self.pos - 1]

    def is_at_end(self) -> bool:
        """
        We are considered "done" when current token is EOF.
        """
        return self.current().type == TokenType.EOF

    def advance(self) -> Token:
        """
        Move forward one token and return the token we just consumed.
        """
        if not self.is_at_end():
            self.pos += 1
        return self.previous()

    def check(self, token_type: TokenType) -> bool:
        """
        Return True if current token has the given type.
        Does not consume the token.
        """
        if self.is_at_end():
            return False
        return self.current().type == token_type

    def match(self, *types: TokenType) -> bool:
        """
        If current token matches any of the given types,
        consume it and return True. Otherwise return False.

        This is one of the most commonly used parser helpers.
        """
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        """
        Require that the current token has a specific type.
        If so, consume it and return it.
        Otherwise, raise a parser error with a helpful message.
        """
        if self.check(token_type):
            return self.advance()
        raise self.error(self.current(), message)

    def error(self, token: Token, message: str) -> ParserError:
        """
        Construct a parser error with line/column information.
        """
        return ParserError(
            f"[line {token.line}, col {token.column}] Error at {token.value!r}: {message}"
        )

    # --------------------------------------------------------
    # Entry point
    # --------------------------------------------------------

    def parse(self) -> Program:
        """
        Parse the whole token stream into a Program node.

        A program is just a list of statements until EOF.
        """
        statements = []

        while not self.is_at_end():
            statements.append(self.statement())

        return Program(statements)

    # --------------------------------------------------------
    # Statement parsing
    # --------------------------------------------------------
    # Statements are the top-level things inside a block/program.
    #
    # We try them in a specific order:
    # - let statement
    # - if statement
    # - while statement
    # - return statement
    # - block
    # - assignment statement
    # - expression statement
    # --------------------------------------------------------

    def statement(self) -> Statement:
        """
        Decide which kind of statement we're looking at.

        The order matters.
        """
        #if self.match(TokenType.LET):
        #    return self.let_statement()

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()

        if self.match(TokenType.LBRACE):
            return self.block_statement()

        # Assignment is a little special:
        # If we see IDENTIFIER followed by ASSIGN, then we treat it
        # as a statement like: x = something;
        #
        # Because our grammar is small, this is easy to detect here.
        if self.check(TokenType.IDENTIFIER) and self.peek_type() == TokenType.ASSIGN:
            return self.assign_statement()

        return self.expression_statement()

    def peek_type(self) -> TokenType | None:
        """
        Return the type of the next token (lookahead by 1),
        or None if there isn't one.
        """
        index = self.pos + 1
        if index >= len(self.tokens):
            return None
        return self.tokens[index].type

    def let_statement(self) -> LetStatement:
        """
        Parse:
            let IDENTIFIER = expression ;

        Example:
            let x = 5;
        """
        # After 'let', we require a variable name.
        name_token = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name after 'let'."
        )

        # Require '='
        self.consume(
            TokenType.ASSIGN,
            "Expected '=' after variable name."
        )

        # Parse the initializer expression on the right side.
        initializer = self.expression()

        # Require ending semicolon.
        self.consume(
            TokenType.SEMICOLON,
            "Expected ';' after variable declaration."
        )

        return LetStatement(name_token.value, initializer)

    def assign_statement(self) -> AssignStatement:
        """
        Parse:
            IDENTIFIER = expression ;

        Example:
            x = x + 1;
        """
        name_token = self.consume(
            TokenType.IDENTIFIER,
            "Expected variable name in assignment."
        )

        self.consume(
            TokenType.ASSIGN,
            "Expected '=' in assignment."
        )

        value = self.expression()

        self.consume(
            TokenType.SEMICOLON,
            "Expected ';' after assignment."
        )

        return AssignStatement(name_token.value, value)

    def if_statement(self) -> IfStatement:
        """
        Parse:
            if ( expression ) statement
            if ( expression ) statement else statement

        Examples:
            if (x > 0) return x;
            if (x > 0) { return x; } else { return 0; }
        """
        self.consume(
            TokenType.LPAREN,
            "Expected '(' after 'if'."
        )

        condition = self.expression()

        self.consume(
            TokenType.RPAREN,
            "Expected ')' after if condition."
        )

        # The "then" branch can be either:
        # - a single statement
        # - a block statement
        then_branch = self.statement()

        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return IfStatement(condition, then_branch, else_branch)

    def while_statement(self) -> WhileStatement:
        """
        Parse:
            while ( expression ) statement
        """
        self.consume(
            TokenType.LPAREN,
            "Expected '(' after 'while'."
        )

        condition = self.expression()

        self.consume(
            TokenType.RPAREN,
            "Expected ')' after while condition."
        )

        body = self.statement()
        return WhileStatement(condition, body)

    def return_statement(self) -> ReturnStatement:
        """
        Parse:
            return ;
            return expression ;

        We allow both forms here.
        """
        # If the next token is ';', then this is a bare return.
        if self.check(TokenType.SEMICOLON):
            self.advance()
            return ReturnStatement(None)

        value = self.expression()

        self.consume(
            TokenType.SEMICOLON,
            "Expected ';' after return value."
        )

        return ReturnStatement(value)

    def block_statement(self) -> BlockStatement:
        """
        Parse a block after already consuming '{'.

        Grammar:
            { statement* }

        Example:
            {
                let x = 1;
                x = x + 1;
            }
        """
        statements = []

        # Keep parsing statements until we hit '}' or EOF.
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.statement())

        self.consume(
            TokenType.RBRACE,
            "Expected '}' after block."
        )

        return BlockStatement(statements)

    def expression_statement(self) -> ExpressionStatement:
        """
        Parse:
            expression ;

        Example:
            x + 1;
        """
        expr = self.expression()

        self.consume(
            TokenType.SEMICOLON,
            "Expected ';' after expression."
        )

        return ExpressionStatement(expr)

    # --------------------------------------------------------
    # Expression parsing
    # --------------------------------------------------------
    #
    # This is where operator precedence happens.
    #
    # Higher-level methods call lower-level methods:
    #
    # expression   -> logical_or
    # logical_or   -> logical_and ( "||" logical_and )*
    # logical_and  -> equality ( "&&" equality )*
    # equality     -> comparison ( ("==" | "!=") comparison )*
    # comparison   -> term ( (">" | ">=" | "<" | "<=") term )*
    # term         -> factor ( ("+" | "-") factor )*
    # factor       -> unary ( ("*" | "/" | "%") unary )*
    # unary        -> ("!" | "-") unary | primary
    # primary      -> literals | identifiers | "(" expression ")"
    #
    # This ordering is what gives:
    # - multiplication higher precedence than addition
    # - comparisons lower precedence than arithmetic
    # - etc.
    # --------------------------------------------------------

    def expression(self) -> Expression:
        """
        Top-level expression parser.
        """
        return self.logical_or()

    def logical_or(self) -> Expression:
        """
        Parse expressions joined by ||.

        Example:
            a || b || c

        This is left-associative:
            ((a || b) || c)
        """
        expr = self.logical_and()

        while self.match(TokenType.OR):
            operator = self.previous().value
            right = self.logical_and()
            expr = Binary(expr, operator, right)

        return expr

    def logical_and(self) -> Expression:
        """
        Parse expressions joined by &&.
        """
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous().value
            right = self.equality()
            expr = Binary(expr, operator, right)

        return expr

    def equality(self) -> Expression:
        """
        Parse == and !=
        """
        expr = self.comparison()

        while self.match(TokenType.EQ, TokenType.NE):
            operator = self.previous().value
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expression:
        """
        Parse < <= > >=
        """
        expr = self.term()

        while self.match(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            operator = self.previous().value
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expression:
        """
        Parse + and -

        "term" is a traditional parser name for this precedence level.
        """
        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().value
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expression:
        """
        Parse * / %
        """
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous().value
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expression:
        """
        Parse unary prefix operators.

        Examples:
            -x
            !flag

        These bind tighter than binary operators.
        """
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous().value
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expression:
        """
        Parse the simplest expression forms:
        - literals
        - identifiers
        - parenthesized expressions
        """
        # true
        if self.match(TokenType.TRUE):
            return Literal(True)

        # false
        if self.match(TokenType.FALSE):
            return Literal(False)

        # null
        if self.match(TokenType.NULL):
            return Literal(None)

        # integer literal
        if self.match(TokenType.INTEGER):
            token = self.previous()
            return Literal(int(token.value))

        # float literal
        if self.match(TokenType.FLOAT):
            token = self.previous()
            return Literal(float(token.value))

        # string literal
        if self.match(TokenType.STRING):
            token = self.previous()
            return Literal(token.value)

        # variable / identifier
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            return Variable(token.value)

        # grouped expression: ( expression )
        if self.match(TokenType.LPAREN):
            expr = self.expression()

            self.consume(
                TokenType.RPAREN,
                "Expected ')' after expression."
            )

            return Grouping(expr)

        raise self.error(self.current(), "Expected expression.")


# ============================================================
# AST PRINTER
# ============================================================
# This is optional, but very useful for learning.
# It converts AST nodes into a readable string form so you can
# actually see what the parser built.
# ============================================================

def print_ast(node, indent=0):
    """
    Pretty-print the AST recursively.

    This function is just for understanding/debugging.
    A real interpreter/compiler would walk the AST differently.
    """
    space = "  " * indent

    if isinstance(node, Program):
        print(f"{space}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, BlockStatement):
        print(f"{space}BlockStatement")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif isinstance(node, LetStatement):
        print(f"{space}LetStatement name={node.name}")
        print(f"{space}  initializer:")
        print_ast(node.initializer, indent + 2)

    elif isinstance(node, AssignStatement):
        print(f"{space}AssignStatement name={node.name}")
        print(f"{space}  value:")
        print_ast(node.value, indent + 2)

    elif isinstance(node, IfStatement):
        print(f"{space}IfStatement")
        print(f"{space}  condition:")
        print_ast(node.condition, indent + 2)
        print(f"{space}  then:")
        print_ast(node.then_branch, indent + 2)
        if node.else_branch is not None:
            print(f"{space}  else:")
            print_ast(node.else_branch, indent + 2)

    elif isinstance(node, WhileStatement):
        print(f"{space}WhileStatement")
        print(f"{space}  condition:")
        print_ast(node.condition, indent + 2)
        print(f"{space}  body:")
        print_ast(node.body, indent + 2)

    elif isinstance(node, ReturnStatement):
        print(f"{space}ReturnStatement")
        if node.value is not None:
            print(f"{space}  value:")
            print_ast(node.value, indent + 2)
        else:
            print(f"{space}  value: None")

    elif isinstance(node, ExpressionStatement):
        print(f"{space}ExpressionStatement")
        print_ast(node.expression, indent + 1)

    elif isinstance(node, Literal):
        print(f"{space}Literal({node.value!r})")

    elif isinstance(node, Variable):
        print(f"{space}Variable({node.name})")

    elif isinstance(node, Unary):
        print(f"{space}Unary({node.operator})")
        print(f"{space}  right:")
        print_ast(node.right, indent + 2)

    elif isinstance(node, Binary):
        print(f"{space}Binary({node.operator})")
        print(f"{space}  left:")
        print_ast(node.left, indent + 2)
        print(f"{space}  right:")
        print_ast(node.right, indent + 2)

    elif isinstance(node, Grouping):
        print(f"{space}Grouping")
        print_ast(node.expression, indent + 1)

    else:
        print(f"{space}UnknownNode({node})")


# ============================================================
# DEMO TOKENS
# ============================================================
# Since your earlier question was about the parser itself,
# this example manually creates tokens instead of requiring a
# full lexer in the same file.
#
# In real usage, your lexer would generate these tokens.
# ============================================================

if __name__ == "__main__":
    tokens = [
        #Token(TokenType.LET, "let", 1, 1),
        Token(TokenType.IDENTIFIER, "x", 1, 5),
        Token(TokenType.ASSIGN, "=", 1, 7),
        Token(TokenType.INTEGER, "10", 1, 9),
        Token(TokenType.SEMICOLON, ";", 1, 11),

        Token(TokenType.IF, "if", 2, 1),
        Token(TokenType.LPAREN, "(", 2, 4),
        Token(TokenType.IDENTIFIER, "x", 2, 5),
        Token(TokenType.GT, ">", 2, 7),
        Token(TokenType.INTEGER, "5", 2, 9),
        Token(TokenType.RPAREN, ")", 2, 10),

        Token(TokenType.LBRACE, "{", 2, 12),

        Token(TokenType.IDENTIFIER, "x", 3, 5),
        Token(TokenType.ASSIGN, "=", 3, 7),
        Token(TokenType.IDENTIFIER, "x", 3, 9),
        Token(TokenType.PLUS, "+", 3, 11),
        Token(TokenType.INTEGER, "1", 3, 13),
        Token(TokenType.SEMICOLON, ";", 3, 14),

        Token(TokenType.RETURN, "return", 4, 5),
        Token(TokenType.IDENTIFIER, "x", 4, 12),
        Token(TokenType.SEMICOLON, ";", 4, 13),

        Token(TokenType.RBRACE, "}", 5, 1),

        Token(TokenType.ELSE, "else", 5, 3),
        Token(TokenType.LBRACE, "{", 5, 8),

        Token(TokenType.RETURN, "return", 6, 5),
        Token(TokenType.INTEGER, "0", 6, 12),
        Token(TokenType.SEMICOLON, ";", 6, 13),

        Token(TokenType.RBRACE, "}", 7, 1),

        Token(TokenType.EOF, "", 7, 2),
    ]

    parser = Parser(tokens)
    program = parser.parse()

    print_ast(program)