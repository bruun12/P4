from type_checker.TypeChecker import TypeChecker
from error_handling import ErrorCode

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

# tjekker om errors bliver formatted rigtigt
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

    assert isinstance(formatted, list) # sikre at formatted er en liste
    assert len(formatted) == 1 # sikre at listen indeholder præcis 1 error
    assert len(formatted) != 2 # sikre at den ikke indeholder mere end 1 error

    # tjekker om den formattere attributterne i listen ordentligt
    assert "INVALID_DECLARED_TYPE" in result
    assert "Variable cannot have type void." in result
    assert "^" in result
