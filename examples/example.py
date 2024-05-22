from flk import Parser

parser = Parser()

parser.parse_file("example.fl")

variable_name = "my_dict"
my_var = parser.get_var(variable_name)

var_type = my_var.get_type()
var_value = my_var.get_value()

print(f"Тип переменной '{variable_name}': {var_type}")
print(f"Значение переменной '{variable_name}': {var_value}")