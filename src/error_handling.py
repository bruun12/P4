class LexerError(Exception):
    def __init__(self, message, error_code, start_col, start_line):
         super().__init__(message, start_col, start_line)
         self.message = message
         self.error_code = error_code
         self.start_col = start_col
         self.start_line = start_line
    
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code} at line {self.start_line}, column {self.start_col})"