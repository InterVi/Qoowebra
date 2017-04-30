"""Модуль для вызова всех плагинов. Документацию по одноимённым функциям
см. в Plugin из core.template."""
from core.plugin.template import Priority


_storage = None
"""PluginStorage, переданный при инициализации."""
_plugins = ()
"""Список плагинов, отсортированный по приоритету и алфавиту."""


def __get_sorted__():
    """Получить отсортированый список плагинов - по приоритету и алфавиту.

    :return: list с плагинами
    """
    result = []
    keys = list(Priority.__members__.values())
    keys.sort()  # сортировка по приоритету
    for key in keys:
        names = list(_storage.get_plugins(key))
        names.sort()  # сортировка по алфавиту
        for name in names:
            result.append(_storage.get_plugin(name))
    return result


def __init__(plugin_storage):
    """Инициализация модуля.

    :param plugin_storage: PluginStorage
    """
    global _storage, _plugins
    _storage = plugin_storage
    _plugins = __get_sorted__()


def pre_load_module(module, name):
    for p in _plugins:
        module, name = p.pre_load_module(module, name)
    return module, name


def loaded_module(module):
    for p in _plugins:
        p.loaded_module(module)


def exit_script():
    for p in _plugins:
        p.exit()


def pre_load(state=True, content=''):
    for p in _plugins:
        state, content = p.pre_load(state, content)
    return state, content


def pre_print(page):
    for p in _plugins:
        page = p.pre_print(page)
    return page


def set_data(title, keywords, description, content):
    for p in _plugins:
        title, keywords, description, content = p.set_data(title, keywords,
                                                           description,
                                                           content)
    return title, keywords, description, content


def add_tag(page, tag, value):
    for p in _plugins:
        page, tag, value = p.add_tag(page, tag, value)
    return page, tag, value


def add_tag_menu(menu, pos, sub_pos, tag, value):
    for p in _plugins:
        menu, pos, sub_pos, tag, value = p.add_tag_menu(menu, pos, sub_pos,
                                                        tag, value)
    return menu, pos, sub_pos, tag, value


def add_tag_widget(sidebar, pos, tag, value):
    for p in _plugins:
        sidebar, pos, tag, value = p.add_tag_widget(sidebar, pos, tag, value)
    return sidebar, pos, tag, value


def add_menu_element(menu, pos, name, link, target):
    for p in _plugins:
        menu, pos, name, link, target = p.add_menu_element(menu, pos, name,
                                                           link, target)
    return menu, pos, name, link, target


def add_menu_sub_element(menu, pos, sub_pos, name, link, target):
    for p in _plugins:
        menu, pos, sub_pos, name, link, target =\
            p.add_menu_sub_element(menu, pos, sub_pos, name, link, target)
    return menu, pos, sub_pos, name, link, target


def add_widget(sidebar, pos, name, content):
    for p in _plugins:
        sidebar, pos, name, content = p.add_widget(sidebar, pos, name, content)
    return sidebar, pos, name, content


def pre_make(result):
    for p in _plugins:
        result = p.pre_make(result)
    return result


def make(page):
    for p in _plugins:
        page = p.make(page)
    return page


def pre_send_cookies(cookies):
    for p in _plugins:
        cookies = p.pre_send_cookies(cookies)
    return cookies


def get_cookies():
    """Получить Cookies от всех плагинов.

    :return: tuple с объектами Cookie из core.cookies
    """
    result = ()
    for p in _plugins:
        result += p.get_cookies()
    return result


def get_header():
    """Получить http заголовки, передаваемые клиенту, от всех плагинов.

    :return: tuple со строками
    """
    result = ()
    for p in _plugins:
        result += p.get_header()
    return result
