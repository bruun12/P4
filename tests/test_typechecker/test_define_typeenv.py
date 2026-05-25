from type_checker.TypeChecker import STRING, INTEGER, TypeEnvironment

# Checks if the value is added to the dictionary with the correct type
def test_define_add_value():
    env = TypeEnvironment(None)
    env.define(1, INTEGER)
    env.define("add_this_string_as_function_name", STRING)

    assert env.values[1] == INTEGER
    assert env.values["add_this_string_as_function_name"] == STRING
  