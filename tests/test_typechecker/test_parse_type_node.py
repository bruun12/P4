'''
from type_checker.TypeChecker import parse_declared_type, declared_type, INTEGER
import unittest

class test_parse_type_node(unittest.TestCase):
    def test_existing_node(self):
        parse_declared_type(INTEGER)

        result = declared_type(INTEGER)
        self.assertTrue(result)

    #def test_not_existing_node(self):


'''