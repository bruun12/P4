from type_checker.TypeChecker import STRING, INTEGER, FunctionEnvironment

# Checks if the value is added to the dictionary with the correct type
def test_define_add_value():
    env = FunctionEnvironment()
    env.define(1, INTEGER)
    env.define("tilføj_denne_streng_som_funktionsnavn", STRING)

    assert env.values[1] == INTEGER
    assert env.values["tilføj_denne_streng_som_funktionsnavn"] == STRING
    