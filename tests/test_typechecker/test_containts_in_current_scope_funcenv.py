from type_checker.TypeChecker import FunctionEnvironment, STRING

# Checks if the environment contains the defined object,
# and not an undefined object
def test_contains_and_not_contains():
    in_environment = FunctionEnvironment()
    in_environment.define("ligger i miljøet", STRING)

    assert in_environment.contains_in_current_scope("ligger i miljøet")
    assert not in_environment.contains_in_current_scope("ligger ikke i miljøet")

# Checks the environment MUST contain somehting (cannot contain nothing)
def test_contains_empty():
    in_environment = FunctionEnvironment()

    assert not in_environment.contains_in_current_scope("")
