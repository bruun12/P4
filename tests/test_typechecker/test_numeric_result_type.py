from type_checker.TypeChecker import numeric_result_type, INTEGER, FLOAT
import unittest

class test_numeric_result_type(unittest.TestCase):

    def test_result_of_same_types(self):
        self.assertEqual(numeric_result_type(FLOAT, FLOAT), FLOAT)
        self.assertEqual(numeric_result_type(INTEGER, INTEGER), INTEGER)

    def test_result_of_different_types(self):
        self.assertEqual(numeric_result_type(FLOAT, INTEGER), FLOAT)
        self.assertEqual(numeric_result_type(INTEGER, FLOAT), FLOAT)

