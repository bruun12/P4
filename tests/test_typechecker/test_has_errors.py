from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# Checks if there is more than 0 errors in the list
def test_has_errors():
    checker = TypeChecker(source_code="")

    node = MockASTNode(1, 1)

    checker.report(
        node, 
        ErrorCode.INVALID_DECLARED_TYPE, 
        "Variable cannot have type void."
    )

    assert checker.has_errors() is True

# Check that there are no errors
def test_has_no_errors():
    checker = TypeChecker(source_code="")

    assert checker.has_errors() is False
