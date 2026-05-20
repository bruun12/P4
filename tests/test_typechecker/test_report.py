from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode, TypeCheckError

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# Checks if it throws an error correctly into the error list
def test_report_adds_error():
    checker = TypeChecker(source_code="")

    node = MockASTNode(1, 1)

    checker.report(
        node, 
        ErrorCode.INVALID_DECLARED_TYPE, 
        "Variable cannot have type void."
    )

    # Checks if the error list contains exactly 1 error
    assert len(checker.errors) == 1 
    assert len(checker.errors) != 2

    err = checker.errors[0] 

    # to ensure it is the correct object that is used
    assert isinstance(err, TypeCheckError)

    # checks the information is placed correctly inside the list
    assert err.line == 1
    assert err.column == 1
    assert err.error_code == ErrorCode.INVALID_DECLARED_TYPE
    assert err.message == "Variable cannot have type void."
