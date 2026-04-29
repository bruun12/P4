#from enum import Enum
#
## OVERVEJ at lave en global message klasse, som bruges på tværs af lexer, parser og type checker
### og så bruge 
#
#class ErrorCode(Enum):
#    # ParserErrors
#    STRUCTURE_ERROR = 21
#    SEMICOLON_ERROR = 22
#    UNEXPECTED_TOKEN_ERROR = 23 
#
#    # TypeCheckerErrors
#    UNDEFINED_VARIABLE_ERROR = 67
#    UNDEFINED_FUNCTION_ERROR = 68
#    ALREADY_DECLARED_ERROR = 69
#    CANNOT_ASSIGN = 70
#    SCOPE_ERROR = 71
#    # ARRAY MISTAKES missing
#
#
#
#class LexerError(Exception):
#    def __init__(self, message, error_code: ErrorCode, start_line, start_col):
#         super().__init__(message)
#         self.error_code = error_code
#         self.start_col = start_col
#         self.start_line = start_line
#    
#    def __str__(self):
#        return f"{self.message} (Error code: {self.error_code} at line {self.start_line}, column {self.start_col})"
#    
#class ParserError(Exception):
#    def __init__(self, error_code: ErrorCode, token, previous_token):
#        if error_code == ErrorCode.STRUCTURE_ERROR:
#            message = f"Parser Error: Unexpected '{token.value}' after '{previous_token.value}'"
#        elif error_code == ErrorCode.SEMICOLON_ERROR:
#            message = f"Parser Error: Expected ';' after '{previous_token.value}'"
#        elif error_code == ErrorCode.UNEXPECTED_TOKEN_ERROR:
#            message = f"Parser Error: Unexpected Token '{token.value}'"
#        else:
#            message = "Parser Error"
#        
#        super().__init__(message)
#        self.message = message  # Store it explicitly
#        self.error_code = error_code
#        self.token = token
#        self.previous_token = previous_token
#    
#    def __str__(self):
#        return f"{self.message} (Error code: {self.error_code} at line {self.token.line}, column {self.token.column})"
#    
#
## skal indeholde errorcodes for: 
### undefined variables
### undefined functions 
### unreachable statements within scope (line 679)
### already declared variable (line 711)
### cannot assign value of type ?? to variable ?? of type ?? (line 783)
### array mistakes (line 724-765)
#
#
#class TypeCheckError(Exception):
#    def __init__(self, message: str, line: int, column: int):
#        super().__init__(message)
#        self.message = message
#        self.line = line
#        self.column = column
#
#def format_type_error(error: TypeCheckError, source_lines: list[str]) -> str:
#    """
#    Pretty-print a type error with source context.
#    """
#    line = error.line
#    column = error.column
#
#    if line < 1 or line > len(source_lines):
#        return f"Type error: {error.message} [line {line}, col {column}]"
#
#    code_line = source_lines[line - 1]
#    caret_line = " " * max(column - 1, 0) + "^"
#
#    return (
#        f"Type error: {error.message}\n"
#        f" --> line {line}, col {column}\n"
#        f"  |\n"
#        f"{line} | {code_line}\n"
#        f"  | {caret_line}"
#    )



"""
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
    
"""
from enum import Enum


class ErrorCode(Enum):
    INVALID_CHARACTER = 1
    UNTERMINATED_STRING = 2

    STRUCTURE_ERROR = 21
    SEMICOLON_ERROR = 22
    UNEXPECTED_TOKEN_ERROR = 23

    UNDEFINED_VARIABLE_ERROR = 67
    UNDEFINED_FUNCTION_ERROR = 68
    ALREADY_DECLARED_ERROR = 69
    CANNOT_ASSIGN = 70
    UNREACHABLE_ERROR = 71
    UNKNOWN_DECLARED_TYPE = 72
    MISSING_RETURN_ERROR = 73
    INVALID_PARAMETER_TYPE = 74
    INVALID_DECLARED_TYPE = 75
    INVALID_RETURN_ERROR = 76
    TYPE_MISMATCH_ERROR = 77
    INVALID_ARGUMENT_COUNT = 78
    UNKNOWN_AST_NODE_ERROR = 79


class CompilerError(Exception):
    def __init__(self, message: str, error_code: ErrorCode, line: int, column: int, stage: str):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.line = line
        self.column = column
        self.stage = stage


class LexerError(CompilerError):
    def __init__(self, message: str, error_code: ErrorCode, line: int, column: int):
        super().__init__(message, error_code, line, column, "lexer")


class ParserError(CompilerError):
    def __init__(self, message: str, error_code: ErrorCode, line: int, column: int):
        super().__init__(message, error_code, line, column, "parser")


class TypeCheckError(CompilerError):
    def __init__(self, message: str, error_code: ErrorCode, line: int, column: int):
        super().__init__(message, error_code, line, column, "type")


def format_compiler_error(error: CompilerError, source_lines: list[str]) -> str:
    line = error.line
    column = error.column
    stage_name = error.stage.capitalize()

    if line < 1 or line > len(source_lines):
        return (
            f"{stage_name} error [{error.error_code.name}]: {error.message} "
            f"[line {line}, col {column}]"
        )

    code_line = source_lines[line - 1]
    caret_line = " " * max(column - 1, 0) + "^"

    return (
        f"{stage_name} error [{error.error_code.name}]: {error.message}\n"
        f" --> line {line}, col {column}\n"
        f"  |\n"
        f"{line} | {code_line}\n"
        f"  | {caret_line}"
    )