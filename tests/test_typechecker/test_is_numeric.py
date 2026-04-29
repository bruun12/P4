from type_checker.TypeChecker import is_numeric, INTEGER, FLOAT, STRING, BOOLEAN, VOID
import unittest

class test_is_numeric(unittest.TestCase):

    def test_valid_numbers(self):
        self.assertTrue(is_numeric(INTEGER))
        self.assertTrue(is_numeric(FLOAT))

    def test_invalid_values(self):
        self.assertFalse(is_numeric(STRING))

    def test_boolean(self):
        self.assertFalse(is_numeric(BOOLEAN))

    def test_empty(self):
        self.assertFalse(is_numeric(VOID))
