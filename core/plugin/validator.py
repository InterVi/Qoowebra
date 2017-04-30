"""Проверка плагинов."""
import os
# from core.plugin.template import Priority


def is_valid(path):
    """Проверить путь к плаину.

    :param path: str, путь к плагину
    :return: bool, True - это валидный плагин
    """
    path_init = os.path.join(path, '__ini__.py')
    if not os.path.isfile(path_init):
        return False
    pack = __import__(path)
    d = pack.__dict__

    def check_type(key, type_):
        """Проверить наличие ключа и его тип в d.

        :param key: str, ключ
        :param type_: тип
        :return: bool, True если проверки успешны
        """
        if key not in d:
            return False
        if type(d[key]) != type_:
            return False
        return True

    for s in ('NAME', 'DESCRIPTION', 'AUTHOR', 'EMAIL', 'URL'):
        if not check_type(s, str):
            return False
    # if not check_type('PRIORITY', Priority):
        # return False
    if 'get_main' not in d or not callable(d['get_main']):
        return False
    return True
