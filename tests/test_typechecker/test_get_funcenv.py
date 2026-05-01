from type_checker.TypeChecker import FunctionEnvironment, TypeCheckError, STRING, INTEGER
import pytest

def test_get_current_scope():
    obj_type = FunctionEnvironment()
    obj_type.define("hej med dig din seje reje", STRING)

    assert obj_type.get("hej med dig din seje reje") == STRING

def test_raise_error():
    obj_type = FunctionEnvironment()
    obj_type.define("wow du er cool", STRING)

    with pytest.raises(TypeCheckError):
        obj_type.get("does_not_exist")
