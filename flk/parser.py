import os
import re
from typing import Any, Dict, Union, Tuple
from flk.variable import Variable

DataType = Union[str, int, float, bool, list, dict, Tuple]

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
            var_type (str): Тип данных ('str', 'int', 'float', 'bool', 'list', 'dict').
            value (str): Строковое значение для парсинга.

        Возврат:
            DataType: Спарсенное значение соответствующего типа данных.

        Исключения:
            ValueError: Если тип данных не поддерживается.
        """
        if isinstance(value, str) and value.startswith("$"):
            return self.parse_reference(value[1:])
        elif var_type == 'str':
            value = f'{value}'
            value = value.strip()
            if value.startswith('"') & value.endswith('"'):
                return value[1:-1]
            elif value.startswith("'") & value.endswith("'"):
                return value[1:-1]
            else:
                raise ValueError(f"Строковая переменная должна быть обрамлена кавычками: {value}")
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
        elif var_type == 'set':
            return self.parse_set(value)
        elif var_type == 'tuple':
            return self.parse_tuple(value)
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
            elif re.match(r'^-?\d+(\.\d+)?$', item):  
                if '.' in item:
                    parsed_items.append(float(item))
                else:
                    parsed_items.append(int(item))
            elif item.lower() in ('true', 'false'): 
                parsed_items.append(item.lower() == 'true')
            else:
                parsed_items.append(self.parse_value("str", item))
        return parsed_items

    def parse_set(self, value: str) -> set:
        """
        Парсит строку в множество.

        Параметры:
            value (str): Строка, представляющая множество.

        Возврат:
            set: Множество спарсенных значений.
        """
        value = value.strip('{}')
        items = value.split(',')
        parsed_items = set()
        for item in items:
            item = item.strip()
            if item.startswith("$"):
                parsed_items.add(self.parse_reference(item[1:]))
            elif re.match(r'^-?\d+(\.\d+)?$', item):  
                if '.' in item:
                    parsed_items.add(float(item))
                else:
                    parsed_items.add(int(item))
            elif item.lower() in ('true', 'false'): 
                parsed_items.add(item.lower() == 'true')
            else:
                parsed_items.add(self.parse_value("str", item))
        return parsed_items

    def parse_tuple(self, value: str) -> tuple:
        """
        Парсит строку в кортеж.

        Параметры:
            value (str): Строка, представляющая кортеж.

        Возврат:
            tuple: Кортеж спарсенных значений.
        """
        value = value.strip('()')
        items = value.split(',')
        parsed_items = []
        for item in items:
            item = item.strip()
            if item.startswith("$"):
                parsed_items.append(self.parse_reference(item[1:]))
            elif re.match(r'^-?\d+(\.\d+)?$', item):  
                if '.' in item:
                    parsed_items.append(float(item))
                else:
                    parsed_items.append(int(item))
            elif item.lower() in ('true', 'false'): 
                parsed_items.append(item.lower() == 'true')
            else:
                parsed_items.append(self.parse_value("str", item))
        return tuple(parsed_items)

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

    def create_var(self, name: str, var_type: str, value: str) -> None:
        """
        Создает новую переменную и записывает ее в файл.

        Параметры:
            name (str): Имя переменной.
            var_type (str): Тип данных переменной ('str', 'int', 'float', 'bool', 'list', 'dict').
            value (str): Значение переменной в виде строки.

        Исключения:
            ValueError: Если переменная с таким именем уже существует.
        """
        if name in self.data:
            raise ValueError(f"Переменная {name} уже существует.")
        if var_type == 'str':
            parsed_value = self.parse_value(var_type, f'"{value}"')
        else:
            parsed_value = self.parse_value(var_type, value)

        self.data[name] = Variable(var_type, parsed_value)

        with open(self.current_file, 'a', encoding='utf-8') as file:
            file.write(f"\n{name}({var_type}) = {value}\n")

    def remove_var(self, name: str) -> None:
        """
        Удаляет переменную из файла.

        Параметры:
            name (str): Имя переменной.

        Исключения:
            ValueError: Если переменная с указанным именем не найдена.
        """
        if name not in self.data:
            raise ValueError(f"Переменная {name} не найдена.")

        del self.data[name]

        with open(self.current_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_lines = []
        var_assignment_pattern = re.compile(rf'(\b{name}\b)\((\w+)\) = (.+)')

        for line in lines:
            match = var_assignment_pattern.match(line.strip())
            if match:
                continue
            new_lines.append(line)

        with open(self.current_file, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

    def evaluate_expression(self, expression: str) -> Any:
        """
        Оценивает арифметическое выражение.

        Параметры:
            expression (str): Строка с арифметическим выражением.

        Возврат:
            Any: Результат вычисления выражения.
        """
        tokens = re.findall(r'[\d.]+|[\w]+|\$[\w]+|[\+\-\*/%()]', expression)
        result = []
        for token in tokens:
            if token.startswith('$'):
                result.append(str(self.parse_reference(token[1:])))
            elif token in self.constants:
                result.append(str(self.constants[token]))
            else:
                result.append(token)

        return round(eval(''.join(result)), 5)

    def parse_line(self, line: str) -> None:
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
                if name in self.data and self.data[name].get_type() != var_type:
                    raise TypeError(f"Переменная '{name}' уже определена с типом '{self.data[name].get_type()}'.")
                if any(op in value for op in "+-*/%"):
                    parsed_value = self.evaluate_expression(value)
                elif value.strip().startswith("$"):
                    parsed_value = self.parse_logical_expression(value)
                else:
                    if var_type == 'str':
                        parsed_value = self.parse_value(var_type, f'"{value.strip()}"')
                    else:
                        parsed_value = self.parse_value(var_type, value.strip())
            else:
                raise ValueError(f"Неправильный формат строки: {line}")

        if name in self.data:
            self.data[name].set_value(parsed_value)
        else:
            self.data[name] = Variable(var_type, parsed_value)

    def edit_var_value(self, var_name: str, new_var_value: str):
        """
        Изменяет значение переменной во всех файлах, включая импортированные.

        Параметры:
            var_name: Имя переменной.
            new_var_value: Новое значение переменной.
        """

        if var_name in self.data:
            var_type = self.data[var_name].get_type()
            parsed_value = self.parse_value(var_type, new_var_value)
            self.data[var_name].set_value(parsed_value)
        else:
            raise ValueError(f"Переменная {var_name} не найдена.")

        self.update_file_var_value(self.current_file, var_name, new_var_value)

    def update_file_var_value(self, file_path: str, var_name: str, new_var_value: str):
        """
        Изменяет значение переменной в указанном файле и его импортированных файлах.

        Параметры:
            file_path: Путь к файлу.
            var_name: Имя переменной.
            new_var_value: Новое значение переменной.
        """

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_lines = []
        var_assignment_pattern = re.compile(rf'(\b{var_name}\b)\((\w+)\) = (.+)')

        for line in lines:
            match = var_assignment_pattern.match(line.strip())
            if match:
                name, var_type, value = match.groups()
                if name == var_name:
                    new_line = f"{var_name}({var_type}) = {new_var_value}\n"
                    new_lines.append(new_line)
                    continue
            new_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('(import)'):
                    import_path = line.strip().split(' ')[1].strip('()')
                    import_file_path = f"{import_path.replace('.', '/')}.fl"
                    full_import_file_path = os.path.join(os.path.dirname(file_path), import_file_path)
                    self.update_file_var_value(full_import_file_path, var_name, new_var_value)


    def parse_logical_expression(self, expression: str) -> bool:
        """
        Парсит логическое выражение.

        Параметры:
            expression (str): Строка с логическим выражением.

        Возврат:
            bool: Результат логического выражения.
        """
        expression = expression.strip()
        match = re.match(r'\$([\w]+)\s*([><=])\s*\$([\w]+)', expression)
        if match:
            var1, operator, var2 = match.groups()
            value1 = self.parse_reference(var1)
            value2 = self.parse_reference(var2)
            if operator == ">":
                return value1 > value2
            elif operator == "<":
                return value1 < value2
            elif operator == "=":
                return value1 == value2
        else:
            raise ValueError(f"Неправильный формат логического выражения: {expression}")

    def parse_import(self, line: str):
        """
        Обрабатывает директивы импорта и загружает данные из указанного файла.

        Параметры:
            line (str): Строка, содержащая директиву импорта.
        """
        parts = line.strip().split(' ')
        if len(parts) > 1:
            import_path = parts[1].strip('()')
            path = f"{import_path.replace('.', '/')}.fl"
            full_path = os.path.join(os.path.dirname(self.current_file), path)
            original_file = self.current_file
            self.parse_file(full_path)
            self.current_file = original_file
        else:
            raise ValueError("Неправильный формат директивы импорта: " + line)

    def get_var(self, name: str) -> Variable:
        """
        Возвращает объект переменной по имени.

        Параметры:
            name (str): Имя переменной.

        Возврат:
            Variable: Объект переменной.
        """
        if name in self.data:
            return self.data[name]
        else:
            raise ValueError(f"Переменная {name} не найдена в файле.")

    def parse_file(self, filename: str) -> Dict[str, DataType]:
        """
        Парсит файл и возвращает данные в виде словаря.

        Параметры:
            filename (str): Имя файла для парсинга.
        """
        self.current_file = filename
        with open(filename, 'r', encoding='utf-8') as file:
            multiline_buffer = ""
            open_braces = 0
            in_multiline_comment = False
            for line in file:
                line = line.strip()
                if line.startswith('/*'):
                    in_multiline_comment = True
                if in_multiline_comment:
                    if '*/' in line:
                        in_multiline_comment = False
                    continue
                if line.startswith('(import)'):
                    self.parse_import(line)
                    continue
                if line and not line.startswith('#'):
                    if '{' in line:
                        open_braces += line.count('{')
                    if '}' in line:
                        open_braces -= line.count('}')
                    
                    multiline_buffer += line + " "
                    
                    if open_braces == 0 and multiline_buffer:
                        if multiline_buffer.startswith("const "):
                            self.parse_constant_line(multiline_buffer)
                        else:
                            self.parse_line(multiline_buffer)
                        multiline_buffer = ""  
                elif open_braces > 0:
                    multiline_buffer += line + " "
                    
        return {name: variable.value for name, variable in self.data.items()}