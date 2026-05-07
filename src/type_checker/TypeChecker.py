from __future__ import annotations
from error_handling import ErrorCode, TypeCheckError, format_compiler_error

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
from type_checker.ClassesAndHelpers import (
    Type,
    INTEGER,
    DOUBLE,
    BOOLEAN,
    STRING,
    VOID,
    ERROR,
    ArrayType,
    FunctionType,
    type_name,
    is_numeric,
    can_assign,
    numeric_result_type,
    parse_declared_type
)


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
    """Flat registry of function signatures collected before body checking."""
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

class TypeChecker:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.source_lines = source_code.splitlines()
        self.errors: list[TypeCheckError] = []

        # Pass 1 stores every function signature here so calls can be checked
        # before or while later function bodies are analyzed.
        self.function_env = FunctionEnvironment()

        # These fields track the active function while its body is being checked.
        self.current_function_name: str | None = None
        self.expected_return_type: Type | None = None
        self.does_return_correctly: bool 

    # --------------------------------------------------------
    # Error helpers
    # --------------------------------------------------------

    def report(self, node: Node, error_code: ErrorCode, message: str) -> None:
        self.errors.append(TypeCheckError(message, error_code, node.line, node.column))

    def formatted_errors(self) -> list[str]:
        # Keep source-aware formatting separate from error collection so the
        # checker can accumulate multiple diagnostics in one pass.
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
        # Run in two passes: first collect all signatures, then validate bodies.
        self.collect_function_signatures(program)
        self.check_all_functions(program)

    def collect_function_signatures(self, program: Program) -> None:
        # This pass makes function calls order-independent.
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
        # Save outer function state in case nested checking reuses the same
        # TypeChecker instance in the future.
        previous_function_name = self.current_function_name
        previous_expected_return_type = self.expected_return_type

        self.current_function_name = function.name
        self.expected_return_type = self.parse_type_node(function.return_type, function)

        # Each function starts with a fresh local scope containing parameters.
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
        
        # This flag is updated only when a structurally valid final return is seen.
        self.does_return_correctly = False
        self.check_statement(function.statement, local_env, True)
        
        # Non-void functions must end in a valid return on the final path.
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
            # Blocks introduce a nested scope but inherit access to outer names.
            block_env = TypeEnvironment(parent=env)

            for i, inner_stmt in enumerate(stmt.statements):
                is_last_statement = i == len(stmt.statements) - 1

                # Only the last statement in the active function body may count
                # as the function's required return statement.
                inner_within_function = within_function and is_last_statement

                self.check_statement(inner_stmt, block_env, inner_within_function)

            return

        # ----------------------------------------------------
        # VarDeclaration
        # ----------------------------------------------------
        if isinstance(stmt, VarDeclaration):
            # Resolve the declared type first so later checks can compare against it.
            declared_type = self.parse_type_node(stmt.type, stmt)
            
            # Variables must always hold a material value type.
            if declared_type == VOID:
                self.report(
                    stmt, 
                    ErrorCode.INVALID_DECLARED_TYPE,
                    f"Variable '{stmt.name}' cannot have type void."
                    )
            value_type = self.check_expression(stmt.value, env)
            
            # Reject shadowing within the same scope while still allowing outer
            # scope names to exist in parent environments.
            if env.contains_in_current_scope(stmt.name):
                self.report(
                    stmt, 
                    ErrorCode.ALREADY_DECLARED_ERROR,
                    f"Variable '{stmt.name}' is already declared in this scope."
                    )

            # Initializer type must be assignable to the declared variable type.
            if declared_type != ERROR and value_type != ERROR:
                if not can_assign(declared_type, value_type):
                    self.report(
                        stmt.value,
                        ErrorCode.CANNOT_ASSIGN,
                        f"Cannot initialize variable '{stmt.name}' of type "
                        f"{type_name(declared_type)} with value of type {type_name(value_type)}."
                    )

            # Keep the binding even after an error so later uses report against a
            # stable environment instead of cascading as undefined-variable errors.
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

            # Arrays carry both element type and declared size for later bounds checks.
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
                
            # Every literal initializer is validated against the declared element type.
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

            # Empty arrays still enter the environment with full static shape info.
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
            
            # Scalar assignment reuses the same assignability rules as declarations.
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

            # Indexed assignment additionally validates the target shape and index.
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

            # Literal indices are checked statically; non-literals are only type-checked.
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

            # Branches get isolated child scopes so declarations do not leak out.
            then_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.then_branch, then_env, False)

            if stmt.else_branch is None:
                return

            else_env = TypeEnvironment(parent=env)
            self.check_statement(stmt.else_branch, else_env, False)
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

            # Loop bodies type-check in their own scope but never guarantee a return.
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

            # Void functions may only return without a value.
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
                # Still type-check the expression to preserve diagnostics inside it.
                self.check_expression(stmt.value, env)
                self.report(
                    stmt.value,
                    ErrorCode.INVALID_RETURN_ERROR,
                    "Void function must not return a value."
                )
                self.does_return_correctly = False
                return
            
            value_type = self.check_expression(stmt.value, env)

            # Non-void returns are validated with the same assignment rules used
            # elsewhere, allowing compatible numeric widening if supported.
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
            # `print` is treated as a built-in rather than a user-declared function.
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

            # User-defined calls are checked against the signature table built in pass 1.
            try:    
                function_type = self.function_env.get(expr.name)
            except TypeCheckError:
                self.report(expr, ErrorCode.UNDEFINED_FUNCTION_ERROR, f"Undefined function '{expr.name}'.")
                return ERROR

            expected_count = len(function_type.parameter_types)
            actual_count = len(expr.arguments)

            # Arity mismatch is reported before per-argument checks to avoid index issues.
            if actual_count != expected_count:
                self.report(
                    expr,
                    ErrorCode.INVALID_ARGUMENT_COUNT,
                    f"Function '{expr.name}' expects {expected_count} argument(s), "
                    f"but got {actual_count}."
                )
                return ERROR

            # Each argument is checked independently so multiple mismatches can be reported.
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

            # Bounds can only be checked statically when the index is a literal integer.
            if isinstance(expr.offset, Literal) and isinstance(expr.offset.value, int):
                if expr.offset.value < 0:
                    self.report(
                        expr.offset,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        f"Array index must be non-negative, got {expr.offset.value}."
                    )
                elif expr.offset.value >= array_type.size:
                    self.report(
                        expr.offset,
                        ErrorCode.INVALID_ARGUMENT_COUNT,
                        f"Array index {expr.offset.value} is out of range for array '{expr.name}' of size {array_type.size}."
                    )

            return array_type.element_type

        if isinstance(expr, Literal):
            value = expr.value

            # `bool` must be checked before `int` because Python models bool as an int subclass.
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

            # Reaching this branch means the parser admitted an unsupported operator.
            self.report(expr, f"Unknown unary operator '{expr.operator}'.")
            return ERROR

        if isinstance(expr, Binary):
            left_type = self.check_expression(expr.left, env)
            right_type = self.check_expression(expr.right, env)
            op = expr.operator

            # Once either side has already failed, avoid layering follow-up type noise.
            if left_type == ERROR or right_type == ERROR:
                return ERROR

            # Arithmetic supports numeric operators plus string concatenation for `+`.
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

            # Relational comparisons are numeric-only and always yield booleans.
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

            # Equality is strict: both sides must have the exact same type.
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

            # Logical operators require boolean operands on both sides.
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