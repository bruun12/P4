from type_checker.TypeChecker import TypeEnvironment, STRING

# Checks the environment contains the defined object, 
# and not an undefined object
def test_contains_and_not_contains():
    i_miljø = TypeEnvironment(None)
    i_miljø.define("ligger i miljøet", STRING)

    assert i_miljø.contains_in_current_scope("ligger i miljøet")
    assert not i_miljø.contains_in_current_scope("ligger ikke i miljøet")

# Checks the environment MUST contain somehting (cannot contain nothing)
def test_contains_empty():
    i_miljø = TypeEnvironment(None)

    assert not i_miljø.contains_in_current_scope("")
