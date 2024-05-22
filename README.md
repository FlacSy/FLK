# FLK (File Language Kit)

FLK - это библиотека для парсинга и работы с файлами в формате FL (File Language), предназначенная для упрощения работы со структурированными данными.

## Основные возможности

- **Парсинг файлов FL**: Чтение и анализ файлов с расширением `.fl`, содержащих переменные и константы.
- **Простота использования**: Импортируйте `Parser` и начните парсинг файлов с минимальной настройкой.
- **Расширяемость**: Легко адаптируйте для парсинга различных форматов данных.

## Установка

Установите через pip:

```bash
pip install flk
```

Для последней версии:

```bash
pip install git+https://github.com/FlacSy/flk
```

## Быстрый старт

### Импорт и использование парсера

```python
from flk import Parser

parser = Parser()

parser.parse_file("example.fl")

variable_name = "my_int"
my_var = parser.get_var(variable_name)

var_type = my_var.get_type()
var_value = my_var.get_value()

print(f"Тип переменной '{variable_name}': {var_type}")
print(f"Значение переменной '{variable_name}': {var_value}")
```

### Командная строка

Используйте FLK из командной строки:

```bash
python -m flk example.fl
```

## Синтаксис файла FL

Файлы FL используют простой и понятный синтаксис для определения переменных и констант:

### Комментарии
- Однострочные: начинаются с `#`
- Многострочные: ограничены `/*` и `*/`

### Константы
- Определяются с ключевым словом `const`, за которым следует тип и значение:
  ```plaintext
  const PI(float) = 3.14159
  ```

### Переменные
- Определяются с указанием типа и значения:
  ```plaintext
  my_string(str) = "Hello, world!"
  ```

### Импорты
- Импорт других `.fl` файлов:
  ```plaintext
  (import) module_name
  ```

### Арифметические и логические операции
- Поддерживаются базовые арифметические (`+`, `-`, `*`, `/`, `%`) и логические операции (`<`, `>`, `=`):
  ```plaintext
  my_sum(float) = $my_int + $my_float
  my_logic_bool(bool) = $my_int < $my_float
  ```

## Расширение для Visual Studio Code

Улучшите визуализацию синтаксиса файлов `.fl` с помощью нашего расширения:
- [GitHub](https://github.com/FlacSy/FLSyntax)
- [VisualStudio Marketplace](https://marketplace.visualstudio.com/items?itemName=FLSyntax.fl-syntax-highlighter&ssr=false#review-details)

## Лицензия

FLK распространяется под [Apache License Version 2.0](LICENSE). Подробности лицензии доступны в файле LICENSE.