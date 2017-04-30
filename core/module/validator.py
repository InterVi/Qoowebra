"""Проверка модулей."""
import core.plugin.validator as p_val


def is_valid(path):
    """Проверить путь к модулю.

    :param path: str, путь к модулю
    :return: bool, True - это валидный модуль
    """
    return p_val.is_valid(path)  # проверки пока одинаковы
