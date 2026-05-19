from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# Checks if errors are formatted correctly
def test_formatted_errors():
    checker = TypeChecker(source_code="void x = 5")

    node = MockASTNode(1, 1)

    checker.report(
        node, 
        ErrorCode.INVALID_DECLARED_TYPE, 
        "Variable cannot have type void."
    )

    formatted = checker.formatted_errors()
    result = formatted[0]

    assert isinstance(formatted, list) # ensures the format is a list
    assert len(formatted) == 1 # ensures the list contains exactly 1 error
    assert len(formatted) != 2 # ensure the list does not contain more than 1 error

    # Checks if it correctly formats the properties in the list 
    assert "INVALID_DECLARED_TYPE" in result
    assert "Variable cannot have type void." in result
    assert "^" in result
