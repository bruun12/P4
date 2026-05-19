from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# tjekker om der er mere end 0 errors i error listen
def test_has_errors():
    checker = TypeChecker(source_code="")

    node = MockASTNode(1, 1)

    checker.report(
        node, 
        ErrorCode.INVALID_DECLARED_TYPE, 
        "Variable cannot have type void."
    )

    assert checker.has_errors() is True

# tjekker at der ingen errors er
def test_has_no_errors():
    checker = TypeChecker(source_code="")

    assert checker.has_errors() is False
