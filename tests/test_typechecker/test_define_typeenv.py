from type_checker.TypeChecker import STRING, INTEGER, TypeEnvironment

# tjekker om der bliver added values til dictionary og de har den rigtige type
def test_define_add_value():
    env = TypeEnvironment()
    env.define(1, INTEGER)
    env.define("tilføj_denne_streng_som_type", STRING)

    assert env.values[1] == INTEGER
    assert env.values["tilføj_denne_streng_som_type"] == STRING
  