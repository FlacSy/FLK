import re
from typing import Any, Dict, Union

class Variable:
    def __init__(self, var_type: str, value: Any):
        self.type = var_type
        self.value = value

    def set_value(self, value: Any) -> None:
        self.value = value

    def get_type(self) -> str:
        return self.type

DataType = Union[str, int, float, bool, list]

class Parser:
    def __init__(self):
        self.data: Dict[str, Variable] = {}
        self.constants: Dict[str, Any] = {}

    def parse_value(self, var_type: str, value: str) -> DataType:
        # Оставляем логику парсинга значения без изменений
        if value.startswith("$"):
            constant_name = value[1:]
            if constant_name in self.constants:
                return self.constants[constant_name]
            elif constant_name in self.data:
                return self.data[constant_name].value
            else:
                raise ValueError(f"Константа или переменная {constant_name} не определена")
        elif var_type == 'str':
            return value.strip()
        elif var_type == 'int':
            return int(value)
        elif var_type == 'float':
            return float(value)
        elif var_type == 'bool':
            return value.strip().lower() in ('да', 'true', '1')
        elif var_type == 'list':
            value = value.strip('[]')
            items = value.split(',')
            parsed_items = []
            for item in items:
                if item.strip().startswith("$"):
                    parsed_items.append(self.parse_value(var_type, item.strip()))
                else:
                    parsed_items.append(self.parse_reference(item.strip()))
            return parsed_items
        else:
            raise ValueError(f"Неизвестный тип данных: {var_type}")



    def parse_reference(self, ref: str) -> Any:
        # Оставляем логику парсинга ссылок без изменений
        if '.' in ref:
            obj, attr = ref.split('.')
            return self.data[obj].value[attr]
        elif ref in self.data:
            return self.data[ref].value
        elif ref.startswith("$"):
            constant_name = ref[1:]
            if constant_name in self.constants:
                return self.constants[constant_name]
            else:
                raise ValueError(f"Константа {constant_name} не определена")
        else:
            return self.parse_value("str", ref)




    def parse_line(self, line: str) -> None:
        # Игнорируем комментарии в конце строки
        line = line.split("//")[0].strip()
        
        # Оставляем логику парсинга строки без изменений
        match = re.match(r'(\w+)\((\w+)\) = (.+)', line)
        if not match:
            raise ValueError(f"Неправильный формат строки: {line}")
        
        name, var_type, value = match.groups()
        if var_type == 'list':
            value = value.strip()
        # elif var_type == 'str':
        #     if value.startswith('"') and value.endswith('"'):
        #         value = value.strip('"')
        if name in self.data:
            self.data[name].set_value(self.parse_value(var_type, value))
        else:
            self.data[name] = Variable(var_type, self.parse_value(var_type, value))

    def parse_constant_line(self, line: str) -> None:
        # Логика парсинга строки для констант
        match = re.match(r'const (\w+)\((\w+)\) = (.+)', line)
        if not match:
            raise ValueError(f"Неправильный формат строки: {line}")

        name, var_type, value = match.groups()
        value = value.strip()
        self.constants[name] = self.parse_value(var_type, value)


    def parse_file(self, filename: str) -> Dict[str, DataType]:
        # Обновленная логика парсинга файла
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith("const "):
                        self.parse_constant_line(line)
        # Parse variable lines after parsing constant lines
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    if not line.startswith("const "):
                        self.parse_line(line)
        return {name: variable.value for name, variable in self.data.items()}