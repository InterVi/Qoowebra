"""Управление виджетами."""
import os
import sys
import json
from uuid import UUID


class WidgetStorage:
    """Хранилище виджетов."""
    def __init__(self):
        self.__widgets__ = {}
        """Словарь с виджетами. Ключи - UUID, значения - виджеты."""
        self.__data__ = {}
        """Словарь с данными. {module: {sidebar: {pos: (name, uuid)}}}"""
        self.__uuids__ = {}
        """Словарь с информацией о виджетах. Ключи - UUID, значения - tuple.
        (module, sidebar, pos, name)"""

    def get_all_uuids(self):
        """Получить все UUID.

        :return: dict_keys
        """
        return self.__widgets__.keys()

    def __get_widget_un(self, module, sidebar, u=True):
        """Получить UUID-ы или названия виджетов.

        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :param u: bool, True - UUID, False - имена
        :return: list
        """
        result = []
        if module in self.__data__ and sidebar in self.__data__[module]:
            dms = list(self.__data__[module][sidebar])
            dms.sort()
            for key in dms:
                value = self.__data__[module][sidebar][key]
                if u:
                    result.append(value[1])
                else:
                    result.append(value[0])
        return result

    def get_uuids(self, module, sidebar):
        """Получить UUID-ы виджетов.

        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :return: list
        """
        return self.__get_widget_un(module, sidebar)

    def get_names(self, module, sidebar):
        """Получить имена виджетов.

        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :return: list
        """
        return self.__get_widget_un(module, sidebar, False)

    def get_widget(self, uuid):
        """Получить виджет.

        :param uuid: UUID виджета
        :return: виджет
        """
        return self.__widgets__[uuid]

    def get_from_pos(self, module, sidebar, pos):
        """Получить виджет.

        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :param pos: позиция
        :return: виджет
        """
        return self.__widgets__[self.__data__[module][sidebar][pos][1]]

    def get_sidebar(self, module, sidebar):
        """Получить UUID-ы виджетов.

        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :return: tuple
        """
        return (self.get_widget(u) for u in self.get_uuids(module, sidebar))

    def get_info(self, uuid):
        """Получить информацию о виджите.

        :param uuid: UUID виджета
        :return: tuple, (module, sidebar, pos, name)
        """
        return self.__uuids__[uuid]

    def __add__(self, uuid, module, sidebar, pos, name, widget):
        """Добавить виджет.

        :param uuid: UUID виджета
        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :param pos: позиция
        :param name: имя виджета
        :param widget: виджет
        """
        self.__widgets__[uuid] = widget
        self.__uuids__[uuid] = (module, sidebar, pos, name)
        if module in self.__data__:
            if sidebar in self.__data__[module]:
                self.__data__[module][sidebar][pos] = (name, uuid)
            else:
                self.__data__[module] = {sidebar: {pos: (name, uuid)}}
        else:
            self.__data__[module] = {sidebar: {pos: (name, uuid)}}


class WidgetCompliance:
    """Хранилище соответствий виджетов плагинам."""
    def __init__(self):
        self.__plugins__ = {}
        """Словарь с данными по плагинам. Ключи - имена плагинов,
        значения - list [(UUID, имя виджета), ...]."""
        self.__uuids__ = {}
        """Словарь с данными по UUID-ам. Ключи - UUID виджетов,
        значения - tuple (имя плагина, имя виджета)."""

    def __add__(self, uuid, plugin, name):
        """Добавить соответствие.

        :param uuid: UUID виджета
        :param plugin: str, имя плагина
        :param name: str, имя виджета
        """
        self.__uuids__[uuid] = (plugin, name)
        if plugin in self.__plugins__:
            self.__plugins__[plugin].append((uuid, name))
        else:
            self.__plugins__[plugin] = [(uuid, name)]

    def get_from_plugin(self, plugin):
        """Получить UUID-ы и имя виджетов.

        :param plugin: имя плагина
        :return: iterable, [(UUID, имя виджета), ...]
        """
        if plugin in self.__plugins__:
            return self.__plugins__[plugin]
        return ()

    def get_from_uuid(self, uuid):
        """Получить имя плагина и имя виджета.

        :param uuid: UUID виджета
        :return: tuple, (имя плагина, имя виджета)
        """
        if uuid in self.__uuids__:
            return self.__uuids__[uuid]
        return ()

    def get_from_name(self, plugin, name):
        """Получить UUID виджета.

        :param plugin: str, имя плагина
        :param name: str, имя виджета
        :return: UUID или None (если не найден)
        """
        all_list = self.get_from_plugin(plugin)
        for a in all_list:
            if a[1] == name:
                return a[0]


