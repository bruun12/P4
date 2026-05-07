from dataclasses import dataclass
from error_handling import TypeCheckError, ErrorCode

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
        ArrayType(INTEGER, 1)
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

#missing comment
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
