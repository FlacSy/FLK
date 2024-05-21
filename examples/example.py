from flk import Parser

# Создание экземпляра парсера
parser = Parser()

# Парсинг строки в словарь
parsed_dict = parser.parse_dict('{key_name_1(key): value_string(str) = "Value String",key_name_2(key): value_integer(int) = 239832 }')
print(parsed_dict)  # Вывод: {'key_name_1': 'Value String', 'key_name_2': 239832}

# Парсинг строки с константой
parser.parse_constant_line('const PI(float) = 3.14')
print(parser.constants)  # Вывод: {'PI': 3.14}

# Парсинг строки с объявлением переменной
parser.parse_line('var1(int) = 10')
print(parser.data)  # Вывод: {'var1': <Variable object with type 'int' and value 10>}

# Парсинг файла
data = parser.parse_file('example.fl')
print(data)  # Вывод: {'var1': 10, ...} (данные из файла)