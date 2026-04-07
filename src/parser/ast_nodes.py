class ASTNode: 
    pass

#following the structure from concreteSyntax.txt
class Program(ASTNode):
    def __init__(self, funcList):
        self.funcList = funcList

class FuncDef(ASTNode):
    def __init__(self, returnType, name, params, statements):
        self.returnType = returnType
        self.name = name
        self.params = params
        self.statements = statements

class Param(ASTNode):
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier


#Our different types of statements

class varDeclartion(ASTNode):
    def __init__(self, type, name, expression):
        self.type = type
        self.name = name 
        self.expression = expression

class varAssignment(ASTNode):
    def __init__(self, name, expression):
        self.name = name
        self.value = expression
        