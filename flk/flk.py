import re
from typing import Any, Dict, Union

class Variable:
    """
    Класс для представления переменной с типом и значением.

    Атрибуты:
        type (str): Тип переменной (например, 'str', 'int', 'float', 'bool', 'list').
        value (Any): Значение переменной.
    """
    def __init__(self, var_type: str, value: Any):
        """
        Инициализация переменной.

        Параметры:
            var_type (str): Тип переменной.
            value (Any): Значение переменной.
        """
        self.type = var_type
        self.value = value

    def set_value(self, value: Any) -> None:
        """
        Устанавливает значение переменной.

        Параметры:
            value (Any): Новое значение переменной.
        """
        self.value = value

    def get_type(self) -> str:
        """
        Возвращает тип переменной.

        Возврат:
            str: Тип переменной.
        """
        return self.type

DataType = Union[str, int, float, bool, list]

class Parser:
    """
    Класс для парсинга и обработки данных из файла.

    Атрибуты:
        data (Dict[str, Variable]): Словарь для хранения переменных.
        constants (Dict[str, Any]): Словарь для хранения констант.
    """
    def __init__(self):
        """
        Инициализация парсера.
        """
        self.data: Dict[str, Variable] = {}
        self.constants: Dict[str, Any] = {}

    def parse_value(self, var_type: str, value: str) -> DataType:
        """
        Парсит значение строки в соответствующий тип данных.

        Параметры:
            var_type (str): Тип данных ('str', 'int', 'float', 'bool', 'list').
            value (str): Строковое значение для парсинга.

        Возврат:
            DataType: Спарсенное значение соответствующего типа данных.

        Исключения:
            ValueError: Если тип данных не поддерживается.
        """
        if isinstance(value, str) and value.startswith("$"):
            return self.parse_reference(value[1:])
        elif var_type == 'str':
            return value.strip()
        elif var_type == 'int':
            return int(value)
        elif var_type == 'float':
            return float(value)
        elif var_type == 'bool':
            return value.strip().lower() in ('да', 'true', '1')
        elif var_type == 'list':
            return self.parse_list(value)
        elif var_type == 'dict':
            return self.parse_dict(value)
        else:
            raise ValueError(f"Неизвестный тип данных: {var_type}")

    def parse_dict(self, value: str) -> dict:
        """
        Парсит строку в словарь значений.

        Параметры:
            value (str): Строка, представляющая словарь.

        Возврат:
            dict: Словарь спарсенных значений.
        """
        result = {}
        # Удаление пробелов и переносов строк для упрощения парсинга
        lines = re.sub(r'\s+', ' ', value.strip('{}')).split(',')
        for line in lines:
            line = line.strip()
            if line:
                match = re.match(r'(\w+)\((\w+)\) *: *(\w+)\((\w+)\) *= *(.+)', line)
                if match:
                    key, key_type, var_type, val_type, val = match.groups()
                    result[key] = self.parse_value(val_type, val.strip())
                else:
                    raise ValueError(f"Неправильный формат элемента словаря: {line}")
        return result
    
    def parse_reference(self, ref: str) -> Any:
        """
        Парсит ссылку на переменную или константу.

        Параметры:
            ref (str): Ссылка на переменную или константу.

        Возврат:
            Any: Значение переменной или константы.

        Исключения:
            ValueError: Если переменная или константа не определена.
        """
        if '.' in ref:
            obj, attr = ref.split('.')
            if obj in self.data:
                return self.data[obj].value[attr]
            else:
                raise ValueError(f"Объект {obj} не определен")
        elif ref in self.data:
            return self.data[ref].value
        elif ref in self.constants:
            return self.constants[ref]
        else:
            raise ValueError(f"Константа или переменная {ref} не определена")

    def parse_list(self, value: str) -> list:
        """
        Парсит строку в список значений.

        Параметры:
            value (str): Строка, представляющая список.

        Возврат:
            list: Список спарсенных значений.
        """
        value = value.strip('[]')
        items = value.split(',')
        parsed_items = []
        for item in items:
            item = item.strip()
            if item.startswith("$"):
                parsed_items.append(self.parse_reference(item[1:]))
            else:
                parsed_items.append(self.parse_value("str", item))
        return parsed_items

    def parse_constant_line(self, line: str) -> None:
        """
        Парсит строку с объявлением константы.

        Параметры:
            line (str): Строка, содержащая объявление константы.

        Исключения:
            ValueError: Если строка имеет неправильный формат.
        """
        match = re.match(r'const (\w+)\((\w+)\) = (.+)', line)
        if not match:
            raise ValueError(f"Неправильный формат строки: {line}")

        name, var_type, value = match.groups()
        value = value.strip()
        self.constants[name] = self.parse_value(var_type, value)

    def evaluate_expression(self, expression: str) -> str:
        """
        Оценивает арифметическое выражение.

        Параметры:
            expression (str): Строка с арифметическим выражением.

        Возврат:
            str: Результат вычисления выражения.
        """
        tokens = re.findall(r'[\d.]+|[\w]+|\$[\w]+|[\+\-\*/\(\)]', expression)
        result = []
        for token in tokens:
            if token.startswith('$'):
                result.append(str(self.parse_reference(token[1:])))
            elif token in self.constants:
                result.append(str(self.constants[token]))
            else:
                result.append(token)
        return str(eval(''.join(result)))

    def parse_line(self, line: str) -> None:
        """
        Парсит строку с объявлением переменной или присваиванием значения.

        Параметры:
            line (str): Строка с объявлением переменной или присваиванием значения.

        Исключения:
            ValueError: Если строка имеет неправильный формат.
        """
        line = line.split("//")[0].strip()
        if '{' in line:
            match = re.match(r'(\w+)\((\w+)\) = ({.*})', line, re.DOTALL)
            if match:
                name, var_type, value = match.groups()
                parsed_value = self.parse_value(var_type, value)
            else:
                raise ValueError(f"Неправильный формат строки: {line}")
        else:
            match = re.match(r'(\w+)\((\w+)\) = (.+)', line)
            if match:
                name, var_type, value = match.groups()
                parsed_value = self.parse_value(var_type, value.strip())
            else:
                raise ValueError(f"Неправильный формат строки: {line}")

        if name in self.data:
            self.data[name].set_value(parsed_value)
        else:
            self.data[name] = Variable(var_type, parsed_value)

    def parse_file(self, filename: str) -> Dict[str, DataType]:
        """
        Парсит файл и возвращает данные в виде словаря.

        Параметры:
            filename (str): Имя файла для парсинга.

        Возврат:
            Dict[str, DataType]: Словарь с данными из файла.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            multiline_buffer = ""
            open_braces = 0
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '{' in line:
                        open_braces += line.count('{')
                    if '}' in line:
                        open_braces -= line.count('}')
                    
                    multiline_buffer += line + " "
                    
                    if open_braces == 0 and multiline_buffer:
                        # Полный блок данных собран, парсим его
                        if multiline_buffer.startswith("const "):
                            self.parse_constant_line(multiline_buffer)
                        else:
                            self.parse_line(multiline_buffer)
                        multiline_buffer = ""  # Очистка буфера после парсинга
                elif open_braces > 0:
                    # Продолжаем собирать многострочный блок
                    multiline_buffer += line + " "
                    
        return {name: variable.value for name, variable in self.data.items()}
