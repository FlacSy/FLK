from flk import Parser

filename = 'example.fl'
parser = Parser()
data = parser.parse_file(filename)

# Вывод результатов
for key, value in data.items():
    print(f"{key}: {value}")