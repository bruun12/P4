from type_checker.TypeChecker import FunctionEnvironment, TypeCheckError, STRING, INTEGER
import unittest

class test_get(unittest.TestCase):
    def test_get_current_scope(self):
        obj_type = FunctionEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        self.assertEqual(obj_type.get("hej med dig din seje reje"), STRING)

    def test_raise_error(self):
        obj_type = FunctionEnvironment()
        obj_type.define("wow du er cool", STRING)

        with self.assertRaises(TypeCheckError):
            obj_type.get("does_not_exist")
