from type_checker.TypeChecker import STRING, INTEGER, TypeEnvironment
import unittest

class test_define_typeenv(unittest.TestCase):
    def test_define_add_value(self):
        obj_type = TypeEnvironment()
        obj_type.define(1, INTEGER)
        obj_type.define("hej din seje reje", STRING)

        self.assertEqual(obj_type.values[1], INTEGER)
        self.assertEqual(obj_type.values["hej din seje reje"], STRING)
        