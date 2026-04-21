from enum import Enum

class ErrorCode(Enum):
    #ParserErrors
    STRUCTURE_ERROR = 21
    SEMICOLON_ERROR = 22
    UNEXPECTED_TOKEN_ERROR = 23 



class LexerError(Exception):
    def __init__(self, message, error_code: ErrorCode, start_line, start_col):
         super().__init__(message)
         self.error_code = error_code
         self.start_col = start_col
         self.start_line = start_line
    
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code} at line {self.start_line}, column {self.start_col})"
    
class ParserError(Exception):
    def __init__(self, error_code: ErrorCode, token, previous_token):
        if error_code == ErrorCode.STRUCTURE_ERROR:
            message = f"Parser Error: Unexpected '{token.value}' after '{previous_token.value}'"
        elif error_code == ErrorCode.SEMICOLON_ERROR:
            message = f"Parser Error: Expected ';' after '{previous_token.value}'"
        elif error_code == ErrorCode.UNEXPECTED_TOKEN_ERROR:
            message = f"Parser Error: Unexpected Token '{token.value}'"
        else:
            message = "Parser Error"
        
        super().__init__(message)
        self.message = message  # Store it explicitly
        self.error_code = error_code
        self.token = token
        self.previous_token = previous_token
    
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code} at line {self.token.line}, column {self.token.column})"