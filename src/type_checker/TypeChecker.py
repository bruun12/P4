
from __future__ import annotations
from dataclasses import dataclass

from parser.ASTNodes import (
    AssignStatement,
    Binary,
    BlockStatement,
    Expression,
    ExpressionStatement,
    IfStatement,
    Literal,
    Node,
    Program,
    ReturnStatement,
    Statement,
    Unary,
    Variable,
    WhileStatement,
    VarDeclaration,
    Function,
    Parameter,
    ArrayDeclaration,
    ArrayDeclarationEmpty,
    FunctionCall,
    ArrayAccess
)
from error_handling import ErrorCode, TypeCheckError, format_compiler_error


class Type:
    pass


@dataclass(frozen=True)
class IntegerType(Type):
    pass


@dataclass(frozen=True)
class DoubleType(Type):
    pass


@dataclass(frozen=True)
class BooleanType(Type):
    pass


@dataclass(frozen=True)
class StringType(Type):
    pass

@dataclass(frozen=True)
class VoidType(Type):
    pass


@dataclass(frozen=True)
class ErrorType(Type):
    pass


@dataclass(frozen=True)
class ArrayType(Type):
    """
    Array type with an element type.

    Example:
        ArrayType(INTEGER)
    """
    element_type: Type
    size: int


@dataclass(frozen=True)
class FunctionType(Type):
    """
    Function signature type.

    CHANGE APPLIED IN TYPECHECKER DESIGN:
    Because programs are now function-centered, the checker
    stores function signatures separately from local variables.
    """
    parameter_types: tuple[Type, ...] 
    return_type: Type


INTEGER = IntegerType()
DOUBLE = DoubleType()
BOOLEAN = BooleanType()
STRING = StringType()
VOID = VoidType()
ERROR = ErrorType()


# ============================================================
# FLOW RESULT
# ============================================================
"""
@dataclass(frozen=True)
class FlowResult:
    definitely_returns: bool


NO_FLOW = FlowResult(
    definitely_returns=False
)

RETURNS = FlowResult(
    definitely_returns=True
)
"""
# ============================================================
# ENVIRONMENTS
# ============================================================

class TypeEnvironment:
    """
    Nested variable environment for parameters and local variables.
    """
    def __init__(self, parent: "TypeEnvironment | None" = None):
        self.parent = parent
        self.values: dict[str, Type] = {}

    def define(self, name: str, type: Type) -> None:
        self.values[name] = type

    def contains_in_current_scope(self, name: str) -> bool:
        return name in self.values

    def get(self, name: str) -> Type:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise TypeCheckError(f"Undefined variable '{name}'.", ErrorCode.UNDEFINED_VARIABLE_ERROR, 0, 0)


class FunctionEnvironment:
    def __init__(self):
        self.values: dict[str, FunctionType] = {}

    def define(self, name: str, typ: FunctionType) -> None:
        self.values[name] = typ

    def contains_in_current_scope(self, name: str) -> bool:
        return name in self.values

    def get(self, name: str) -> FunctionType:
        if name in self.values:
            return self.values[name]
        raise TypeCheckError(f"Undefined function '{name}'.", ErrorCode.UNDEFINED_FUNCTION_ERROR, 0, 0)


# ============================================================
# HELPERS
# ============================================================
# Returns matching string of type object.
# Mainly used for printing.
def type_name(t: Type) -> str:
    if t == INTEGER:
        return "integer"
    if t == DOUBLE:
        return "double"
    if t == BOOLEAN:
        return "boolean"
    if t == STRING:
        return "string"
    if t == VOID:
        return "void"
    if t == ERROR:
        return "<error>"
    if isinstance(t, ArrayType):
        return f"{type_name(t.element_type)}[]"
    if isinstance(t, FunctionType):
        # 1. Convert each type object into its string name (e.g., [integer, float])
        name_list = []
        for p in t.parameter_types:
            name_list.append(type_name(p))

        # 2. Join them with commas (e.g., "integer, float")
        params_string = ", ".join(name_list)

        # 3. Build the final function signature
        return f"function({params_string}) -> {type_name(t.return_type)}"
    return repr(t)


