from type_checker.TypeChecker import FunctionEnvironment, STRING

# Checks if the environment contains the defined object,
# and not an undefined object
def test_contains_and_not_contains():
    in_environment = FunctionEnvironment()
    in_environment.define("Is in the envirionment", STRING)

    assert in_environment.contains_in_current_scope("Is in the envirionment")
    assert not in_environment.contains_in_current_scope("Is not in the envirionment")

# Checks the environment MUST contain somehting (cannot contain nothing)
def test_contains_empty():
    in_environment = FunctionEnvironment()

    assert not in_environment.contains_in_current_scope("")