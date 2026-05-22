from type_checker.TypeChecker import STRING, INTEGER, ERROR, TypeEnvironment
from error_handling import TypeCheckError, ErrorCode
# Checks if the value is added to the dictionary with the correct type
import pytest
def test_define_add_value():
    outer_env = TypeEnvironment(None)
    inner_env = TypeEnvironment(outer_env)
    
    outer_env.define("x", INTEGER)
    inner_env.define("x", STRING)
    
    assert inner_env.get("x") == STRING
    assert outer_env.get("x") == INTEGER
    
def test_out_of_scope():
    outer_env = TypeEnvironment(None)
    inner_env = TypeEnvironment(outer_env)
    
    inner_env.define("y", INTEGER)
    
    with pytest.raises(TypeCheckError) as err:
        outer_env.get("y")
    assert err.value.error_code == ErrorCode.UNDEFINED_VARIABLE_ERROR


  