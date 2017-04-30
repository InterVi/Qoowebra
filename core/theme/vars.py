"""Модуль для работы с секцией VARS."""
import os
from enum import IntEnum


class VarType(IntEnum):
    """Тип переменной."""
    path = 0
    user_path = 1
    url_user_path = 2
    select = 3
    text = 4
    text_html = 5
    color = 6
    page = 7


def transform(section_vars, path_theme):
    """Преобразование секции VARS. Тектовый тип заменяется на VarType,
    {path} на path_theme.

    :param section_vars: dict, секция VARS
    :param path_theme: str, доменный путь к папке с темой
    :return: dict, преобразованная секция VARS
    """
    result = section_vars.copy()
    for section, value in result.items():
        typ = None
        if value['TYPE'].lower() in VarType._member_map_:
            typ = VarType._member_map_[value['TYPE'].lower()]
        value['TYPE'] = typ
        value['CONTENT'] = value['CONTENT'].replace('{path}', path_theme)
        result[section] = value
    return result


class ConfigMap:  # в процессе
    def __init__(self, conf, domain, path_theme):
        self.tags = {}
        self.tags_menus = {}
        self.tags_widgets = {}
        self.vars = transform(conf['VARS'], domain + '/themes/' +
                              os.path.basename(path_theme))
        self._conf = conf
        self.DOMAIN = domain
        self.PATH_THEME = path_theme
