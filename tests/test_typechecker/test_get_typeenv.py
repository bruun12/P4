from type_checker.TypeChecker import TypeEnvironment, TypeCheckError, STRING, INTEGER
import pytest

def test_get_current_scope():
    obj_type = TypeEnvironment()
    obj_type.define("hej med dig din seje reje", STRING)

    assert obj_type.get("hej med dig din seje reje") == STRING

def test_get_parent_scope():
    parent = TypeEnvironment()
    parent.define("holy shit du er sej", STRING)

    child = TypeEnvironment(parent)    

    assert child.get("holy shit du er sej") == STRING

def test_both_in_child_and_parent():
    parent = TypeEnvironment()
    parent.define("wow du er cool", STRING)

    child = TypeEnvironment(parent)
    child.define("wow du er cool", INTEGER)    

    assert child.get("wow du er cool") == INTEGER
    assert child.get("wow du er cool") != STRING

def test_raise_error():
    parent = TypeEnvironment()
    parent.define("wow du er cool", STRING)

    child = TypeEnvironment(parent)
    child.define("wow du er cool", STRING)

    with pytest.raises(TypeCheckError):
        child.get("does_not_exist")

