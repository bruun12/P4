from type_checker.TypeChecker import FunctionEnvironment, STRING

# tjekker om miljøet indeholder det defineret objekt, 
# og ikke indeholder et udefineret objekt
def test_contains_and_not_contains():
    i_miljø = FunctionEnvironment()
    i_miljø.define("ligger i miljøet", STRING)

    assert i_miljø.contains_in_current_scope("ligger i miljøet")
    assert not i_miljø.contains_in_current_scope("ligger ikke i miljøet")

# tjekker at miljøet SKAL indeholde et eller andet (må ikke indeholde ingenting)
def test_contains_empty():
    i_miljø = FunctionEnvironment()

    assert not i_miljø.contains_in_current_scope("")
