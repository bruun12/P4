import json

class Node:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def to_dict(self):
        return {"type": self.__class__.__name__}
    
    def to_c(self):
        raise NotImplementedError(f"to_c is not implemented for {__class__.__name__}")

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
    
    def to_dict(self):
        return {
            "type": "Program",
            "functions": [func.to_dict() for func in self.functions]
        }

    def to_c(self):
        functionList = ""
        for func in self.functions:
            functionList += func.to_c() + "\n"

        return f"""
                    #include <stdio.h>
                    #include <stdbool.h>
                    {functionList}
                """

class Function(Node):
    def __init__(self, return_type: str, name: str, parameters: list, statement: Statement, line: int, column: int):
        super().__init__(line, column)
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.statement = statement
    
    def to_dict(self):
        return {
            "type": "Function",
            "name": self.name,
            "return_type": self.return_type,
            "parameters": [param.to_dict() for param in self.parameters],
            "body": self.statement.to_dict()
        }
    
    def to_c(self):
        type_map = {
            'integer': 'int',
            'double': 'float',
            'string': 'char*',
            'void': 'void'
        }
        paraList = ""
        for param in self.parameters:
            paraList += param.to_c() + ","
        return f"{type_map[self.return_type]} {self.name}({paraList[:-1]}) {self.statement.to_c()}"
        
class Parameter(Node):
    def __init__(self, type: str, name: str, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
    
    def to_dict(self):
        return {
            "type": "Parameter",
            "param_type": self.type,
            "name": self.name
        }
    
    def to_c(self):
        type_map = {
            'integer': 'int',
            'double': 'float',
            'string': 'char*',
            'boolean': 'bool',
            'void': 'void'
        }
        if(self.type == 'string'):
            return f"{type_map[self.type]} {self.name}[]"
        else:
            return f"{type_map[self.type]} {self.name}"
        
class BlockStatement(Statement):
    def __init__(self, statements: list, line: int, column: int):
        super().__init__(line, column)
        self.statements = statements
    
    def to_dict(self):
        return {
            "type": "Block",
            "body": [stmt.to_dict() for stmt in self.statements]
        }

    def to_c(self):
        stmtList = ""
        for stmt in self.statements:
            stmtList += stmt.to_c() + "\n"
        return f"""{{
            {stmtList}
            }}"""


class VarDeclaration(Statement):
    def __init__(self, type: str, name: str, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
        self.value = value
    
    def to_dict(self):
        return {
            "type": "VarDeclaration",
            "var_type": self.type,
            "name": self.name,
            "value": self.value.to_dict() if self.value else None
        }
    
    def to_c(self):
        type_map = {
            'integer': 'int',
            'double': 'float',
            'string': 'char',
            'boolean': 'bool'
        }
        if(self.type == 'string'):
            return f"{type_map[self.type]} {self.name}[] = {self.value.to_c()};" 
        else:
            return f"{type_map[self.type]} {self.name} = {self.value.to_c()};" 
         

class AssignStatement(Statement):
    def __init__(self, name: str, offset: Expression, value: Expression, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.offset = offset
        self.value = value
    
    def to_dict(self):
        if self.offset is None:
            return {
                "type": "Assign",
                "name": self.name,
                "value": self.value.to_dict()
            }
        return {
                "type": "Assign",
                "name": self.name,
                "offset": self.offset.to_dict(),
                "value": self.value.to_dict()
            }

    def to_c(self):
        if self.offset is None:
            return f"{self.name} = {self.value.to_c()};"
        else:
            return f"{self.name}[{self.offset.to_c()}] = {self.value.to_c()};"

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: Statement, else_branch: Statement | None, line: int, column: int):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def to_dict(self):
        result = {
            "type": "If",
            "condition": self.condition.to_dict(),
            "then": self.then_branch.to_dict() if isinstance(self.then_branch, BlockStatement) else [self.then_branch.to_dict()]
        }
        if self.else_branch:
            result["else"] = self.else_branch.to_dict() if isinstance(self.else_branch, BlockStatement) else [self.else_branch.to_dict()]
        return result
    
    def to_c(self):
        if self.else_branch is None:
            return f"""if ({self.condition.to_c()})
                        {self.then_branch.to_c()}
                    """
        else:
            return f"""if ({self.condition.to_c()})
                        {self.then_branch.to_c()}
                    else 
                        {self.else_branch.to_c()}
                    """

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement, line: int, column: int):
        super().__init__(line, column)
        self.condition = condition
        self.body = body
    
    def to_dict(self):
        return {
            "type": "While",
            "condition": self.condition.to_dict(),
            "body": self.body.to_dict() if isinstance(self.body, BlockStatement) else [self.body.to_dict()]
        }

    def to_c(self):
        return f"""while ({self.condition.to_c()})
        {self.body.to_c()}"""

class ReturnStatement(Statement):
    def __init__(self, value: Expression | None, line: int, column: int):
        super().__init__(line, column)
        self.value = value
    
    def to_dict(self):
        result = {"type": "Return"}
        if self.value:
            result["value"] = self.value.to_dict()
        return result
    
    def to_c(self):
        if self.value is not None:
            return f"return {self.value.to_c()};"
        else:
            return "return;"

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression, line: int, column: int):
        super().__init__(line, column)
        self.expression = expression
    
    def to_dict(self):
        return {
            "type": "Expression",
            "value": self.expression.to_dict()
        }
    
    def to_c(self):
        return f"{self.expression.to_c()};"

