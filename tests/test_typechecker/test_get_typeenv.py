from type_checker.TypeChecker import TypeEnvironment, TypeCheckError, STRING, INTEGER
import pytest

# Checks if the object is in the current environment
def test_get_current_scope():
    nu_miljø = TypeEnvironment(None)
    nu_miljø.define("nuværende miljø", STRING)

    assert nu_miljø.get("nuværende miljø") == STRING

# Checks if the object is in the parent scope
def test_get_parent_scope():
    parent = TypeEnvironment(None)
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent)    

    assert child.get("globalt objekt") == STRING

# Checks if the object defined in the parent also lies within the child (global scope)
def test_defined_in_parent():
    parent = TypeEnvironment(None)
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent) 

    assert child.get("globalt objekt") == STRING

# Checks if it makes an error, if the object is not in the current environment
def test_raise_error():
    parent = TypeEnvironment(None)
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent)
    child.define("lokalt objekt", STRING)

    with pytest.raises(TypeCheckError):
        child.get("dette objekt er udefineret i child")

    with pytest.raises (TypeCheckError):
        parent.get(child) # parent node should not have access to the child node