"""Управление темами."""
import os
import sys
from configparser import ConfigParser

__themes = {}
"""Информация о темах.

{
    имя: {
        INFO: {default: str, author: str, description: str, screenshot: str,
               url: str},
        SUB: {
            имя: {description: str, module: str, plugin: str, screenshot: str}
        }
    }
}
"""


def __init__():
    """Загрузить темы."""
    global __themes
    path = os.path.join(sys.path[0], 'themes')
    for d in os.listdir(path):
        path_dir = os.path.join(path, d)
        if not os.path.isdir(path_dir):  # фильтр не директорий
            continue
        path_conf = os.path.join(path_dir, 'conf')  # папка с конфигами
        path_theme = os.path.join(path_dir, 'theme.conf')  # главный конфиг
        if os.path.isfile(path_theme) and os.path.isdir(path_conf):
            sub_info = {}
            for sub in os.listdir(path_conf):  # обработка подтем
                path_sub = os.path.join(path_conf, sub)
                if os.path.isfile(path_sub):
                    sub_parser = ConfigParser()
                    sub_parser.read(path_sub)
                    spi = sub_parser['INFO']
                    if spi['select'] == 'no':  # тему нельзя выбирать
                        continue
                    sub_info[spi['name']] = {  # заполнение информации
                        'description': spi['description'],
                        'module': spi['module'],
                        'plugin': spi['plugin']
                    }
                    if 'screenshot' in spi:  # не обязательный параметр
                        sub_info[spi['name']]['screenshot'] = spi['screenshot']
            parser = ConfigParser()
            parser.read(path_theme)
            pi = parser['INFO']
            __themes[pi['name']] = {
                'INFO': {
                    'default': pi['default'],
                    'author': pi['author'],
                    'description': pi['description'],
                }, 'SUB': sub_info
            }
            if 'screenshot' in pi:
                __themes[pi['name']]['INFO']['screenshot'] = pi['screenshot']
            if 'url' in pi:
                __themes[pi['name']]['INFO']['url'] = pi['url']


def get_themes():
    """Получить названия тем.

    :return: tuple
    """
    return tuple(__themes.keys())


def __get_sub_themes(name, module='main', plugin='none'):
    """Получить имена суб-темы для модуля или плагина.

    :param name: str, имя темы
    :param module: str, имя модуля
    :param plugin: str, имя плагина
    :return: list
    """
    if name in __themes:
        result = []
        for sub, val in __themes[name]['SUB'].items():
            if val['module'] == module and val['plugin'] == plugin:
                result.append(sub)
        return result
    return []


def get_default(name):
    """Получить суб-тему по-умолчанию.

    :param name: str, имя темы
    :return: str или None
    """
    if name in __themes:
        return __themes[name]['INFO']['default']


def get_sub_themes(name):
    """Получить имена суб-тем.

    :param name: str, имя темы
    :return: list
    """
    return __get_sub_themes(name)


def get_module_themes(module, name=None):
    """Получить имена суб-тем для модуля.

    :param module: str, имя модуля
    :param name: str, имя темы (при None - поиск по всем темам)
    :return: list (если name != None) или dict
    (ключи - имена тем, содержимое - list)
    """
    if name:
        return __get_sub_themes(name, module)
    else:
        result = {}
        for theme in __themes:
            st = __get_sub_themes(theme, module)
            if st:
                result[theme] = st
        return result


def get_plugin_themes(plugin, name=None):
    """Получить имена суб-тем для плагина.

    :param plugin: str, имя плагина
    :param name: str, имя темы (при None - поиск по всем темам)
    :return: list (если name != None) или dict
    (ключи - имена тем, содержимое - list)
    """
    if name:
        return __get_sub_themes(name, plugin=plugin)
    else:
        result = {}
        for theme in __themes:
            st = __get_sub_themes(theme, plugin=plugin)
            if st:
                result[theme] = st
        return result
