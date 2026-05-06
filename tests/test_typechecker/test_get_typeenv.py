from type_checker.TypeChecker import TypeEnvironment, TypeCheckError, STRING, INTEGER
import pytest

# tjekker om et objekt er i det nuværende miljø
def test_get_current_scope():
    nu_miljø = TypeEnvironment()
    nu_miljø.define("nuværende miljø", STRING)

    assert nu_miljø.get("nuværende miljø") == STRING

# tjekker om et objekt er i parent scope
def test_get_parent_scope():
    parent = TypeEnvironment()
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent)    

    assert child.get("globalt objekt") == STRING

# tjekker om et objekt defineret i parent også ligger i child (globalt miljø)
def test_defined_in_parent():
    parent = TypeEnvironment()
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent) 

    assert child.get("globalt objekt") == STRING

# tjekker om den laver en error, hvis et objekt ikke ligger i det nuværende miljø
def test_raise_error():
    parent = TypeEnvironment()
    parent.define("globalt objekt", STRING)

    child = TypeEnvironment(parent)
    child.define("lokalt objekt", STRING)

    with pytest.raises(TypeCheckError):
        child.get("dette objekt er udefineret i child")

    with pytest.raises (TypeCheckError):
        parent.get(child) # parent node burde ikke have adgang til child node
