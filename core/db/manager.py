"""Управление базами данных."""
import os
import sys
from core.db.validator import is_valid

__packs = {}


def __init__(valid=True):
    """Импортировать и сохранить все пакеты баз данных.

    :param valid: bool, True - отсекать не валидные БД
    """
    global __packs
    path = os.path.join(sys.path[0], 'dbs')
    sys.path.append(path)
    for d in os.listdir(path):
        file = os.path.join(path, d)
        if not os.path.isdir(file) or d == '__pycache__':
            continue
        if valid and not is_valid(file):
            continue
        p = __import__(file)
        __packs[p.NAME] = p


def get_names():
    """Получить имена загруженных БД.

    :return: tuple
    """
    return tuple(__packs.keys())


def get_info(name):
    """Получить информацию о БД.

    :param name: str, имя БД
    :return: dict, ключи: DESCRIPTION, AUTHOR, EMAIL, URL, содержимое - str
    """
    if name in __packs:
        pack = __packs[name]
        return {
            'DESCRIPTION': pack.DESCRIPTION,
            'AUTHOR': pack.AUTHOR,
            'EMAIL': pack.EMAIL,
            'URL': pack.URL
        }


def get_info_all():
    """Получить информацию о всех БД.

    :return: dict, {имя: {DESCRIPTION: str, AUTHOR: str, EMAIL: str, URL: str}}
    """
    result = {}
    for name in __packs.items():
        result[name] = get_info(name)
    return result


def get_main(name):
    """Получить главный класс БД.

    :param name: str, имя БД
    :return: класс, унаследованный от DB из template
    """
    if name in __packs:
        return __packs[name].get_main()
