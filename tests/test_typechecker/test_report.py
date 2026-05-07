from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode, TypeCheckError

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# tjekker om den smider det korrekt ind i error listen
def test_report_adds_error():
    checker = TypeChecker(source_code="")

    node = MockASTNode(1, 1)

    checker.report(
        node, 
        ErrorCode.INVALID_DECLARED_TYPE, 
        "Variable cannot have type void."
    )

    # tjekker at error listen indeholder præcis 1 error
    assert len(checker.errors) == 1 
    assert len(checker.errors) != 2

    err = checker.errors[0] 

    # for at sikre det er det rigtige objekt der bliver brugt
    assert isinstance(err, TypeCheckError)

    # tjekker at informationerne er blevet sat korrekt ind i listen
    assert err.line == 1
    assert err.column == 1
    assert err.error_code == ErrorCode.INVALID_DECLARED_TYPE
    assert err.message == "Variable cannot have type void."
