from enum import Enum
source = "integer x = 5 ;"
tokens = []




KEYWORDS = {
    "integer": "INTEGER",
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
    def skip_block_comment(Self):
        return

    ##
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

        ##
        #TODO: insert error handling
        ##
        if number_str.count(".") > 1:
            print("Invalid Number")
            return None

        if '.' in number_str:
            return float(number_str)
        return int(number_str)


    #Function to read identifier and check if identifier is a keyword
    def read_identifier(self):
        return

    #Function to read strings, denoted by quotes
    def read_string(self):
        return
    
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