class WidgetManager:
    """Менеджер виджетов."""
    def __init__(self):
        self.widget_storage = WidgetStorage()
        """Хранилище виджетов."""
        self.widget_compliance = WidgetCompliance()
        """Хранилище соответствий виджетов плагинам."""
        self._PATH_JSON = os.path.join(sys.path[0], 'conf', 'widgets.json')
        """Путь к конфигу JSON с информацией о установленных виджетах."""

    def add(self, uuid, module, sidebar, pos, name, widget, plugin):
        """Добавить виджет в хранилища.

        :param uuid: UUID виджета
        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :param pos: позиция
        :param name: str, имя виджета
        :param widget: виджет
        :param plugin: str, имя плагина
        """
        self.widget_storage.__add__(uuid, module, sidebar, pos, name, widget)
        self.widget_compliance.__add__(uuid, plugin, name)
        self.__save__()

    def __convert__(self, to_uuid=False):
        """Конвертация UUID из хранилищ в str и наоборот.

        :param to_uuid: bool, True - str -> UUID, False - UUID -> str
        :return: tuple, (WidgetCompliance.__uuids__,
        WidgetCompliance.__plugins__, WidgetStorage.__data__,
        WidgetStorage.__uuids__), где все UUID заменены на str или наоборот
        """
        def con(arg):
            """Конвертация.

            :param arg: UUID или str для конвертации
            :return: UUID или str, в зависимости от значения to_uuid
            """
            if to_uuid:
                return UUID(arg)
            return str(arg)

        wc_uuids = {}  # WidgetCompliance.__uuids__
        wc_plugins = {}  # WidgetCompliance.__plugins__
        ws_data = {}  # WidgetStorage.__data__
        ws_uuids = {}  # WidgetStorage.__uuids__
        for key, value in self.widget_compliance.__uuids__.items():
            wc_uuids[con(key)] = value
        for key, value in self.widget_compliance.__plugins__.items():
            v = []
            for val in value:
                v.append((con(val[0]), val[1]))
            wc_plugins[key] = v
        # {module: {sidebar: {pos: (name, uuid)}}}
        # | 1 слой                               |
        #          | 2 слой                     |
        #                    | 3 слой          |
        for key, value in self.widget_storage.__data__.items():  # первый слой
            for key1, value1 in value.items():  # второй слой
                for key2, value2 in value1.items():  # третий слой
                    if key in ws_data:
                        if key1 in ws_data[key]:
                            ws_data[key][key1][key2] =\
                                (value2[0], con(value2[1]))
                        else:
                            ws_data[key][key1] =\
                                {key2: (value2[0], con(value2[1]))}
                    else:
                        ws_data[key] =\
                            {key1: {key2: (value2[0], con(value2[1]))}}
        for key, value in self.widget_storage.__uuids__.items():
            ws_uuids[con(key)] = value
        return wc_uuids, wc_plugins, ws_data, ws_uuids

    def __save__(self):
        """Сохранить конфиг."""
        with open(self._PATH_JSON, 'w', encoding='utf-8') as file:
            json.dump(self.__convert__(), file)

    def load(self, plugin_manager, module=None):
        """Заполнить хранилища по информации из конфига.

        :param plugin_manager: PluginManager
        :param module: str, имя модуля (при None загружает в
        WidgetStorage.__widgets__ виджеты для всех модулей)
        """
        def save(arg):
            """Сохранить значения в словари.

            :param arg: value
            """
            self.widget_compliance.__uuids__ = arg[0]
            self.widget_compliance.__plugins__ = arg[1]
            self.widget_storage.__data__ = arg[2]
            self.widget_storage.__uuids__ = arg[3]

        if os.path.isfile(self._PATH_JSON):
            with open(self._PATH_JSON, 'r', encoding='utf-8') as file:
                value = json.load(file)
            if value:
                save(value)  # сохранение сырых данных
                save(self.__convert__(True))  # конвертация str-ов в UUID-ы
                for uuid, val in self.widget_compliance.__uuids__.items():
                    info = self.widget_storage.get_info(uuid)
                    if module and info[0] != module:
                        continue
                    widget = plugin_manager.get_plugin(val[0]).get_widget(
                        val[1])(uuid, *info + (self,))
                    self.widget_storage.__widgets__[uuid] = widget
