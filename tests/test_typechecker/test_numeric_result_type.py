from type_checker.TypeChecker import numeric_result_type, INTEGER, FLOAT, STRING, BOOLEAN
import unittest

class test_numeric_result_type(unittest.TestCase):

    def test_result_of_same_types(self):
        self.assertEqual(numeric_result_type(FLOAT, FLOAT), FLOAT)
        self.assertEqual(numeric_result_type(INTEGER, INTEGER), INTEGER)

    def test_result_of_different_types(self):
        self.assertEqual(numeric_result_type(FLOAT, INTEGER), FLOAT)
        self.assertEqual(numeric_result_type(INTEGER, FLOAT), FLOAT)

# måske det skal laves om - kommer an på, om den bliver begrænset andre steder
# så den ikke godtager de her tests andre steder
    def test_incorrect_results(self):
        self.assertTrue(numeric_result_type(STRING, INTEGER), STRING)
        self.assertTrue(numeric_result_type(INTEGER, STRING), INTEGER)
        self.assertTrue(numeric_result_type(BOOLEAN, INTEGER), BOOLEAN)
        self.assertTrue(numeric_result_type(True, 1), INTEGER)
