from enum import Enum, auto

from error_handling import LexerError

#source = "integer x = 5 ;"
#tokens = []


class TokenType(Enum):
    # Special
    EOF = auto()

    # Literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # Keywords
    LET = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    ASSIGN = auto()       # =
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    LE = auto()           # <=
    GT = auto()           # >
    GE = auto()           # >=

    AND = auto()          # &&
    OR = auto()           # ||
    NOT = auto()          # !

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()

KEYWORDS = {
    "integer": TokenType.INTEGER,
    "double floating point": TokenType.FLOAT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL
}

class Token:

    def __init__(self, type, value, row, column):
        self.type = type
        self.value = value
        self.row = row
        self.column = column
    
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})"

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

        while (self.current_char() != '*' or self.peek_next_char() != '/'):
            if self.position >= self.length:
                raise LexerError("Comment is never ended, please put */", 420)
            self.advance()  
        self.advance()
        self.advance()
        return self.current_char()
 
        
    #Function to read number; can be integer or float
    ##
    def read_number(self):
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
            self.add_token(Token(TokenType.FLOAT, float(number_str), self.line, self.column))
        else:
            self.add_token(Token(TokenType.INTEGER, int(number_str), self.line, self.column))
        return


    #Function to read identifier and check if identifier is a keyword
    def read_identifier(self):
        start_line = self.line
        start_col = self.column
        start_pos = self.position

        while (self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == "_")):
            self.advance()

        value = self.source[start_pos:self.position]
        
        return token()
        

    #Function to read strings, denoted by quotes
    def read_string(self):
        return
    
    def add_token(self, token):
        self.tokens.append(token)

    #
    def lexer(self):
        while(self.position < self.length):
            char = source[self.position]
            print(char)
            if char.isspace():
                self.position+=1
            elif char.isdigit():
                value = self.read_number()
                tokens.append(("NUMBER", value))
            elif char.isalpha():
                start = 0
                while self.position < self.length and (source[self.position].isalum() or source[self.position] == "_"):
                    self.position+=1
                value = source[start:self.position]
                if value == "integer":
                    tokens.append(("IDENTIFIER", value))


