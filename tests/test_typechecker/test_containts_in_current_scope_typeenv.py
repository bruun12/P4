from type_checker.TypeChecker import TypeEnvironment, STRING

# Checks the environment contains the defined object, 
# and not an undefined object
def test_contains_and_not_contains():
    inEnvironment = TypeEnvironment(None)
    inEnvironment.define("ligger i miljøet", STRING)

    assert inEnvironment.contains_in_current_scope("ligger i miljøet")
    assert not inEnvironment.contains_in_current_scope("ligger ikke i miljøet")

# Checks the environment MUST contain somehting (cannot contain nothing)
def test_contains_empty():
    inEnvironment = TypeEnvironment(None)

    assert not inEnvironment.contains_in_current_scope("")
