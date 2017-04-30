"""Проверка БД."""
import core.plugin.validator as p_val


def is_valid(path):
    """Проверить путь к БД.

    :param path: str, путь к БД
    :return: bool, True - это валидная БД
    """
    return p_val.is_valid(path)  # проверки пока одинаковы
