from enum import Enum

# OVERVEJ at lave en global message klasse, som bruges på tværs af lexer, parser og type checker
## og så bruge 

class ErrorCode(Enum):
    # ParserErrors
    STRUCTURE_ERROR = 21
    SEMICOLON_ERROR = 22
    UNEXPECTED_TOKEN_ERROR = 23 

    # TypeCheckerErrors
    UNDEFINED_VARIABLE_ERROR = 67
    UNDEFINED_FUNCTION_ERROR = 68
    ALREADY_DECLARED_ERROR = 69
    CANNOT_ASSIGN = 70
    SCOPE_ERROR = 71
    # ARRAY MISTAKES missing



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
    

# skal indeholde errorcodes for: 
## undefined variables
## undefined functions 
## unreachable statements within scope (line 679)
## already declared variable (line 711)
## cannot assign value of type ?? to variable ?? of type ?? (line 783)
## array mistakes (line 724-765)

class TypeCheckerError(Exception):
    def __init__(self, error_code: ErrorCode, message, line, column, name, type_name, value_type, target_type, stmt):
        if error_code == ErrorCode.SCOPE_ERROR:
            message = f"Type Error: Unreachable statement."
        elif error_code == ErrorCode.UNDEFINED_FUNCTION_ERROR:
            message = f"Undefined function '{name}'."
        elif error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR:
            message = f"Undefined variable '{name}'."
        elif error_code == ErrorCode.ALREADY_DECLARED_ERROR:
            message = f"Function '{function.name}' is already declared."
        elif error_code == ErrorCode.CANNOT_ASSIGN:
            message = f"Cannot assign value of type {type_name(value_type)} to variable '{stmt.name}' of type {type_name(target_type)}. "
        
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.column = column
        self.line = line

    def __str__(self):
        return f"{self.message} (Error code: {self.error_code} at line {self.line}, column {self.column})"
    

