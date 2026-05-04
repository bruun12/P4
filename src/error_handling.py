from enum import Enum


class ErrorCode(Enum):
    INVALID_CHARACTER = 1
    UNTERMINATED_STRING = 2
    UNTERMINATED_COMMENT = 3
    INVALID_NUMBER = 4

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