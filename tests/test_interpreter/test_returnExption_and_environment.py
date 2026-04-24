import pytest
from interpreter.interpreter import Environment, ReturnException

# ReturnException tests

def test_return_exception_saves_value():
    ex = ReturnException(42)
    assert ex.value == 42

def test_return_exception_with_none():
    ex = ReturnException(None)
    assert ex.value is None

def test_return_exception_raise():
    with pytest.raises(ReturnException) as info:
        raise ReturnException(99)
    assert info.value.value == 99

def test_return_exception_is_exception():
    ex = ReturnException(1)
    assert isinstance(ex, Exception)

# Environment tests
# set and get

def test_set_and_get():
    env = Environment()
    env.set("x", 5)
    assert env.get("x") == 5

def test_get_unknown_variable_raises_error():
    env = Environment()
    with pytest.raises(RuntimeError):
        env.get("x")

def test_set_overwrite_existing():
    env = Environment()
    env.set("x", 5)
    env.set("x", 10)
    assert env.get("x") == 10

# parent scope

def test_get_finds_variable_in_parent():
    global_env = Environment()
    global_env.set("x", 5)
    local_env = Environment(parent=global_env)
    assert local_env.get("x") == 5

def test_get_takes_local_scope():
    global_env = Environment()
    global_env.set("x", 5)
    local_env = Environment(parent=global_env)
    local_env.set("x", 99)
    assert local_env.get("x") == 99  # lokal x, ikke global

def test_get_though_more_layers():
    env1 = Environment()
    env1.set("x", 1)
    env2 = Environment(parent=env1)
    env3 = Environment(parent=env2)
    assert env3.get("x") == 1  # finder x tre lag oppe

# assign

def test_assign_opdates_in_same_scope():
    env = Environment()
    env.set("x", 5)
    env.assign("x", 10)
    assert env.get("x") == 10

def test_assign_opdates_in_parent():
    global_env = Environment()
    global_env.set("x", 5)
    local_env = Environment(parent=global_env)
    local_env.assign("x", 99)
    assert global_env.get("x") == 99  # global x er opdateret

def test_assign_unknown_variable_error():
    env = Environment()
    with pytest.raises(RuntimeError):
        env.assign("x", 10)

def test_assign_do_not_make_new_variable_in_child():
    global_env = Environment()
    global_env.set("x", 5)
    local_env = Environment(parent=global_env)
    local_env.assign("x", 99)
    assert "x" not in local_env.vars  # x er ikke i local_env
    assert global_env.get("x") == 99  # men opdateret i global