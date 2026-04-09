from lexer.token import Token,TokenType,KEYWORDS,TYPES,DELIMITERS,OPERATORS

from error_handling import LexerError


class Lexer:

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    #Function for finding current char in source
    def current_char(self):
        if self.position >= self.length:
            return None
        return self.source[self.position]

    #Function for viewing the next char in source
    def peek_next_char(self):
        if self.position+1 >= self.length:
            return None
        return self.source[self.position+1]

    #Function for advancing for whitespace and next line
    def advance(self):
        ch = self.current_char()
        if ch is None:
            return None

        self.position += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch


    #Function to skip block comments
    def skip_comment(self):
        startColumn = self.column
        startLine = self.line

        while (self.current_char() != '*' or self.peek_next_char() != '/'):
            if self.position >= self.length:
                raise LexerError("Comment is never ended, please put */", 420, startColumn, startLine)
            self.advance()  
        self.advance()
        self.advance()
        return self.current_char()
 
        
    #Function to read number; can be integer or float
    ##
    def read_number(self) -> Token:
        startPos = self.position
        startColumn = self.column
        startLine = self.line

        
        # Check if we haven't reached the end of the source
        while self.position < self.length:
            char = self.peek_next_char()
            # check is needed because we are peaking at a char that doesn't exist
            if char is None:
                break
            if char.isdigit() or char == '.':
                self.advance()
            else:
                break
        
        self.advance()

        number_str = self.source[startPos:self.position]

        if number_str.count(".") > 1:
            raise LexerError("A error on line: " + str(startLine) + " Invalid number: a number can only have one punctuation", 12, startLine, startColumn)

        if '.' in number_str:
            return Token(TokenType.FLOAT, float(number_str), startLine, startColumn)
        else:
            return Token(TokenType.INTEGER, int(number_str), startLine, startColumn)
        

    #Function to read identifier or other keyword and return Token
    def read_word(self) -> Token:
        startLine = self.line
        startColumn = self.column
        startPos = self.position

        while (self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == "_")):
            self.advance()

        #Slice [self.source[startPos:self.position]] is a subarray of the full array
        #self.source[] from position "startPos" to "self.position"
        value = self.source[startPos:self.position]

        if value in KEYWORDS:
            return Token(KEYWORDS[value] , value, startLine, startColumn)
        elif value in TYPES:
            return Token(TokenType.TYPE, value, startLine, startColumn)
        else:
            return Token(TokenType.IDENTIFIER, value, startLine, startColumn)

    #Function to read strings, denoted by quotes
    def read_string(self) -> Token:
        self.advance()
        startLine = self.line
        startColumn = self.column
        startPos = self.position
        while (self.current_char() != '"'):
            if (self.position >= self.length):
                raise LexerError("Missing closing quote", 6969, startLine, startColumn)
            self.advance()
        value = self.source[startPos:self.position]

        self.advance()

        return Token(TokenType.STRING, value, startLine, startColumn)
    
    def add_token(self, token):
        self.tokens.append(token)


    #
    def lexer(self):
        while(self.position < self.length):
            token = None
            
            char = self.current_char()
            peek = self.peek_next_char()
            
            # Skip to next token
            if char.isspace():
                self.advance()
                continue
            
            if char == '/' and peek == '*':
                self.skip_comment()
                continue
        
            if char.isdigit():
                token = self.read_number()
            elif char.isalpha():
                token = self.read_word()
            elif char == '"':
                token = self.read_string()
            
            #Arithmetic operators
            elif char in OPERATORS:
                token = Token(OPERATORS[char], char, self.line, self.column)
                self.advance()
                
            #boolean operators
            elif char == '=' and peek == '=':
                token = Token(TokenType.EQ, '==', self.line, self.column)
                self.advance()
                self.advance()
            elif char == '!' and peek == '=':
                token = Token(TokenType.NE, '!=', self.line, self.column)
                self.advance()
                self.advance()
            elif char == '<' and peek != '=':
                token = Token(TokenType.LT, '<', self.line, self.column)
                self.advance()
            elif char == '<' and peek == '=':
                token = Token(TokenType.LE, '<=', self.line, self.column)
                self.advance()
            elif char == '>' and peek != '=':
                token = Token(TokenType.GT, '>', self.line, self.column)
                self.advance()
            elif char == '>' and peek == '=':
                token = Token(TokenType.GE, '>=', self.line, self.column)
                self.advance()

            #Assign
            elif char == '=' and peek != '=':
                token = Token(TokenType.ASSIGN, '=', self.line, self.column)
                self.advance()

            #Delimiters
            elif char in DELIMITERS:
                token = Token(DELIMITERS[char], char, self.line, self.column)
                self.advance()

            else:
                raise LexerError("Invalid token", 1, self.line, self.column)
            
            if token is not None:
                self.add_token(token)
            
            
        
        self.add_token(Token(TokenType.EOF, "EOF", self.line, self.column))
