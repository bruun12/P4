from lexer.token import Token,TokenType,KEYWORDS

from error_handling import LexerError

source = "integer x = 5 ;"
tokens = []

class Token:

    def __init__(self, type, value, row, column):
        self.type = type
        self.value = value
        self.row = row
        self.column = column

class Lexer:

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.position = 0
        self.line = 1
        self.column = 1

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

        while (self.current_char() != '*' or self.peek_next_char() != '/'):
            if self.position >= self.length:
                raise LexerError("Comment is never ended, please put */", 420, self.column, self.line)
            self.advance()  
        self.advance()
        self.advance()
        return self.current_char()
 
        
    #Function to read number; can be integer or float
    ##
    def read_number(self) -> Token:
        start = self.position
        
        # Check if we haven't reached the end of the source
        while self.position < len(self.source):
            char = self.peek_next_char()
            # check is needed because we are peaking at a char that doesn't exist
            if char is None:
                break
            if char.isdigit() or char == '.':
                self.advance()
            else:
                break
        
        self.advance()

        number_str = self.source[start:self.position]

        if number_str.count(".") > 1:
            raise LexerError("A error on line: " + str(self.line) + " Invalid number: a number can only have one punctuation", 12)

        if '.' in number_str:

            return Token(TokenType.FLOAT, float(number_str), self.line, self.column)
        else:
            return Token(TokenType.INTEGER, int(number_str), self.line, self.column)
        

    #Function to read identifier or other keyword and return Token
    def read_identifier(self):
        start_line = self.line
        start_col = self.column
        start_pos = self.position

        while (self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == "_")):
            self.advance()

        value = self.source[start_pos:self.position]

        if value in KEYWORDS:
            return Token(KEYWORDS[value], value, start_line, start_col)
        return Token(TokenType.IDENTIFIER, value, start_line, start_col)

    #Function to read strings, denoted by quotes
    def read_string(self):
        self.advance()
        start_line = self.line
        start_col = self.column
        start = self.position
        while (self.current_char() != '"'):
            if (self.position >= self.length):
                raise LexerError("Missing closing quote", 6969, self.line, self.column)
            self.advance()
        string = self.source[start:self.position]
        self.advance()

        return Token(TokenType.STRING, string, start_line, start_col)
    def add_token(self, token):
        self.tokens.append(token)


    #
    def lexer(self):
        while(self.position < self.length):

            char = self.source[self.position]
            peek = self.peek_next_char()
            if char.isdigit():
                token = self.read_number()
            elif char.isalpha():
                token = self.read_identifier()
            elif char == '"':
                token = self.read_string()
            elif char == '=' and peek != '=':
                token = Token(TokenType.ASSIGN, '=', self.line, self.column)
            elif char == '/' and peek == '*':
                #If a comment is read continue to the next valid input
                self.skip_comment()
                continue

            self.add_token(token)

            self.advance()
