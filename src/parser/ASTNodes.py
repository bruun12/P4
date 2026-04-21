class Node:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

class Statement(Node):
    def __init__(self, line: int, column: int):
        super().__init__(line, column)


class Expression(Node):
    def __init__(self, line: int, column: int):
        super().__init__(line, column)


#Statement nodes:
class Program(Node):
    def __init__(self, functions: list, line: int, column: int):
        super().__init__(line, column)
        self.functions = functions

class Function(Node):
    def __init__(self, return_type: str, name: str, parameters: list, statement: Statement, line: int, column: int):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.statement = statement
        
class Parameter(Node):
    def __init__(self, type: str, name: str, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
        
class BlockStatement(Statement):
    def __init__(self, statements: list, line: int, column: int):
        super().__init__(line, column)
        self.statements = statements

class VarDeclaration(Statement):
    def __init__(self, type: str, name: str, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
        self.value = value

class AssignStatement(Statement):
    def __init__(self, name: str, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.value = value

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: Statement, else_branch: Statement | None, line: int, column: int):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement, line: int, column: int):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

class ReturnStatement(Statement):
    def __init__(self, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.value = value

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression

class ArrayDeclaration(Statement): # integer arr = [1, 2, 3];
    def __init__(self, type: str, name: str, elements: list, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name 
        self.elements = elements # list[expression]
        self.size = len(elements)

class ArrayDeclarationEmpty(Statement): # integer arr[3];
    def __init__(self, type: str, name: str, size: Expression, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
        self.size = size
        

#Expression nodes
class Literal(Expression):
    def __init__(self, value, line: int, column: int):
        super().__init__(line, column)
        self.value = value

    def getValue(self):
        return self.value

class Variable(Expression):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(line, column)
        self.name = name

class FunctionCall(Expression):
    def __init__(self, name: str, arguments: list, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.arguments = arguments

class Unary(Expression):
    def __init__(self, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.operator = operator
        self.right = right

class Binary(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator

class Grouping(Expression):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression


#Error class
class ParserError(Exception):
    pass