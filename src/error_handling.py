class LexerError(Exception):
    def __init__(self, message, error_code):
         super().__init__(message)
         self.error_code = error_code
    
    def __str__(self):
        return f"{self.message} (Error code: {self.error_code})"