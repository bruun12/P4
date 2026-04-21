class Node:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


class Statement(Node):
    pass


class Expression(Node):
    pass


# ============================================================
# Statement nodes
# ============================================================

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
    def __init__(self, statements: list, line: int, column: int):
        super().__init__(line, column)
        self.statements = statements


class VarDeclaration(Statement):
    def __init__(self, type: DataType, name: str, value: Expression):
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
    def __init__(self, value: Expression | None, line: int, column: int):
        super().__init__(line, column)
        self.value = value


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression

class ArrayDeclaration(Statement): # integer arr = [1, 2, 3];
    def __init__(self, type: DataType, name: str, elements: list):
        self.type = type
        self.name = name 
        self.elements = elements # list[expression]

class ArrayDeclarationEmpty(Statement): # integer arr[3];
    def __init__(self, type: str, name: str, size: Expression):
        self.type = type
        self.name = name
        self.size = size
        

#Expression nodes
class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Variable(Expression):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(line, column)
        self.name = name


class Unary(Expression):
    def __init__(self, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.operator = operator
        self.right = right


class Binary(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expression):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression


# ============================================================
# Error class
# ============================================================

class ParserError(Exception):
    pass