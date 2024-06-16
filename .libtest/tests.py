import unittest
from flk import Parser

class TestParser(unittest.TestCase):

    def setUp(self): 
        self.parser = Parser()
        self.variable_name = "my_sum"
        self.test_file = "test.fl"
        self.parser.current_file = self.test_file

    def test_edit_var_value(self):
        self.parser.parse_file(self.test_file)
        self.parser.edit_var_value(self.variable_name, 3)
        my_var = self.parser.get_var(self.variable_name)
        self.assertEqual(my_var.get_value(), 3)

    def test_get_var_type(self):
        self.parser.parse_file(self.test_file)
        my_var = self.parser.get_var(self.variable_name)
        var_type = my_var.get_type()
        self.assertIsInstance(var_type, str) 

    def test_get_var_value(self):
        self.parser.parse_file(self.test_file)
        self.parser.edit_var_value(self.variable_name, 3)
        my_var = self.parser.get_var(self.variable_name)
        var_value = my_var.get_value()
        self.assertEqual(var_value, 3)

    def test_create_var(self):
        self.parser.create_var("my_custom_var", "str", "Hello World!")
        my_custom_var = self.parser.get_var("my_custom_var")
        self.assertEqual(my_custom_var.get_value(), 'Hello World!')
        self.assertEqual(my_custom_var.get_type(), 'str')

    def test_remove_var(self):
        self.parser.create_var("my_custom_var", "str", "Hello World!")
        self.parser.remove_var("my_custom_var")
        with self.assertRaises(ValueError):
            self.parser.get_var("my_custom_var")

    def test_variable_info(self):
        self.parser.parse_file(self.test_file)
        self.parser.edit_var_value(self.variable_name, 3)
        my_var = self.parser.get_var(self.variable_name)
        var_type = my_var.get_type()
        var_value = my_var.get_value()
        print(f"Тип переменной '{self.variable_name}': {var_type}")
        print(f"Значение переменной '{self.variable_name}': {var_value}")
        self.assertEqual(var_type, 'float') 
        self.assertEqual(var_value, 3.0)

if __name__ == '__main__':
    unittest.main()
