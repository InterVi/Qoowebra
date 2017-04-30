"""Управление плагинами."""
import os
import sys
from core.plugin.template import Priority
from core.plugin.validator import is_valid


class PluginStorage:
    """Хранилище плагинов."""
    def __init__(self):
        self.__plugins__ = {
            Priority.lowest: {}, Priority.low: {}, Priority.middle: {},
            Priority.high: {}, Priority.highest: {}
        }
        """Словарь с плагинами.

        Ключи - Priority, значения - dict.
        {Priority.value: {name: plugin, ...}, ...}
        """
        self.__names__ = {}
        """Словарь с приоритетами.
        Ключи - имена плагинов, значения - Priority."""
        self.__info__ = {}

    def get_all_plugins(self):
        """Получить имена всех плагинов.

        :return: dict_keys
        """
        return self.__names__.keys()

    def get_plugins(self, priority):
        """Получить имена приложений.

        :param priority: Priority, приоритет
        :return: dict_keys
        """
        return self.__plugins__[priority].keys()

    def get_plugin(self, name):
        """Получить плагин.

        :param name: str, имя плагина
        :return: плагин
        """
        return self.__plugins__[self.__names__[name]][name]

    def get_info(self, name):
        """Получить информацию о плагине.

        :param name: str, имя плагина
        :return: dict, ключи: DESCRIPTION, AUTHOR, EMAIL, URL, PATH
        """
        return self.__info__[name]

    def get_priority(self, name):
        """Получить приоритет плагина.

        :param name: str, имя плагина
        :return: Priority
        """
        return self.__names__[name]

    def __add__(self, priority, name, plugin, info):
        """Добавить плагин.

        :param priority: Priority, приоритет
        :param name: str, имя плагина
        :param plugin: плагин
        :param info: dict, информация о плагине
        """
        self.__names__[name] = priority
        self.__plugins__[priority][name] = plugin
        self.__info__[name] = info


class PluginManager:
    """Менеджер плагинов."""
    def __init__(self, field_storage, maker, db):
        """

        :param field_storage: FieldStorage из cgi
        :param maker: maker, сборщик темы
        :param db: база данных
        """
        self._field_storage = field_storage
        """FieldStorage из cgi."""
        self._maker = maker
        """maker, сборщик тем."""
        self.db = db
        """База данных."""
        self.plugin_storage = PluginStorage()
        self.PATH = os.path.join(sys.path[0], 'plugins')
        """Путь к директории с плагинами."""
        self.__no_load = False

    def __load__(self, pack):
        """Загрузить плагин.

        :param pack: пакет плагина
        """
        if self.__no_load:  # загрузка плагинов отключена
            return
        # инициализация
        main = pack.get_main()(self._field_storage, self._maker, self)
        if not main.load():  # вызов события
            return
        info = {
            'DESCRIPTION': pack.DESCRIPTION,
            'AUTHOR': pack.AUTHOR,
            'EMAIL': pack.EMAIL,
            'URL': pack.URL,
            'PATH': os.path.dirname(pack.__file__)
        }
        self.plugin_storage.__add__(pack.PRIORITY, pack.NAME, main, info)

    def load_from_path(self, path):
        """Загрузить плагин.

        :param path: str, путь к пакету плагина
        """
        self.__load__(__import__(path))

    @staticmethod
    def get_sort(paths):
        """Сортировка плагинов по приоритету.

        :param paths: iterable, список с путями к плагинам
        :return: dict, {Priority.value: {name: пакет плагина, ...}, ...}
        """
        result = {
            Priority.lowest: {}, Priority.low: {}, Priority.middle: {},
            Priority.high: {}, Priority.highest: {}
        }
        for path in paths:
            pack = __import__(path)
            result[pack.PRIORITY][pack.NAME] = pack
        return result

    def unload(self, name):
        """Отгрузить плагин (вызывает unload и удаляет из словарей).

        :param name: str, имя плагина
        """
        self.plugin_storage.get_plugin(name).unload()
        ps = self.plugin_storage
        del ps.__plugins__[ps.__names__[name]][name]
        del ps.__names__[name]
        del ps.__info__[name]

    def break_load(self):
        """Отключает загрузку плагинов."""
        self.__no_load = True

    def repair_load(self):
        """Включает загрузку плагинов."""
        self.__no_load = False

    def get_widgets_info(self, admin=False):
        """Получить информацию о виджетах из всех плагинов.

        :param admin: bool, True - о виджетах для админ панели
        :return: dict, ключи - имена плагинов, значения - tuple
        (имя виджета, описание в html)
        """
        result = {}
        for name in self.plugin_storage.get_all_plugins():
            if admin:
                result[name] = self.plugin_storage.get_plugin(
                    name).get_admin_widgets_info()
            else:
                result[name] =\
                    self.plugin_storage.get_plugin(name).get_widgets_info()
        return result


