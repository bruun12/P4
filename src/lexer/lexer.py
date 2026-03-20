import sys
from enum import Enum
source = "integer x = 5 ;"
tokens = []

KEYWORDS = {
    "ingeger": "INTEGER",
}

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
        self.self.position = 0
        self.line = 1
        self.column = 1

    #Function for finding current char in source
    def current_char(self):
        return

    #Function for viewing the next char in source
    def peek_next_char(self):
        return

    #Function for advancing for whitespace and next line
    def advance(self):
        return

    #Function to skip block comments
    def skip_block_comment(Self):
        return

    def read_number(self):
        
    def lexer(self):
        while(self.position < self.length):
            char = source[self.position]
            print(char)
            if char.isspace():
                self.position+=1
            elif char.isdigit():
                start = self.position
                while self.position < self.length and source[self.position].isdigit():
                    self.position+=1
                value = source[start:self.position]
                tokens.append(("NUMBER", value))
            elif char.isalpha():
                start = 0
                while self.position < self.length and (source[self.position].isalum() or source[self.position] == "_"):
                    self.position+=1
                value = source[start:self.position]
                if value == "integer":
                    tokens.append(("IDENTIFIER", value))


