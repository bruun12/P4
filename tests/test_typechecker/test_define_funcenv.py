from type_checker.TypeChecker import STRING, INTEGER, FunctionEnvironment
from type_checker.ClassesAndHelpers import FunctionType
# Checks if the value is added to the dictionary with the correct type
def test_define_function():
    env = FunctionEnvironment()
    func_type = FunctionType(
        parameter_types=[INTEGER, INTEGER],
        return_type=INTEGER
    )
    env.define("func", func_type)
    assert env.get("func") == func_type
    assert env.contains_in_current_scope("func") == True
    
# Python will accept any type of value in the dict at runtime, not just FunctionType,
#therefore no sad path test has been added