class PluginScanner:
    """Поисковик плагинов."""
    def __init__(self):
        self.PATH_PLUGINS = os.path.join(sys.path[0], 'plugins')
        """Путь к директории с плагинами."""
        self.PATH_THEMES = os.path.join(sys.path[0], 'themes')
        """Путь к директории с темами."""
        self.PATH_MODULES = os.path.join(sys.path[0], 'modules')
        """Путь к директории с модулями."""

    @staticmethod
    def __get_from_dir__(path):
        """Получить пути к субдиректориям.

        :param path: str, путь к директории
        :return: list с путями к субдиректориям
        """
        result = []
        for d in os.listdir(path):
            file = os.path.join(path, d)
            if not os.path.isdir(file) or d == '__pycache__':
                continue
            result.append(file)
        return result

    def get_from_plugins(self):
        """Получить пути к субдиректориям из директории с плагинами.

        :return: list с путями к субдиректориям
        """
        return self.__get_from_dir__(self.PATH_PLUGINS)

    def __get_from_subdir(self, path):
        """Получить пути к субдиректориям из субдиректории plugins.
        Предназначается для получения плагинов из тем.

        :param path: str, путь к директории
        :return: list с путями к субдиректориям из plugins
        """
        result = []
        for d in os.listdir(path):
            file = os.path.join(path, d)
            if not os.path.isdir(file) or d == '__pycache__':
                continue
            plugins = os.path.join(file, 'plugins')
            if os.path.isdir(plugins):
                result += self.__get_from_dir__(plugins)
        return result

    def get_from_themes(self):
        """Получить пути к плагинам тем.

        :return: list с путями к плагинам
        """
        return self.__get_from_subdir(self.PATH_THEMES)

    def get_from_modules(self):
        """Получить пути к плагинам модулей.

        :return: list с путями к плагинам
        """
        return self.__get_from_subdir(self.PATH_MODULES)

    def get_all(self):
        """Полуить пути ко всем плагинам (из директории с плагинами, из тем
        и модулей).

        :return: list с путями к плагинам
        """
        return self.get_from_plugins() + self.get_from_themes() +\
            self.get_from_modules()


plugin_manager = None
"""PluginManager."""
plugin_list = None
"""Список с путями к плагинам."""


def __init__(field_storage, maker, db, plugins):
    """Инициализация модуля.

    :param field_storage: FieldStorage из cgi
    :param maker: maker, сборщик тем
    :param db: база данных
    :param plugins: список путей к плагинам
    """
    global plugin_manager, plugin_list
    plugin_manager = PluginManager(field_storage, maker, db)
    plugin_list = plugins


def load(valid=True):
    """Загрузить плагины из списка, переданного при инициализации.

    :param valid: bool, True - проверять плагины
    """
    if valid:
        global plugin_list
        for p in plugin_list:  # чистка от не валидных плагинов
            if not is_valid(p):
                plugin_list.remove(p)
    sort = plugin_manager.get_sort(plugin_list)  # сортировка по приоритетам
    keys = list(sort.keys())
    keys.sort()  # сортировка ключей (приоритетов)
    for pri in keys:  # загрузка в порядке по приоритетам
        names = list(sort[pri].keys())
        names.sort()  # сортировка имён плагинов по алфавиту
        for name in names:  # загрузка по отсортированным именам
            plugin_manager.__load__(sort[pri][name])
