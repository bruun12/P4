from type_checker.TypeChecker import FunctionEnvironment, STRING

def test_contains():
    obj_type = FunctionEnvironment()
    obj_type.define("hej med dig din seje reje", STRING)

    assert obj_type.contains_in_current_scope("hej med dig din seje reje")

def test_does_not_contain():
    obj_type = FunctionEnvironment()
    obj_type.define("hej med dig din seje reje", STRING)

    assert not obj_type.contains_in_current_scope("hej")

def test_contains_empty():
    obj_type = FunctionEnvironment()

    assert not obj_type.contains_in_current_scope("")
