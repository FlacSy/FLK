# FLK (File Language Kit)

FLK - это библиотека для парсинга и работы с файлами в формате FL (File Language). FLK позволяет читать и анализировать файлы, написанные на языке FL, который предоставляет простой формат для хранения структурированных данных.

## Установка

Установите FLK с помощью pip из PyPi:

```bash
pip install flk
```

Или установите последнюю версию с GitHub:

```bash
pip install git+https://github.com/FlacSy/flk
```

## Использование

Для начала работы с FLK, импортируйте класс `Parser` из библиотеки:

```python
from flk import Parser
```

Затем создайте экземпляр класса `Parser` и используйте его для парсинга файла FL:

```python
filename = 'example.fl'
parser = Parser()
data = parser.parse_file(filename)

# Вывод результатов
for key, value in data.items():
    print(f"{key}: {value}")
```

## Формат файла FL

Файл FL содержит переменные и их значения в определенном формате. Вот пример простого файла FL:

```
# Константы
const PI(float) = 3.14159

# Переменные
my_string(str) = Hello, world! // Коментарии для строк
my_int(int) = 42
my_float(float) = 3.14
my_bool(bool) = True
my_list(list) = [1, 2, 3]
my_dict(dict) = {
    key_name_1(key): vaule_string(str) = Vaule String,
    key_name_2(key): vaule_integer(int) = 239832
}
```

Комментарии начинаются с символа `#`. Для строк, где переменная используется, можно использовать комментарий `//`. Определение констант начинается с ключевого слова `const`, а определение переменных - с их имени, типа и значения.

## Расширение Visual Studio Code для отображения синтаксиса файлов .fl 

[GitHub](https://github.com/FlacSy/FLSyntax)

[VisualStudio Marketplace](https://marketplace.visualstudio.com/items?itemName=FLSyntax.fl-syntax-highlighter&ssr=false#review-details)

## Методы

### `parse_file(filename: str) -> Dict[str, Any]`

Парсит файл FL и возвращает словарь данных, содержащий переменные и их значения.

- `filename`: Путь к файлу FL.
- Возвращает: Словарь данных, где ключи - имена переменных, а значения - их значения.

## Лицензия

FLK распространяется под лицензией Apache License Version 2.0. Подробную информацию о лицензии можно найти в файле [LICENSE](LICENSE).