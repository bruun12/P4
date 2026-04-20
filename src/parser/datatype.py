from enum import Enum, auto

class DataType(Enum):
    # types
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOLEAN = auto(),

    VOID = auto()

TYPES = {
    "integer": DataType.INTEGER,
    "double": DataType.FLOAT,
    "string": DataType.STRING,
    "boolean": DataType.BOOLEAN,
    "void" : DataType.VOID
}