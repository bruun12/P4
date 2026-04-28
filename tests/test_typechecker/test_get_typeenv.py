from type_checker.TypeChecker import TypeEnvironment, TypeCheckError, STRING, INTEGER
import unittest

class test_get(unittest.TestCase):
    def test_get_current_scope(self):
        obj_type = TypeEnvironment()
        obj_type.define("hej med dig din seje reje", STRING)

        self.assertEqual(obj_type.get("hej med dig din seje reje"), STRING)

    def test_get_parent_scope(self):
        parent = TypeEnvironment()
        parent.define("holy shit du er sej", STRING)

        child = TypeEnvironment(parent)    

        self.assertEqual(child.get("holy shit du er sej"), STRING)

    def test_both_in_child_and_parent(self):
        parent = TypeEnvironment()
        parent.define("wow du er cool", STRING)

        child = TypeEnvironment(parent)
        child.define("wow du er cool", INTEGER)    

        self.assertEqual(child.get("wow du er cool"), INTEGER)
        self.assertNotEqual(child.get("wow du er cool"), STRING)

    def test_raise_error(self):
        parent = TypeEnvironment()
        parent.define("wow du er cool", STRING)

        child = TypeEnvironment(parent)
        child.define("wow du er cool", STRING)

        with self.assertRaises(TypeCheckError):
            child.get("does_not_exist")

