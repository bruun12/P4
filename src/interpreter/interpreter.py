

class ReturnException(Exception): #Funktionen er til at give mulighed til en genvej ud af funktionen
    def __init__(self, value): # For eksempel i et for loop, vil vi være 4 lag nede inden et return
        self.value = value

# Denne klasse er til at gemme vores værdier
class Environment:
    def __init__(self, parent=None): # Parent er scope 
        self.vars = {}
        self.parent = parent
    
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Unknown Variable: '{name}'")
    
    def set(self, name, value): # Bruger den her funktion til at oprette en ny variable i vores nuværende scope
        self.vars[name] = value # Bliver brugt ved x = 10; 
    
    def assign(self, name, value):
        if name in self.vars: # Tjekker efter variable i scopet 
            self.vars[name] = value # HVis ja opdaterer 
            return
        if self.parent: # Har vi et parent scope hvis ja brug den eller kast en error
            self.parent.assign(name, value)
            return
        raise RuntimeError(f"Variable not assigned: '{name}'")

class Interpreter:
    def __init__(self):
        self.functions = {}
        self.global_env = Environment()

    def run(self, program):
        for func in program.functions:
            self.functions[func.name] = func

        if "main" not in self.functions:
            raise RuntimeError("No main-function found")
        return self.call_function("main", [])
    
    def call_function(self, name, args):
        func = self.functions.get(name)
        if not func: 
            raise RuntimeError(f"Unknown function: '{name}'")


# Eksempel på logikken bag local og global_env
#integer x = 5;        // ligger i global_env

#nteger foo(integer y) {
#    integer z = 10;   // ligger i local_env
#    return x + y + z; // kan se ALLE tre variable
#}