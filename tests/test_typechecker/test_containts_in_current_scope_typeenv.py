from type_checker.TypeChecker import TypeEnvironment, STRING
import unittest

class test_contains_in_current_scope_typeenv(unittest.TestCase):
    def test_contains(self):
        obj_type = TypeEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        result = obj_type.contains_in_current_scope("hej med dig din seje reje")

        self.assertTrue(result)

    def test_does_not_contain(self):
        obj_type = TypeEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        result = obj_type.contains_in_current_scope("hej")

        self.assertFalse(result)

    def test_contains_empty(self):
        obj_type = TypeEnvironment()

        result = obj_type.contains_in_current_scope("")

        self.assertFalse(result)
