class Node:
    pass


class Statement(Node):
    pass


class Expression(Node):
    pass



#Statement nodes:
class Program(Node):
    def __init__(self, functions: list):
        self.functions = functions

class Function(Node):
    def __init__(self, return_type: str, name: str, parameters: list, statement: Statement):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.statement = statement
        
class Parameter(Node):
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
        
class BlockStatement(Statement):
    def __init__(self, statements: list):
        self.statements = statements

class VarDeclaration(Statement):
    def __init__(self, type: str, name: str, value: Expression):
        self.type = type
        self.name = name
        self.value = value

class AssignStatement(Statement):
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: Statement, else_branch: Statement | None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

class ReturnStatement(Statement):
    def __init__(self, value: Expression):
        self.value = value

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

#Expression nodes
class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value

class Variable(Expression):
    def __init__(self, name: str):
        self.name = name

class Unary(Expression):
    def __init__(self, operator: str, right: Expression):
        self.operator = operator
        self.right = right

class Binary(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression


#Error class
class ParserError(Exception):
    pass
