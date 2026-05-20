from enum import Enum, auto

# Global variable datatypes
class DataType(Enum):
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto(),

    VOID = auto()

# Global variables that assign values used in the source code to their respectively datatype
TYPES = {
    "integer": DataType.INTEGER,
    "double": DataType.FLOAT,
    "string": DataType.STRING,
    "boolean": DataType.BOOLEAN,
    "void" : DataType.VOID
}