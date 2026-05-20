from type_checker.TypeChecker import STRING, INTEGER, TypeEnvironment

# Checks if the value is added to the dictionary with the correct type
def test_define_add_value():
    env = TypeEnvironment(None)
    env.define(1, INTEGER)
    env.define("tilføj_denne_streng_som_type", STRING)

    assert env.values[1] == INTEGER
    assert env.values["tilføj_denne_streng_som_type"] == STRING
  