from type_checker.TypeChecker import FunctionEnvironment, TypeCheckError, STRING
import pytest

# Checks if the object is in the current environment
def test_get_current_scope():
    nu_env = FunctionEnvironment()
    nu_env.define("Current environment", STRING)

    assert nu_env.get("Current environment") == STRING

# Checks if it makes an error, if the object is not in the current environment
def test_raise_error():
    nu_env = FunctionEnvironment()
    nu_env.define("Current environment", STRING)

    with pytest.raises(TypeCheckError):
        nu_env.get("this object is udefineret")