class ArrayDeclaration(Statement):
    def __init__(self, type: str, name: str, elements: list, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name 
        self.elements = elements
        self.size = len(elements)
    
    def to_dict(self):
        return {
            "type": "ArrayDeclaration",
            "array_type": self.type,
            "name": self.name,
            "elements": [elem.to_dict() for elem in self.elements],
            "size": self.size
        }
    
    def to_c(self):
        type_map = {
            'integer': 'int',
            'double': 'float',
            'string': 'char*',
        }
        arrElements = ""
        for elements in self.elements:
            arrElements += elements.to_c() + ","
        return f"{type_map[self.type]} {self.name}[] = {{{arrElements[:-1]}}};"

class ArrayDeclarationEmpty(Statement):
    def __init__(self, type: str, name: str, size: Expression, line: int, column: int):
        super().__init__(line, column)
        self.type = type
        self.name = name
        self.size = size
    
    def to_dict(self):
        return {
            "type": "ArrayDeclarationEmpty",
            "array_type": self.type,
            "name": self.name,
            "size": self.size.to_dict()
        }
        
    def to_c(self):
        type_map = {
            'integer': 'int',
        }
        return f"{type_map[self.type]} {self.name}[{self.size.to_c()}];"

#Expression nodes
class Literal(Expression):
    def __init__(self, value, line: int, column: int):
        super().__init__(line, column)
        self.value = value
    
    def to_dict(self):
        value_type = type(self.value).__name__
        if value_type == "int":
            return {"type": "integer", "value": self.value}
        elif value_type == "float":
            return {"type": "double", "value": self.value}
        elif value_type == "bool":
            return {"type": "boolean", "value": self.value}
        elif value_type == "str":
            return {"type": "string", "value": self.value}
        else:
            return {"type": "literal", "value": self.value}

    def to_c(self):
        value_type = type(self.value).__name__
        if value_type == "int":
            return f"{self.value}"
        if value_type == "float":
            return f"{self.value}"
        if value_type == "bool":
            return f"{self.value}".lower()
        if value_type == "str":
            return f'"{self.value}"'
        else:
            return f"{self.value}"

class Variable(Expression):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(line, column)
        self.name = name
    
    def to_dict(self):
        return {
            "type": "variable",
            "name": self.name
        }
    
    def to_c(self):
        return f"{self.name}"

class FunctionCall(Expression):
    def __init__(self, name: str, arguments: list, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.arguments = arguments
    
    def to_dict(self):
        return {
            "type": "FunctionCall",
            "name": self.name,
            "arguments": [arg.to_dict() for arg in self.arguments]
        }

    def to_c(self):
        if(self.name == "print"):
            return self.to_print()
        else:
            argString = ""
            for arg in self.arguments:
                argString += arg.to_c() + ","
            

            #argString[:-1] removes the last comma
            return f"{self.name}({argString[:-1]})"
    
    def to_print(self):
        a = f"if(sizeof({self.arguments[0].to_c()})==8)"
        b = """{printf("%f","""
        c = f"{self.arguments[0].to_c()});"
        d = "}else if(sizeof("
        e = f"{self.arguments[0].to_c()})==4)"
        f ="""{printf("%d","""
        g = f"{self.arguments[0].to_c()});"
        h = """}else{printf("%s","""
        i = f"{self.arguments[0].to_c()});"
        k = "}"
        
        s = a + b + c + d + e + f + g + h + i + k

        return s

        #self.name = "printf"
        #s = ""
        #for arg in self.arguments:
        #    if type(arg.value).__name__ == "str":
        #        s = s + arg.to_c() + ","
        #    if type(arg.value).__name__ == "int":
        #        s = s + "%d,"
        #    if type(arg.value).__name__ == "float":
        #        s = s + "%f,"
        #    if type(arg.value).__name__ == "bool":
        #        s = s + "%b,"
        #return s




class Unary(Expression):
    def __init__(self, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.operator = operator
        self.right = right
    
    def to_dict(self):
        return {
            "type": "UnaryOp",
            "op": self.operator,
            "right": self.right.to_dict()
        }
    
    def to_c(self):
        return f"{self.operator}{self.right.to_c()}" 

class Binary(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression, line: int, column: int):
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator
    
    def to_dict(self):
        # Map operator symbols to their string representations if needed
        op_map = {
            '+': '+', '-': '-', '*': '*', '/': '/', '%': '%',
            '==': '==', '!=': '!=', '<': '<', '<=': '<=', '>': '>', '>=': '>=',
            '&&': 'and', '||': 'or'
        }
        return {
            "type": "BinaryOp",
            "op": op_map.get(self.operator, self.operator),
            "left": self.left.to_dict(),
            "right": self.right.to_dict()
        }

    def to_c(self):
        op_map = {
            '+': '+', '-': '-', '*': '*', '/': '/', 'MOD': '%',
            '==': '==', '!=': '!=', '<': '<', '<=': '<=', '>': '>', '>=': '>=',
            'AND': '&&', 'OR': '||'
        }
        return f"({self.left.to_c()} {op_map.get(self.operator, self.operator)} {self.right.to_c()})"
    
class ArrayAccess(Expression):
    def __init__(self, name: str, offset: Expression, line: int, column: int):
        super().__init__(line, column)
        self.name = name
        self.offset = offset

    def to_dict(self):
        return {
            "type": "ArrayAccess",
            "name": self.name, 
            "offset": self.offset.to_dict()
        }
    
    def to_c(self):
        return f"{self.name}[{self.offset.to_c()}]"

#Error class
class ParserError(Exception):
    pass