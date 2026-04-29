from type_checker.TypeChecker import parse_declared_type, TypeCheckError, INTEGER, FLOAT, BOOLEAN, STRING, VOID
import unittest

class test_parse_declared_type(unittest.TestCase):
    
    def test_correct_type(self):
        self.assertEqual(parse_declared_type("integer"), INTEGER)
        self.assertEqual(parse_declared_type("float"), FLOAT)
        self.assertEqual(parse_declared_type("boolean"), BOOLEAN)
        self.assertEqual(parse_declared_type("string"), STRING)
        self.assertEqual(parse_declared_type("void"), VOID)

    def test_type_error_int(self):
        with self.assertRaises(TypeCheckError):
            parse_declared_type("int")
    
    def test_type_error_double(self):
        with self.assertRaises(TypeCheckError):
            parse_declared_type("double")

    def test_type_error_case_sensitive(self):
        with self.assertRaises(TypeCheckError):
            parse_declared_type("INTEGER")

    def test_type_error_extra_space(self):
        with self.assertRaises(TypeCheckError):
            parse_declared_type("void ")