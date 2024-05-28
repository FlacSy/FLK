# Импортируем класс Parser из модуля flk
from flk import Parser

# Создаем экземпляр парсера
parser = Parser()

# Задаем имя переменной, значение которой мы хотим изменить
variable_name = "my_sum"

# Парсим файл "example.fl" и анализируем его содержимое
parser.parse_file("example.fl")

# Изменяем значение переменной с именем, указанным в variable_name, на 3
# parser.edit_var_value(variable_name, 3)

# Получаем объект переменной с именем, указанным в variable_name
my_var = parser.get_var(variable_name)

# Получаем тип переменной
var_type = my_var.get_type()

# Получаем значение переменной
var_value = my_var.get_value()

# Создаем переменную 
parser.create_var("my_custom_var", "str", "Hello World!")

# Удаляем переменную
parser.remove_var("my_custom_var")

# Выводим информацию о переменной
print(f"Тип переменной '{variable_name}': {var_type}")
print(f"Значение переменной '{variable_name}': {var_value}")