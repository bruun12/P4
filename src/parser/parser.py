class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def advance(self):
        self.pos += 1
    
    #functions that runs recursively until we have the whole tree