def is_numeric(t: Type) -> bool:
    return t == INTEGER or t == DOUBLE


def can_assign(target: Type, value: Type) -> bool:

    if target == value:
        return True

    if target == DOUBLE and value == INTEGER:
        return True

    if isinstance(target, ArrayType) and isinstance(value, ArrayType):
        return can_assign(target.element_type, value.element_type)

    return False


def numeric_result_type(left: Type, right: Type) -> Type:
    if left == DOUBLE or right == DOUBLE:
        return DOUBLE
    return INTEGER


def parse_declared_type(declared_type: str) -> Type:

    if declared_type == "integer":
        return INTEGER
    if declared_type == "double":
        return DOUBLE
    if declared_type == "boolean":
        return BOOLEAN
    if declared_type == "string":
        return STRING
    if declared_type == "void":
        return VOID

    raise TypeCheckError(f"Unknown declared type '{declared_type}'.", ErrorCode.UNKNOWN_DECLARED_TYPE, 0, 0)


class TypeChecker:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.errors: list[TypeCheckError] = []

        # Global function signatures live here.
        self.function_env = FunctionEnvironment()

        # These are set while checking a function body.
        self.current_function_name: str | None = None
        self.expected_return_type: Type | None = None
        self.does_return_correctly: bool 

    # --------------------------------------------------------
    # Error helpers
    # --------------------------------------------------------

    def report(self, node: Node, error_code: ErrorCode, message: str) -> None:
        self.errors.append(TypeCheckError(message, error_code, node.line, node.column))

    def formatted_errors(self) -> list[str]:
        
        error_list = []

        for err in self.errors:
            error_list.append(format_compiler_error(err, self.source_lines))           
        return error_list

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    # --------------------------------------------------------
    # Type parsing helper
    # --------------------------------------------------------

    def parse_type_node(self, declared_type: str, node: Node) -> Type:
        """
        Parse a declared type and tie errors to the node that
        declared it.
        """
        try:
            return parse_declared_type(declared_type)
        except TypeCheckError as err:
            self.report(node, err.error_code, err.message)
            return ERROR
    
    def is_printable_type(self, t: Type) -> bool:
        return t in {INTEGER, DOUBLE, BOOLEAN, STRING}


    def check(self, program: Program) -> None:

        self.collect_function_signatures(program)
        self.check_all_functions(program)

    def collect_function_signatures(self, program: Program) -> None:
        for function in program.functions:
            if self.function_env.contains_in_current_scope(function.name):
                self.report(function, ErrorCode.ALREADY_DECLARED_ERROR, f"Function '{function.name}' is already declared.")
                continue

            return_type = self.parse_type_node(function.return_type, function)

            parameter_types: list[Type] = []
            for parameter in function.parameters:
                param_type = self.parse_type_node(parameter.type, parameter)
                parameter_types.append(param_type)

            self.function_env.define(
                function.name,
                FunctionType(
                    parameter_types=tuple(parameter_types),
                    return_type=return_type,
                )
            )

    # --------------------------------------------------------
    # Pass 2: check each function body
    # --------------------------------------------------------

    def check_all_functions(self, program: Program) -> None:
        for function in program.functions:
            self.check_function(function)

    def check_function(self, function: Function) -> None:
        # Every time a new function is checked, the current function name and 
        # expected return type is set on the TypeChecker object
        previous_function_name = self.current_function_name
        previous_expected_return_type = self.expected_return_type

        self.current_function_name = function.name
        self.expected_return_type = self.parse_type_node(function.return_type, function)

        local_env = TypeEnvironment()

        # Add parameters as local variables
        for parameter in function.parameters:
            param_type = self.parse_type_node(parameter.type, parameter)
            
            if param_type == VOID:
                self.report(
                    parameter,
                    ErrorCode.INVALID_PARAMETER_TYPE,
                    f"Parameter '{parameter.name}' cannot have type void."
                )
                
            if local_env.contains_in_current_scope(parameter.name):
                self.report(
                    parameter, 
                    ErrorCode.ALREADY_DECLARED_ERROR,
                    f"Duplicate parameter '{parameter.name}' in function '{function.name}'."
                    )
                continue

            local_env.define(parameter.name, param_type)
        
        self.does_return_correctly = False
        self.check_statement(function.statement, local_env, True)
        
       
        # Enforce that the function returns correctly.
        if self.expected_return_type not in (VOID, ERROR) and not self.does_return_correctly:
            self.report(
                function,
                ErrorCode.MISSING_RETURN_ERROR,
                f"Function '{function.name}' must include return statement at the end."
            )
        self.current_function_name = previous_function_name
        self.expected_return_type = previous_expected_return_type

    # --------------------------------------------------------
    # Statement checking
    # --------------------------------------------------------

    def check_statement(
        self,
        stmt: Statement,
        env: TypeEnvironment,
        within_function: bool
         ) -> None:

        # ----------------------------------------------------
        # BlockStatement
        # ----------------------------------------------------

        if isinstance(stmt, BlockStatement):
            block_env = TypeEnvironment(parent=env)

            for i, inner_stmt in enumerate(stmt.statements):
                is_last_statement = i == len(stmt.statements) - 1

                inner_within_function = within_function and is_last_statement

                self.check_statement(inner_stmt, block_env, inner_within_function)

            return

        # ----------------------------------------------------
        # VarDeclaration
        # ----------------------------------------------------
        if isinstance(stmt, VarDeclaration):
            #Returns a Type object that matches the type declared in the statement
            #parse_type_node will raise an TypeCheckError and append it self.errors if type is unknown
            declared_type = self.parse_type_node(stmt.type, stmt)
            
            #Void is not allowed as a declared type
            if declared_type == VOID:
                self.report(
                    stmt, 
                    ErrorCode.INVALID_DECLARED_TYPE,
                    f"Variable '{stmt.name}' cannot have type void."
                    )
            value_type = self.check_expression(stmt.value, env)
            
            #Check if a variable name already is in the environment
            if env.contains_in_current_scope(stmt.name):
                self.report(
                    stmt, 
                    ErrorCode.ALREADY_DECLARED_ERROR,
                    f"Variable '{stmt.name}' is already declared in this scope."
                    )
            #If declared type and value type cannot be assigned
            if declared_type != ERROR and value_type != ERROR:
                if not can_assign(declared_type, value_type):
                    self.report(
                        stmt.value,
                        ErrorCode.CANNOT_ASSIGN,
                        f"Cannot initialize variable '{stmt.name}' of type "
                        f"{type_name(declared_type)} with value of type {type_name(value_type)}."
                    )
            #Variable is defined in current environment
            env.define(stmt.name, declared_type)
            return

        # ----------------------------------------------------
        # ArrayDeclaration
        # ----------------------------------------------------
        if isinstance(stmt, ArrayDeclaration):
            element_type = self.parse_type_node(stmt.type, stmt)
            if element_type == VOID:
                self.report(
                    stmt, 
                    ErrorCode.INVALID_DECLARED_TYPE,
                    f"Array '{stmt.name}' cannot have element type void."
                    )
            
            size_type = self.check_expression(stmt.size, env)
            if size_type != ERROR and size_type != INTEGER:
                self.report(
                    stmt.size,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Array size must be integer, got {type_name(size_type)}."
                )
            #Create ArrayType object
            array_type_size = ArrayType(element_type, stmt.size.value)
        
            if env.contains_in_current_scope(stmt.name):
                self.report(
                    stmt, 
                    ErrorCode.ALREADY_DECLARED_ERROR,
                    f"Variable '{stmt.name}' is already declared in this scope."
                    )
            if stmt.size.value != len(stmt.elements):
                self.report(
                        stmt,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        f"Array size must match number or declared array elements"
                        f" Expected {stmt.size.value} number of elements, but got {len(stmt.elements)}."
                    )
                
            for element in stmt.elements:
                element_expr_type = self.check_expression(element, env)
                if element_type != ERROR and element_expr_type != ERROR:
                    if not can_assign(element_type, element_expr_type):
                        self.report(
                            element,
                            ErrorCode.CANNOT_ASSIGN,
                            f"Cannot place element of type {type_name(element_expr_type)} "
                            f"into array '{stmt.name}' of element type {type_name(element_type)}."
                        )

            env.define(stmt.name, array_type_size)
            return 

        # ----------------------------------------------------
        # ArrayDeclarationEmpty
        # ----------------------------------------------------
        if isinstance(stmt, ArrayDeclarationEmpty):
            element_type = self.parse_type_node(stmt.type, stmt)
            if element_type == VOID:
                self.report(
                    stmt, 
                    ErrorCode.INVALID_DECLARED_TYPE,
                    f"Array '{stmt.name}' cannot have element type void."
                    )
            array_type_size = ArrayType(element_type, stmt.size.value)

            if env.contains_in_current_scope(stmt.name):
                self.report(
                    stmt, 
                    ErrorCode.ALREADY_DECLARED_ERROR,
                    f"Variable '{stmt.name}' is already declared in this scope."
                    )

            size_type = self.check_expression(stmt.size, env)
            if size_type != ERROR and size_type != INTEGER:
                self.report(
                    stmt.size,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Array size must be integer, got {type_name(size_type)}."
                )

            env.define(stmt.name, array_type_size)
            return

        # ----------------------------------------------------
        # AssignStatement
        # ----------------------------------------------------
        if isinstance(stmt, AssignStatement):
            try:
                target_type = env.get(stmt.name)
            except TypeCheckError:
                self.report(
                    stmt,
                    ErrorCode.UNDEFINED_VARIABLE_ERROR,
                    f"Undefined variable '{stmt.name}'."
                )
                target_type = ERROR
            
            # Normal assignment: x = value;
            if stmt.offset is None:
                value_type = self.check_expression(stmt.value, env)

                if target_type != ERROR and value_type != ERROR:
                    if not can_assign(target_type, value_type):
                        self.report(
                            stmt.value,
                            ErrorCode.CANNOT_ASSIGN,
                            f"Cannot assign value of type {type_name(value_type)} "
                            f"to variable '{stmt.name}' of type {type_name(target_type)}."
                        )

                return

            # Array assignment: arr[index] = value;
            if target_type != ERROR and not isinstance(target_type, ArrayType):
                self.report(
                    stmt,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Variable '{stmt.name}' is not an array, so it cannot be indexed."
                )
                # Still check subexpressions so their own errors are not hidden
                self.check_expression(stmt.offset, env)
                self.check_expression(stmt.value, env)
                return 

            offset_type = self.check_expression(stmt.offset, env)
            value_type = self.check_expression(stmt.value, env)

            if offset_type != ERROR and offset_type != INTEGER:
                self.report(
                    stmt.offset,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Array index must be integer, got {type_name(offset_type)}."
                )
            if isinstance(stmt.offset, Literal) and isinstance(stmt.offset.value, int):    
                if stmt.offset.value < 0:
                    self.report(
                        stmt.offset,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        f"Array index must be positive, got {stmt.offset.value}."
                    )
            if stmt.offset.value > target_type.size:
                    self.report(
                        stmt.offset,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        f"Element assigned to array index is out of range."
                        f" Array maximum index: {target_type.size} but tries to assign to index: {stmt.offset.value}"
                    )                
                
            if isinstance(target_type, ArrayType) and value_type != ERROR:
                element_type = target_type.element_type

                if not can_assign(element_type, value_type):
                    self.report(
                        stmt.value,
                        ErrorCode.CANNOT_ASSIGN,
                        f"Cannot assign value of type {type_name(value_type)} "
                        f"to array '{stmt.name}' element of type {type_name(element_type)}."
                    )

            return 

        # ----------------------------------------------------
        # IfStatement
        # ----------------------------------------------------
        if isinstance(stmt, IfStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != ERROR and condition_type != BOOLEAN:
                self.report(
                    stmt.condition,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"If condition must be boolean, got {type_name(condition_type)}."
                )

            then_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.then_branch, then_env, False)

            if stmt.else_branch is None:
                return

            else_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.else_branch, else_env, False)
            # Return flow result based on if then and else block definitely return,
            return 
    
        # ----------------------------------------------------
        # WhileStatement
        # ----------------------------------------------------
        if isinstance(stmt, WhileStatement):
            condition_type = self.check_expression(stmt.condition, env)

            if condition_type != ERROR and condition_type != BOOLEAN:
                self.report(
                    stmt.condition,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"While condition must be boolean, got {type_name(condition_type)}."
                )

            body_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.body, body_env, False)

            return

        # ----------------------------------------------------
        # ReturnStatement
        # ----------------------------------------------------
        if isinstance(stmt, ReturnStatement):
            if not within_function:
                self.report(
                    stmt,
                    ErrorCode.INVALID_RETURN_ERROR,
                    "Return statement is only allowed as the final statement of a function."
                    )  
                return
                 
            if self.expected_return_type is None:
                self.report(
                    stmt, 
                    ErrorCode.INVALID_RETURN_ERROR,
                    "Return statement is not allowed here."
                    )
                return

            if stmt.value is None:
                if self.expected_return_type == VOID:
                    self.does_return_correctly = True
                    return 
                
                self.report(
                    stmt,
                    ErrorCode.INVALID_RETURN_ERROR,
                    f"Return statement must include a value of type "
                    f"{type_name(self.expected_return_type)}."
                )
                self.does_return_correctly = False
                return 
           
            if self.expected_return_type == VOID:
               
                self.check_expression(stmt.value, env)
                self.report(
                    stmt.value,
                    ErrorCode.INVALID_RETURN_ERROR,
                    "Void function must not return a value."
                )
                self.does_return_correctly = False
               # still check the expression so errors inside it are found
                return
            
            value_type = self.check_expression(stmt.value, env)

            if value_type != ERROR and not can_assign(self.expected_return_type, value_type):
                self.report(
                    stmt.value,
                    ErrorCode.INVALID_RETURN_ERROR,
                    f"Return type mismatch in function '{self.current_function_name}': "
                    f"expected {type_name(self.expected_return_type)}, got {type_name(value_type)}."
                )
            self.does_return_correctly = True
            return 

        # ----------------------------------------------------
        # ExpressionStatement
        # ----------------------------------------------------
        if isinstance(stmt, ExpressionStatement):
            self.check_expression(stmt.expression, env)
            return
        # !r uses repr() for a detailed, quoted debug view
        # repr() used to clarify type and content
        self.report(
            stmt,
            ErrorCode.UNKNOWN_AST_NODE_ERROR,
            f"Unknown statement node: {stmt!r}"
            )
        return

    # --------------------------------------------------------
    # Expression checking
    # --------------------------------------------------------

    def check_expression(self, expr: Expression, env: TypeEnvironment) -> Type:
        if isinstance(expr, FunctionCall):
            
            if expr.name == "print":
                if len(expr.arguments) == 0:
                    self.report(
                        expr,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        "Function 'print' expects at least 1 argument."
                    )
                    return ERROR

                for argument in expr.arguments:
                    argument_type = self.check_expression(argument, env)

                    if argument_type != ERROR and not self.is_printable_type(argument_type):
                        self.report(
                            argument,
                            ErrorCode.TYPE_MISMATCH_ERROR,
                            f"Function 'print' cannot print value of type {type_name(argument_type)}."
                        )

                return VOID

            #Check if the function name exists in the function environment 
            #Return function object if it exist, else return type check error
            try:    
                function_type = self.function_env.get(expr.name)
            except TypeCheckError:
                self.report(expr, ErrorCode.UNDEFINED_FUNCTION_ERROR, f"Undefined function '{expr.name}'.")
                return ERROR

            expected_count = len(function_type.parameter_types)
            actual_count = len(expr.arguments)
            # Compare expected parameter count to the argument count from the function call
            if actual_count != expected_count:
                self.report(
                    expr,
                    ErrorCode.INVALID_ARGUMENT_COUNT,
                    f"Function '{expr.name}' expects {expected_count} argument(s), "
                    f"but got {actual_count}."
                )
                return ERROR
            #Check all argument types against the expected parameter types
            for i in range(actual_count):
                argument_expr = expr.arguments[i]
                parameter_type = function_type.parameter_types[i]
        
                argument_type = self.check_expression(argument_expr, env)

                if argument_type != ERROR and not can_assign(parameter_type, argument_type):
                    self.report(
                        argument_expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Argument {i + 1} of function '{expr.name}' has type "
                        f"{type_name(argument_type)}, but expected {type_name(parameter_type)}."
                    )

            return function_type.return_type
        
        if isinstance(expr, ArrayAccess):
            try:
                array_type = env.get(expr.name)
            except TypeCheckError:
                self.report(
                    expr,
                    ErrorCode.UNDEFINED_VARIABLE_ERROR,
                    f"Undefined variable '{expr.name}'."
                )
                return ERROR
        
            if not isinstance(array_type, ArrayType):
                self.report(
                    expr,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Variable '{expr.name}' is not an array, so it cannot be indexed."
                )
                # Still check the offset so errors inside it are not hidden
                self.check_expression(expr.offset, env)
                return ERROR
        
            offset_type = self.check_expression(expr.offset, env)
        
            if offset_type != ERROR and offset_type != INTEGER:
                self.report(
                    expr.offset,
                    ErrorCode.TYPE_MISMATCH_ERROR,
                    f"Array index must be integer, got {type_name(offset_type)}."
                )
                return ERROR
            return array_type.element_type
        
        if isinstance(expr, Literal):
            value = expr.value

            # bool before int because Python bool is a subclass of int
            if isinstance(value, bool):
                return BOOLEAN

            if isinstance(value, int):
                return INTEGER

            if isinstance(value, float):
                return DOUBLE

            if isinstance(value, str):
                return STRING

            self.report(
                expr, 
                ErrorCode.TYPE_MISMATCH_ERROR,
                f"Unsupported literal value {value!r}."
                )
            return ERROR

        if isinstance(expr, Variable):
            try:
                return env.get(expr.name)
            except TypeCheckError:
                self.report(
                    expr, 
                    ErrorCode.UNDEFINED_VARIABLE_ERROR, 
                    f"Undefined variable '{expr.name}'."
                    )
                return ERROR

        if isinstance(expr, Unary):
            right_type = self.check_expression(expr.right, env)

            if right_type == ERROR:
                return ERROR

            if expr.operator == "-":
                if not is_numeric(right_type):
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Unary '-' requires integer or double, got {type_name(right_type)}."
                    )
                    return ERROR
                return right_type

            if expr.operator == "!":
                if right_type != BOOLEAN:
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Unary '!' requires boolean, got {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN
            #This should never run if parser works correctly
            self.report(expr, f"Unknown unary operator '{expr.operator}'.")
            return ERROR

        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            if left_type == ERROR or right_type == ERROR:
                return ERROR

            # Arithmetic
            if op in {"+", "-", "*", "/", "MOD"}:
                if op == "+" and left_type == STRING and right_type == STRING:
                    return STRING

                if not is_numeric(left_type) or not is_numeric(right_type):
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Operator '{op}' requires numeric operands "
                        f"(or string + string for '+'), got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR

                return numeric_result_type(left_type, right_type)

            # Comparison
            if op in {"<", "<=", ">", ">="}:
                if not is_numeric(left_type) or not is_numeric(right_type):
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Operator '{op}' requires numeric operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Equality
            if op in {"==", "!="}:
                if left_type != right_type:
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Operator '{op}' requires both sides to have the same type, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            # Logical 
            if op in {"AND", "OR"}:
                if left_type != BOOLEAN or right_type != BOOLEAN:
                    self.report(
                        expr,
                        ErrorCode.TYPE_MISMATCH_ERROR,
                        f"Operator '{op}' requires boolean operands, got "
                        f"{type_name(left_type)} and {type_name(right_type)}."
                    )
                    return ERROR
                return BOOLEAN

            self.report(
                expr,
                ErrorCode.UNKNOWN_AST_NODE_ERROR,
                f"Unknown binary operator '{op}'."
                )
            return ERROR

        self.report(
            expr, 
            ErrorCode.UNKNOWN_AST_NODE_ERROR,
            f"Unknown expression node: {expr!r}"
            )
        return ERROR


# ============================================================
# OPTIONAL CONVENIENCE RUNNER
# ============================================================

def run_typecheck(program: Program, source_code: str) -> None:
    checker = TypeChecker(source_code)
    checker.check(program)

    if checker.errors:
        for err in checker.formatted_errors():
            print(err)
            print()
    else:
        print("Type check passed.")