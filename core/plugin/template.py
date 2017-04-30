"""Шаблоны для плагинов."""
from enum import IntEnum


class Widget:
    """Шаблон для виджетов."""
    def __init__(self, uuid, module, sidebar, pos, name, widget_manager):
        """

        :param uuid: UUID виджета
        :param module: str, имя модуля
        :param sidebar: str, имя области для виджетов
        :param pos: позиция
        :param name: str, имя виджета
        :param widget_manager: WidgetManager
        """
        self.UUID = uuid
        self.MODULE = module
        self.SIDEBAR = sidebar
        self.POS = pos
        self.NAME = name
        self._widget_manager = widget_manager

    def load(self):
        """Событие загрузки виджета.

        :return: bool, True - загрузка одобрена, False - не загружать виджет
        """
        return True

    def get_name(self):
        """Получить имя виджета.

        :return: str
        """
        return self.NAME

    def get_content(self):
        """Получить содержимое виджета.

        :return: str (html)
        """
        pass

    def get_setting_content(self):
        """Получить содержимое для настроек виджета.

        :return: str (html)
        """
        pass

    def get_tags(self):
        """Получить теги для замены в сборщике тем.

        :return: iterable, tuple-капсулы (тег, замена),
        (('{tag}', 'content'), ...)
        """
        pass

    def remove(self):
        """Событие удаление виджета (должно вычищать данные)."""
        pass


class Priority(IntEnum):
    """Приоритет инициализации и вызова событий."""
    highest = 0
    high = 1
    middle = 2
    low = 3
    lowest = 4


class Plugin:
    """Шаблон для плагинов."""
    def __init__(self, field_storage, maker, manager):
        """

        :param field_storage: FieldStorage из cgi
        :param maker: maker, сборщик тем
        :param manager: PluginManager
        """
        self._field_storage = field_storage
        self._maker = maker
        self._manager = manager

    def load(self):
        """Событие загрузки плагина.

        :return: bool, True - загрузка одобрена, False - не загружать плагин
        """
        return True

    def unload(self):
        """Событие выгрузки плагина."""
        pass

    def pre_load_module(self, module, name):
        """Событие предзагрузки модуля.

        :param module: str, имя модуля
        :param name: str, параметр name для модуля
        :return: tuple, (str, str), (module, name)
        """
        return module, name

    def loaded_module(self, module):
        """Событие загрузки модуля.

        :param module: модуль
        """
        pass

    def exit_script(self):
        """Событие завершения скрипта."""
        pass

    def get_widgets_info(self):
        """Получить информацию о виджетах.

        :return: tuple, (заголовок, описание в html)
        """
        pass

    def get_widget(self, name):
        """Получить виджет.

        :param name: str, имя виджета
        :return: не инициализированный объект виджета
        """
        pass

    def get_admin_widgets_info(self):
        """Получить информацию о виджетах для админ панели.

        :return: tuple, (заголовок, описание в html)
        """
        pass

    def get_admin_widget(self, name):
        """Получить виджет для админ панели.

        :param name: str, имя виджета
        :return: не инициализированный объект виджета
        """
        pass

    def get_admin_menu(self):
        """Получить пункт меню для админ панели.

        :return: tuple, ((имя, ссылка), ...), первая пара - отображается
        в меню, остальное - свёрнутые подпункты
        """
        pass

    def pre_load(self, state, content):
        """Событие предзагрузки компонентов движка.

        :param state: bool (см. return)
        :param content: tuple (см. return)
        :return: tuple, (bool, str),
        bool - True одобряет загрузку, False отменяет;
        str - контент, который выводится в случае отмены загрузки
        """
        return True, ''

    def pre_print(self, page):
        """Событие предвывода страницы.

        :param page: str, контент на вывод
        :return: str на вывод (если не надо менять - page)
        """
        return page

    def set_data(self, title, keywords, description, content):
        """Событие установки основной информации.

        :param title: str, заголовок страницы
        :param keywords: str, ключевые слова
        :param description: str, описание
        :param content: str, основное содержимое
        :return: tuple, (title, keywords, description, content)
        """
        return True, title, keywords, description, content

    def add_tag(self, page, tag, value):
        """Событие добавления тега.

        :param page: str, имя страницы без расширения
        :param tag: str, имя тега без фигурных скобок
        :param value: str, значение
        :return: tuple, (page, tag, value)
        """
        return True, page, tag, value

    def add_tag_menu(self, menu, pos, sub_pos, tag, value):
        """Событие добавления тега меню.

        :param menu: str, имя меню
        :param pos: int, позиция родительского элемента
        :param sub_pos: int, позиция суб-элемента
        (None, если это основной элемент)
        :param tag: str, имя тега без фигурных скобок
        :param value: str, значение
        :return: tuple (menu, pos, sub_pos, tag, value)
        """
        return True, menu, pos, sub_pos, tag, value

    def add_tag_widget(self, sidebar, pos, tag, value):
        """Событие добавления тега виджета.

        :param sidebar: имя области для виджетов
        :param pos: int, позиция виджета
        :param tag: str, имя тега без фигурных скобок
        :param value: str, значение
        :return: tuple, (sidebar, pos, tag, value)
        """
        return True, sidebar, pos, tag, value

    def add_menu_element(self, menu, pos, name, link, target):
        """Событие добавления элемента меню.

        :param menu: str, имя меню
        :param pos: int, позиция элемента
        :param name: str, имя элемента
        :param link: str, ссылка
        :param target: str, значение параметра target у ссылки
        :return: tuple, (menu, pos, name, link, target)
        """
        return True, menu, pos, name, link, target

    def add_menu_sub_element(self, menu, pos, sub_pos, name, link, target):
        """Событие добавления субэлемента меню.

        :param menu: str, имя меню
        :param pos: int, позиция родительского элемента
        :param sub_pos: int, позиция элемента
        :param name: str, имя элемента
        :param link: str, ссылка
        :param target: str, значение параметра target у ссылки
        :return: tuple, (menu, pos, sub_pos, name, link, target)
        """
        return True, menu, pos, sub_pos, name, link, target

    def add_widget(self, sidebar, pos, name, content):
        """Событие добавления виджета.

        :param sidebar: str, имя области для виджетов
        :param pos: int, позиция виджета
        :param name: str, имя виджета
        :param content: str, содержимое виджета
        :return: tuple, (sidebar, pos, name, content)
        """
        return True, sidebar, pos, name, content

    def pre_make(self, result):
        """Событие предсборки темы.

        :param result: bool (см. return)
        :return: bool, True - инициализировать, False - нет
        (если плагин провёл инициализацию самостоятельно)
        """
        return True

    def make(self, page):
        """Событие сборки темы.

        :param page: str (см. return)
        :return: str,  страница на вывод (если не нужно заменять - page)
        """
        return page

    def get_cookies(self):
        """Получить Cookies плагина.

        :return: tuple с объектами Cookie из core.cookies
        """
        return ()

    def get_header(self):
        """Получить http заголовки, передаваемые клиенту.

        :return: tuple со строками
        """
        return ()

    def pre_send_cookies(self, cookies):
        """Предсохранение Cookies для последующей отправки клиенту.

        :param cookies: tuple c объектами Cookie из core.cookies
        :return: tuple c объектами Cookie из cookies
        (если не надо заменять - cookies)
        """
        return cookies

    def call(self, **kwargs):
        """Вызов плагина.

        :param kargs: dict с параметрами
        :return: опционально
        """
        pass

    def remove(self):
        """Событие удаления плагина (должнов вычищать данные)."""
        pass
