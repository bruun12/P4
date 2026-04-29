from type_checker.TypeChecker import type_name, ArrayType, FunctionType, Type, INTEGER, FLOAT, BOOLEAN, VOID, STRING, ERROR
import unittest

class DummyTest(Type):
    pass

class test_type_name(unittest.TestCase):
    def test_correct_types(self):
        self.assertEqual(type_name(INTEGER), "integer")
        self.assertEqual(type_name(FLOAT), "float")
        self.assertEqual(type_name(BOOLEAN), "boolean")
        self.assertEqual(type_name(STRING), "string")
        self.assertEqual(type_name(VOID), "void")
        self.assertEqual(type_name(ERROR), "<error>")
    
    def test_array_type(self):
        arrayObj_int = ArrayType(INTEGER)
        arrayObj_str = ArrayType(STRING)
        arrayObj_bool = ArrayType(BOOLEAN)
        arrayObj_void = ArrayType(VOID)

        self.assertEqual(type_name(arrayObj_int), "integer[]")
        self.assertNotEqual(type_name(arrayObj_int), "integer")
        self.assertEqual(type_name(arrayObj_str), "string[]")
        self.assertNotEqual(type_name(arrayObj_str), "string")
        self.assertEqual(type_name(arrayObj_bool), "boolean[]")
        self.assertNotEqual(type_name(arrayObj_bool), "boolean")
        self.assertEqual(type_name(arrayObj_void), "void[]")
        self.assertNotEqual(type_name(arrayObj_void), "void")
        
    def test_nested_array_type(self):
        arrayObj_nested_int = ArrayType(ArrayType(INTEGER))
        arrayObj_nested_str = ArrayType(ArrayType(STRING))
        arrayObj_nested_bool = ArrayType(ArrayType(BOOLEAN))
        arrayObj_nested_void = ArrayType(ArrayType(VOID))

        self.assertEqual(type_name(arrayObj_nested_int), "integer[][]")
        self.assertNotEqual(type_name(arrayObj_nested_int), "integer[]")
        self.assertEqual(type_name(arrayObj_nested_str), "string[][]")
        self.assertNotEqual(type_name(arrayObj_nested_str), "string[]")
        self.assertEqual(type_name(arrayObj_nested_bool), "boolean[][]")
        self.assertNotEqual(type_name(arrayObj_nested_bool), "boolean[]")
        self.assertEqual(type_name(arrayObj_nested_void), "void[][]")
        self.assertNotEqual(type_name(arrayObj_nested_void), "void[]")

    def test_function_type(self):
        funcObj = FunctionType(
            parameter_types=(INTEGER,),
            return_type=STRING
        )
        
        self.assertEqual(type_name(funcObj), "function(integer) -> string")
        self.assertNotEqual(type_name(funcObj), "function(integer, integer) -> string")

    def test_function_tuple_type(self):
        funcObj = FunctionType(
            parameter_types=(INTEGER, FLOAT),
            return_type=BOOLEAN
        )
        
        self.assertEqual(type_name(funcObj), "function(integer, float) -> boolean")
        self.assertNotEqual(type_name(funcObj), "function(float, integer) -> string")

    def test_array_function_type(self):
        funcObj = FunctionType(
            parameter_types=(ArrayType(INTEGER),),
            return_type=STRING
        )
        funcObj_str_bool = FunctionType(
            parameter_types=(ArrayType(STRING),),
            return_type=BOOLEAN
        )
        funcObj_nested = FunctionType(
            parameter_types=(ArrayType(ArrayType(STRING),),),
            return_type=BOOLEAN
        )

        self.assertEqual(type_name(funcObj), "function(integer[]) -> string")
        self.assertEqual(type_name(funcObj_str_bool), "function(string[]) -> boolean")
        self.assertEqual(type_name(funcObj_nested), "function(string[][]) -> boolean")

    def test_repr_type(self):
        tObj = DummyTest()

        self.assertEqual(type_name(tObj), repr(tObj))
