
# This function makes it possible to take a shortcut out of a function
# For example, in a for loop we will be 4 layers down before a return
class ReturnException(Exception): 
    def __init__(self, value): 
        self.value = value

# This class saves our values in the correct environment
class Environment:
    def __init__(self, parent=None): # Parent is the scope 
        self.vars = {}
        self.parent = parent
    
    # Function to take a variable if it exists
    def get(self, name):
        if name in self.vars:
            return self.vars[name] # Returns a variable if it exists
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Unknown Variable: '{name}'") # If the variable is not in scope; throw an error
    
    # Function to create a new variable in the current scope
    def set(self, name, value): 
        self.vars[name] = value
    
    # Function to assign a variable if it exists
    def assign(self, name, value):
        if name in self.vars:  
            self.vars[name] = value # If variable exists, assign it to a value
            return
        if self.parent: # If a parent scope exists, use it; else throw an error
            self.parent.assign(name, value)
            return
        raise RuntimeError(f"Variable not assigned: '{name}'")

# This class is the interpreter and (noget mere måske)
class Interpreter:
    def __init__(self):
        self.functions = {}
        self.global_env = Environment()
        self.position = 0

    # Function to run the program and check if an executable file exists
    def run(self, program):
        for func in program.functions:
            self.functions[func.name] = func

        if "main" not in self.functions: # If a main-file does not exist, then throw an error as there is no executable
            raise RuntimeError("No main-function found")
        return self.call_function("main", [])
    
    # Function to call functions - if they do not exists; throw error
    def call_function(self, name):
        func = self.functions.get(name)
        if not func: 
            raise RuntimeError(f"Unknown function: '{name}'")
        
    # Function to check if we are at an end of a function
    def is_at_end(self) -> bool:
        return len(self.functions) > self.position
         
    # Function to continue a function if it is not at the end
    def exefunc(self):
        while not self.is_at_end():
            pass
            


# Eksempel på logikken bag local og global_env
#integer x = 5;        // ligger i global_env

#nteger foo(integer y) {
#    integer z = 10;   // ligger i local_env
#    return x + y + z; // kan se ALLE tre variable
