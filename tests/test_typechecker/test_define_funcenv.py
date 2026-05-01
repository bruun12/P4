from type_checker.TypeChecker import STRING, INTEGER, FunctionEnvironment

def test_define_add_value():
    obj_type = FunctionEnvironment()
    obj_type.define(1, INTEGER)
    obj_type.define("hej din seje reje", STRING)

    assert obj_type.values[1] == INTEGER
    assert obj_type.values["hej din seje reje"] == STRING
    