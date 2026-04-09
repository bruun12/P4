from enum import Enum, auto

class Token:

    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    

class TokenType(Enum):
    # Special
    EOF = auto()
    INVALID = auto()

    # Literals
    TYPE = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # Keywords
    BOOLEAN = auto()
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
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # [
    RBRACE = auto()       # ]
    LCBRACE = auto()      # {
    RCBRACE = auto()      # }
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,

KEYWORDS = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
    "MOD": TokenType.PERCENT 
}

TYPES = {
    "integer": TokenType.INTEGER,
    "double": TokenType.FLOAT,
    "string": TokenType.STRING,
    "boolean": TokenType.BOOLEAN
}


DELIMITERS = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LCBRACE,
    "}": TokenType.RCBRACE,
    ";": TokenType.SEMICOLON,
    "[": TokenType.LBRACE,
    "]": TokenType.RBRACE,
    ",": TokenType.COMMA
}

OPERATORS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH
}


