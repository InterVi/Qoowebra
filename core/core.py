"""Главный модуль логики, собирающий всё вместе."""
import core.db.manager as db_manager
import core.plugin.event_manager as event_manager
import core.plugin.plugin_manager as plugin_manager
from core.plugin.widget_manager import WidgetManager
from core.module.manager import ModuleManager
import core.plugin.maker_iface as maker_iface
import core.theme.maker as maker
from configparser import ConfigParser
import json
import os
import sys

PATH_MAIN = os.path.join(sys.path[0], 'conf', 'main.conf')
"""Путь к главному конфигу."""
PATH_CHOICE = os.path.join(sys.path[0], 'conf', 'choice.json')
"""Путь к choice.json"""
PATH_PLUGINS = os.path.join(sys.path[0], 'conf', 'plugins.json')
"""Путь к plugins.json"""
PATH_MODULES = os.path.join(sys.path[0], 'conf', 'modules.json')
"""Путь к modules.json"""
PATH_CGITB = os.path.join(sys.path[0], 'content', 'logs', 'cgitb')
"""Путь к директории для логов cgitb."""
PATH_PROFILE = os.path.join(sys.path[0], 'content', 'logs', 'profile')
"""Путь к директории для логов cProfile."""

config = ConfigParser()
"""Главный конфиг (ConfigParser)."""
choice = {
    'theme': 'Glass',
    'sub_theme': 'main',
    'index': 'IndexPage',
    'index_name': None
}
"""Конфиг choice.json (dict)."""
plugins = [os.path.join(sys.path[0], 'plugins', 'EasyWidgets')]
"""Пути к плагинам (plugins.json, list)."""
modules = [('IndexPage', None)]
"""modules.json (list).
[(str, str), ...], [(имя модуля, параметр name), ...]"""

db = None
widget_manager = None
module_manager = None


def __init__():
    """Инициализация модуля: загрузка всех конфигов."""
    config.read(PATH_MAIN, 'utf-8')
    global choice, plugins, modules
    # choice.json
    if os.path.isfile(PATH_CHOICE):
        with open(PATH_CHOICE, 'r', encoding='utf-8') as file:
            choice = json.load(file)
    else:
        with open(PATH_CHOICE, 'w', encoding='utf-8') as file:
            json.dump(choice, file)
    # plugins.json
    if os.path.isfile(PATH_PLUGINS):
        with open(PATH_PLUGINS, 'r', encoding='utf-8') as file:
            plugins = json.load(file)
    else:
        with open(PATH_PLUGINS, 'w', encoding='utf-8') as file:
            json.dump(plugins, file)
    # module.json
    if os.path.isfile(PATH_MODULES):
        with open(PATH_MODULES, 'r', encoding='utf-8') as file:
            modules = json.load(file)
    else:
        with open(PATH_MODULES, 'w', encoding='utf-8') as file:
            json.dump(modules, file)
    # создание директорий
    logs = os.path.join(sys.path[0], 'logs')
    if not os.path.isdir(logs):
        os.mkdir(logs)
    if not os.path.isdir(PATH_CGITB):
        os.mkdir(PATH_CGITB)
    if not os.path.isdir(PATH_PROFILE):
        os.mkdir(PATH_PROFILE)


def run(field_storage):
    """Запуск движка.

    :param field_storage: FieldStorage из cgi
    :return: tuple, (tuple, str, tuple), (header, content, cookies),
    (строки, строка, Cookie из cookies)
    """
    global db, widget_manager, module_manager
    maker.__init__(os.path.join(sys.path[0], 'themes', choice['theme']),
                   choice['sub_theme'])
    # инициализация базы данных
    db_manager.__init__(config['VALID']['dbs'])
    db = db_manager.get_main(config['DB']['name'])
    del config['DB']['name']
    db = db(**config['DB'])
    # инициализация плагинов
    plugin_manager.__init__(field_storage, maker, db, plugins)
    plugin_manager.load(config['VALID']['plugins'])
    event_manager.__init__(plugin_manager.plugin_manager.plugin_storage)
    state, content = event_manager.pre_load()
    if not state:
        return content, ()
    maker_iface.__init__(event_manager, maker)
    widget_manager = WidgetManager()
    # пре-инициализация модуля
    module_manager = ModuleManager(maker, maker_iface, event_manager, db,
                                   field_storage, plugin_manager,
                                   widget_manager, config['MAIN']['domain'])
    name = None
    module_name = choice['index']
    if 'name' in field_storage:
        name = field_storage['name'].value
    if 'module' in field_storage:
        module_name = field_storage['module']
    module_name, name = event_manager.pre_load_module(module_name, name)
    widget_manager.load(plugin_manager, module_name)  # загрузка виджетов
    module = module_manager.get_module(module_name, name,  # инициализация
                                       config['VALID']['modules'])
    event_manager.loaded_module(module)
    content = module.make()  # получение содержимого страницы
    cookies = module.get_cookies() + event_manager.get_cookies()  # куков
    header = module.get_header() + event_manager.get_header()  # заголовков
    try:
        return header, content, cookies
    finally:
        event_manager.exit_script()
