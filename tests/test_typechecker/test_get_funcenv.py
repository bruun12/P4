from type_checker.TypeChecker import FunctionEnvironment, TypeCheckError, STRING, INTEGER
import pytest

# tjekker om et objekt er i det nuværende miljø
def test_get_current_scope():
    nu_miljø = FunctionEnvironment()
    nu_miljø.define("nuværende miljø", STRING)

    assert nu_miljø.get("nuværende miljø") == STRING

# tjekker om den laver en error, hvis et objekt ikke ligger i det nuværende miljø
def test_raise_error():
    nu_miljø = FunctionEnvironment()
    nu_miljø.define("nuværende miljø", STRING)

    with pytest.raises(TypeCheckError):
        nu_miljø.get("dette objekt er udefineret")
