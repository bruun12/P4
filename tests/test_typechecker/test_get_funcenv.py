from type_checker.TypeChecker import FunctionEnvironment, TypeCheckError, STRING
import pytest

# Checks if the object is in the current environment
def test_get_current_scope():
    nu_miljø = FunctionEnvironment()
    nu_miljø.define("nuværende miljø", STRING)

    assert nu_miljø.get("nuværende miljø") == STRING

# Checks if it makes an error, if the object is not in the current environment
def test_raise_error():
    nu_miljø = FunctionEnvironment()
    nu_miljø.define("nuværende miljø", STRING)

    with pytest.raises(TypeCheckError):
        nu_miljø.get("dette objekt er udefineret")
