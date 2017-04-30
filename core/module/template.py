"""Шиблон модуля."""


class Module:
    """Шаблон модуля."""
    def __init__(self, name, manager, data_iface):
        """

        :param name: str, параметр name
        :param manager: ModuleManager
        :param data_iface: data_iface для сборки темы
        """
        self._NAME = name
        self._manager = manager
        self._data_iface = data_iface

    def make(self):
        """Полная сборка страницы на вывод.

        :return: str
        """
        return ''

    def get_cookies(self):
        """Получить Cookie для передачи клиенту.

        :return: tuple с Cookie
        """
        return ()

    def get_header(self):
        """Получить http заголовки, передаваемые клиенту.

        :return: tuple со строками
        """
        return 'Content-Type: text/html',

    def call(self, **kwargs):
        """Вызов модуля.

        :param kargs: dict с параметрами
        :return: опционально
        """
        pass
