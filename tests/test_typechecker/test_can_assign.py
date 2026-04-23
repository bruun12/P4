from type_checker.TypeChecker import can_assign, INTEGER, FLOAT, STRING, BOOLEAN, ArrayType
import unittest

class test_can_assign(unittest.TestCase):

    def test_same_type(self):
        self.assertTrue(can_assign(INTEGER, INTEGER))
        self.assertTrue(can_assign(FLOAT, FLOAT))
        self.assertTrue(can_assign(BOOLEAN, BOOLEAN))
        self.assertTrue(can_assign(STRING, STRING))

    def test_int_to_float(self):
        self.assertTrue(can_assign(FLOAT, INTEGER))
        self.assertFalse(can_assign(FLOAT, STRING))
        self.assertFalse(can_assign(FLOAT, BOOLEAN))
    
    def test_float_to_int(self):
        self.assertFalse(can_assign(INTEGER, FLOAT))

    def test_same_array_type(self):
        self.assertTrue(can_assign(ArrayType(INTEGER), ArrayType(INTEGER)))
        self.assertTrue(can_assign(ArrayType(FLOAT), ArrayType(FLOAT)))
        self.assertTrue(can_assign(ArrayType(STRING), ArrayType(STRING)))

    def test_different_array_type(self):
        self.assertFalse(can_assign(ArrayType(INTEGER), ArrayType(FLOAT)))
        self.assertFalse(can_assign(ArrayType(FLOAT), ArrayType(STRING)))
        self.assertFalse(can_assign(ArrayType(STRING), ArrayType(INTEGER)))
