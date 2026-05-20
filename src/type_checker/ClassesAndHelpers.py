from dataclasses import dataclass
from error_handling import TypeCheckError, ErrorCode

class Type:
    pass

#frozen = True makes the class unchangable 
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

# Dataclass of an array that contains elements
# example: ArrayType(INTEGER, 1)
@dataclass(frozen=True)
class ArrayType(Type):
    element_type: Type
    size: int

# Dataclass of a function that contains parameter- and return-types
@dataclass(frozen=True)
class FunctionType(Type):
    parameter_types: tuple[Type, ...] 
    return_type: Type


# Global variables to make it easier to call the dataclasses
INTEGER = IntegerType()
DOUBLE = DoubleType()
BOOLEAN = BooleanType()
STRING = StringType()
VOID = VoidType()
ERROR = ErrorType()

# Function to return matching string of type object.
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
    
    # Checks if the datatype is an ArrayType, 
    # and returns its elementtype
    if isinstance(t, ArrayType):
        return f"{type_name(t.element_type)}[]"
    
    if isinstance(t, FunctionType):
        # Convert each type object into its string name (e.g., [integer, float])
        name_list = []
        for p in t.parameter_types:
            name_list.append(type_name(p))

        # Join them with commas (e.g., "integer, float")
        params_string = ", ".join(name_list)

        # Build the final function signature
        return f"function({params_string}) -> {type_name(t.return_type)}"
    
    return repr(t)

# Function to return true if datatype is an integer or double
def is_numeric(t: Type) -> bool:
    return t == INTEGER or t == DOUBLE

# Function to return true if the datatype target and assigned value can be assigned to each other 
def can_assign(target: Type, value: Type) -> bool:
    if target == value: # If both target and value have same datatype
        return True

    # Implicit type conversion; 
    # allows value to be of the datatype integer, 
    # even though target datatype is a double
    if target == DOUBLE and value == INTEGER: 
        return True

    # Makes sure elements in an array have the same datatype (or is part of the implicit conversion)
    if isinstance(target, ArrayType) and isinstance(value, ArrayType):
        return can_assign(target.element_type, value.element_type)

    return False

# Function to return either a double or an integer depending on the result (er usikker på om det er resultatet der tjekkes)
def numeric_result_type(left: Type, right: Type) -> Type:
    if left == DOUBLE or right == DOUBLE:
        return DOUBLE
    return INTEGER

# ???
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
