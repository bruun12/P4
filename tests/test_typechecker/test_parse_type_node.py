from type_checker.TypeChecker import TypeChecker
from type_checker.ClassesAndHelpers import INTEGER, ERROR

class MockASTNode:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

def test_parse_valid_type():
        checker = TypeChecker(source_code="")

        node = MockASTNode(1, 1)

        result = checker.parse_type_node("integer", node)


        assert result == INTEGER
        assert result != ERROR

        assert len(checker.errors) == 0
        

def test_parse_invalid_type():
        checker = TypeChecker(source_code="")

        node = MockASTNode(1, 1)

        result = checker.parse_type_node("int", node)

        assert result != INTEGER
        assert result == ERROR

        assert len(checker.errors) == 1
