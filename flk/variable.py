from typing import Any

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

    def get_value(self):
        return self.value