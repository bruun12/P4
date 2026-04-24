from type_checker.TypeChecker import FunctionEnvironment, STRING
import unittest

class test_contains_in_current_scope_typeenv(unittest.TestCase):
    def test_contains(self):
        obj_type = FunctionEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        self.assertTrue(obj_type.contains_in_current_scope("hej med dig din seje reje"))

    def test_does_not_contain(self):
        obj_type = FunctionEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        self.assertFalse(obj_type.contains_in_current_scope("hej"))

    def test_contains_empty(self):
        obj_type = FunctionEnvironment()

        self.assertFalse(obj_type.contains_in_current_scope(""))
