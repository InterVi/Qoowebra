"""Модуль для сборки шаблона. Файлы шаблона и конфиг должны быть
в кодировке utf-8."""
import os
import json
from configparser import ConfigParser


__conf = {}
"""конфиг подтемы"""

# =================================================== константы

PATH_HTML = None
"""полный путь к директории с подтемой в директории html"""
THEME = None
"""имя подтемы"""
PATH = None
"""полный путь к теме"""

# =================================================== основные значения

_title = ''
"""заголовок для тега title"""
_keywords = ''
"""содержимое для мета-тега keywords"""
_description = ''
"""содержимое для мета-тега description"""
_content = ''
"""основное содержимое страницы"""

# =================================================== теги

__tags = {}
"""Теги для замены в шаблоне.

{page: {tag: value}}
"""
__tags_menus = {}
"""Теги для замены в элементах меню.

{menu: {pos: {None: {tag: value}, pos: {tag: value}}}}
"""
__tags_widgets = {}
"""Теги для замены в виджетах.

{sidebar: {pos: {tag: value}}}
"""

# =================================================== элементы

__menus = {}
"""Элементы меню.

{menu: {pos: ((element, link, target), {pos: (name, link, target)})}}
"""
__widgets = {}
"""Виджеты.

{sidebar: {pos: (name, content)}}
"""

# =================================================== шаблоны

__html = {}
"""Основа шаблона.

{страница: контент (str)}
"""
__html_menus = {}
"""Шаблоны меню.

{страница: контент (str)}
"""
__html_widgets = {}
"""Шаблоны виджетов.

{страница: контент (str)}
"""


def _clear():
    """Очистка данных для повторной инициализации модуля."""
    global __conf, PATH_HTML, THEME, _title, _keywords, _description
    global _content, __tags, __tags_menus, __tags_widgets, __menus, __widgets
    global __html, __html_menus, __html_widgets
    __conf = {}
    __tags = {}
    __tags_menus = {}
    __tags_widgets = {}
    __menus = {}
    __widgets = {}
    __html = {}
    __html_menus = {}
    __html_widgets = {}
    PATH_HTML = None
    THEME = None
    _title, _keywords, _description, _content = ('', '', '', '')


# =================================================== добавление


def set_data(title, keywords, description, content):
    """Установить значения главных тегов."""
    global _title, _keywords, _description, _content
    _title = title
    _keywords = keywords
    _description = description
    _content = content


# ======================= теги


def add_tag(page, tag, value):
    """Добавить тег для замены в общем шаблоне.

    :param page: str, имя страницы без расширения
    :param tag: str, имя тега без фигурных скобок
    :param value: str, значение
    """
    global __tags
    if not page or not tag:
        return
    if page in __tags:
        __tags[page][tag] = value
    else:
        __tags[page] = {tag: value}


def __add_tag(dict_, key1, key2, key3, value):
    """Добавить тег вглубь словаря.

    :param dict_: ссылка на dict
    """
    if key1 in dict_:
        if key2 in dict_[key1]:
            dict_[key1][key2][key3] = value
        else:
            dict_[key1][key2] = {key3: value}
    else:
        dict_[key1] = {key2: {key3: value}}


def add_tag_menu(menu, pos, sub_pos, tag, value):
    """Добавить тег для замены в элементах меню.

    :param menu: str, имя меню
    :param pos: int, позиция родительского элемента
    :param sub_pos: int, позиция суб-элемента (None, если это основной элемент)
    :param tag: str, имя тега без фигурных скобок
    :param value: str, значение
    """
    global __tags_menus
    if not menu or not tag:
        return
    if menu in __tags_menus:
        __add_tag(__tags_menus[menu], pos, sub_pos, tag, value)
    else:
        __tags_menus[menu] = {pos: {sub_pos: {tag: value}}}


def add_tag_widget(sidebar, pos, tag, value):
    """Добавить тег для замены в виджетах.

    :param sidebar: имя области для виджетов
    :param pos: int, позиция виджета
    :param tag: str, имя тега без фигурных скобок
    :param value: str, значение
    """
    global __tags_widgets
    if not sidebar or not tag:
        return
    __add_tag(__tags_widgets, sidebar, pos, tag, value)


# ======================= элементы


def add_menu_element(menu, pos, name, link, target):
    """Добавить элемент меню.

    :param menu: str, имя меню
    :param pos: int, позиция элемента
    :param name: str, имя элемента
    :param link: str, ссылка
    :param target: str, значение параметра target у ссылки
    """
    global __menus
    if not menu or not name or not link:
        return
    if menu in __menus:
        if pos in __menus[menu]:
            mmp = __menus[menu][pos]
            __menus[menu][pos] = ((name, link, target), mmp[1])
        else:
            __menus[menu][pos] = ((name, link, target), {})
    else:
        __menus[menu] = {pos: ((name, link, target), {})}


def add_menu_sub_element(menu, pos, sub_pos, name, link, target):
    """Добавить субэлемент меню.

    :param menu: str, имя меню
    :param pos: int, позиция родительского элемента
    :param sub_pos: int, позиция элемента
    :param name: str, имя элемента
    :param link: str, ссылка
    :param target: str, значение параметра target у ссылки
    """
    global __menus
    if not menu or not name or not link:
        return
    if menu in __menus:
        if pos in __menus[menu]:
            mmp = __menus[menu][pos]
            mmp[1][sub_pos] = (name, link, target)
            __menus[menu][pos] = (mmp[0], mmp[1])
        else:
            __menus[menu][pos] = ((), {sub_pos: (name, link, target)})
    else:
        __menus[menu] = {pos: ((), {sub_pos: (name, link, target)})}


def add_widget(sidebar, pos, name, content):
    """Добавить виджет.

    :param sidebar: str, имя области для виджетов
    :param pos: int, позиция виджета
    :param name: str, имя виджета
    :param content: str, содержимое виджета
    """
    global __widgets
    if not sidebar or not name:
        return
    if sidebar in __widgets:
        __widgets[sidebar][pos] = (name, content)
    else:
        __widgets[sidebar] = {pos: (name, content)}


# =================================================== инициализация модуля


def __load_config(path):
    """Загрузка конфига.

    :param path: str, путь к конфигу
    """
    global __conf
    parser = ConfigParser()
    parser.read(path, 'utf-8')  # чтение
    for section in parser.sections():
        __conf[section] = {}
        for key, val in parser.items(section):
            if section == 'FILES' or section == 'VARS':  # в этой секции json
                __conf[section][key] = json.loads(val)
            elif section == 'MAIN':
                if key in ('setting', 'sidebars', 'menus'):  # json
                    __conf[section][key] = json.loads(val)
                else:
                    __conf[section][key] = val
            else:
                __conf[section][key] = val


def get_config():
    """Получить копию конфига.

    :return: dict
    """
    return __conf.copy()


def get_theme():
    """Получить подтему.

    :return: tuple, (dict, dict, dict), (основной шаблон, меню, виджеты),
    ключи словарей - имена страниц без расширения,
    значения - содержимое страниц
    """
    path_menus = os.path.join(PATH_HTML, 'menus')
    path_widgets = os.path.join(PATH_HTML, 'widgets')

    def get_html(path):
        """Получить шаблон.

        :param path: str, путь к папке с шаблоном
        :return: dict, ключи - имена страниц, значения - содержимое страниц
        """
        result = {}
        for file in os.listdir(path):
            path_file = os.path.join(path, file)
            if not os.path.isfile(path_file) or file[-5:] != '.html':
                continue
            with open(path_file, encoding='utf-8') as page:
                result[file[:-5]] = page.read().strip()
        return result

    main = get_html(PATH_HTML)
    menus = {}
    widgets = {}
    if os.path.isdir(path_menus):  # если есть шаблоны меню
        menus = get_html(path_menus)
    if os.path.isdir(path_widgets):  # если есть шаблоны виджетов
        widgets = get_html(path_widgets)
    return main, menus, widgets


def __init__(path, theme, conf=None):
    """Инициализация модуля.

    :param path: полный путь к директории с темой
    :param theme: имя подтемы
    :param conf: dict, конфиг подтемы
    """
    global PATH_HTML, THEME, PATH, __conf
    PATH_HTML = os.path.join(path, 'html', theme)
    THEME = theme
    PATH = path
    if conf:
        __conf = conf.copy()
    else:
        __load_config(os.path.join(path, 'conf', theme + '.conf'))


def set_theme(main, menus, widgets):
    """Установка подтемы.

    :param main: dict, главный шаблон
    :param menus: dict, шаблоны меню
    :param widgets: dict, шаблоны виджетов
    """
    global __html, __html_menus, __html_widgets
    if main:
        __html = main.copy()
    if menus:
        __html_menus = menus.copy()
    if widgets:
        __html_widgets = widgets.copy()


def load_theme():
    """Загрузить и установить подтему."""
    set_theme(*get_theme())


# =================================================== утилиты


def replace(line, values):
    """Массовая замена в строке.

    :param line: str
    :param values: list или tuple, [(что заменять, на что заменять), ...]
    :return: str, обработанная строка
    """
    for val in values:
        line = line.replace(*val)
    return line


def get_replace(tags, dict_tags=(), no_empty=False):
    """Получить значение для replace из словаря.

    :param tags: list, tuple или dict, полный список тегов без фигурных скобок
    :param dict_tags: dict, ключи - теги (должны быть в tags),
    значения - замена
    :param no_empty: bool, True - не заменять теги пустотой,
    если их нет в dict_tags
    :return: list, [(тег, замена), ...], значение для replace
    (с подставленными фигурными скобками у тегов)
    """
    result = []
    for tag in tags:
        to = ''
        if tag in dict_tags:
            to = dict_tags[tag]
        elif no_empty:
            continue
        result.append(('{' + tag + '}', to))
    return result


def get_page_name(tag, menu=True):
    """Получить страницу с тегом меню или области для виджетов.

    :param tag: str, имя тега без фигурных скобок
    :param menu: bool, True - искать среди меню,
    False - среди областей для виджетов
    :return: имя файла или None
    """
    if menu:
        d = __conf['MAIN']['menus']
    else:
        d = __conf['MAIN']['sidebars']
    for file in d:
        if tag in __conf['FILES'][file]:
            return file


def get_menus_and_sidebars(page):
    """Получить имена тегов меню и областей для виджетов, которые используются
    на этой странице.

    :param page: str, имя страницы
    :return: tuple, (list, list), (теги меню, теги областей для виджетов)
    """
    menus = []
    sidebars = []
    cf = __conf['FILES']
    cs = __conf['SIDEBARS']
    cm = __conf['MENUS']
    if page in cf:
        for tag in cf[page]:
            if tag in cm:
                menus.append(tag)
            elif tag in cs:
                sidebars.append(tag)
    return menus, sidebars


# =================================================== сборка


def make_menu_element(menu, pos, no_empty=False):
    """Собрать элемент меню.

    :param menu: str, имя меню
    :param pos: int, позиция элемента
    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, шаблон с подставленными значениями
    """
    val_menu = __conf['MENUS'][menu]  # имя шаблона меню
    li_name = val_menu + '_li'  # имя шаблона меню для элементов списков
    template = __html_menus[val_menu]  # шаблон меню
    template_ul = __html_menus[val_menu + '_ul']
    template_li = __html_menus[li_name]
    m = __menus[menu]  # сокращения для удобства
    mp = m[pos]  # __menus[menu][pos]
    mpz = mp[0]  # __menus[menu][pos][0]
    rep = [  # замена в главном шаблоне
        ('{menu_link}', mpz[1]),
        ('{menu_target}', mpz[2]),
        ('{menu_text}', mpz[0])
    ]
    cf = __conf['FILES']
    if menu in cf:  # обработка тегов
        if menu in __tags_menus and pos in __tags_menus[menu]\
                and None in __tags_menus[menu][pos]:
            rep += get_replace(cf[menu], __tags_menus[menu][pos][None],
                               no_empty)
        else:  # нет замены - заменяем пустотой
            rep += get_replace(cf[menu], no_empty=no_empty)
    li = ''  # элементы списка (суб-элементы)
    mpk = list(mp[1].keys())  # __menus[menu][pos][1].keys() -> list
    mpk.sort()
    for sub_pos in mpk:  # обработка суб-элементов
        val = mp[1][sub_pos]  # __menus[menu][pos][1][sub_pos]
        rep_li = [  # замена в элементе
            ('{menu_link}', val[1]),
            ('{menu_target}', val[2]),
            ('{menu_text}', val[0])
        ]
        if li_name in cf:  # обработка тегов
            if menu in __tags_menus and pos in __tags_menus[menu]\
                    and sub_pos in __tags_menus[menu][pos]:
                rep_li += get_replace(cf[li_name],
                                      __tags_menus[menu][pos][sub_pos],
                                      no_empty)
            else:  # нет замены - заменяем пустотой
                rep_li += get_replace(cf[li_name], no_empty=no_empty)
        li += (replace(template_li, rep_li)) + '\n'
    rep.append(('{ul}', template_ul.replace('{li}', li.strip())))
    return replace(template, rep)


def make_menu(name, no_empty=False):
    """Собрать меню.

    :param name: str, имя меню
    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, содержимое меню
    """
    result = ''
    if name in __menus:
        mnk = list(__menus[name].keys())
        mnk.sort()
        for pos in mnk:
            result += make_menu_element(name, pos, no_empty) + '\n'
    return result.strip()


def make_widget(sidebar, pos, no_empty=False):
    """Собрать виджет.

    :param sidebar: str, имя области для виджетов
    :param pos: int, позиция виджета
    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, содержимое виджета
    """
    page = __conf['SIDEBARS'][sidebar]  # имя страницы шаблона виджета
    template = __html_widgets[page]  # шаблон виджета
    cf = __conf['FILES']
    rep = [
        ('{widget_name}', __widgets[sidebar][pos][0]),
        ('{widget_content}', __widgets[sidebar][pos][1])
    ]
    if page in cf:
        if sidebar in __tags_widgets and pos in __tags_widgets[sidebar]:
            rep += get_replace(cf[page], __tags_widgets[sidebar][pos],
                               no_empty)
        else:  # нет замены - заменяем пустотой
            rep += get_replace(cf[page], no_empty=no_empty)
    return replace(template, rep)


def make_sidebar(name, no_empty=False):
    """Собрать область виджетов.

    :param name: str, имя области для виджетов
    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, содержимое области виджетов
    """
    result = ''
    if name in __widgets:
        wnk = list(__widgets[name].keys())
        wnk.sort()
        for pos in wnk:
            result += make_widget(name, pos, no_empty) + '\n'
    return result.strip()


def make_page(name, tags=(), no_empty=False):
    """Собрать страницу.

    :param name: str, имя страницы
    :param tags: dict, теги для замены, {тег: замена}
    (имена без фигурных скобок)
    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, содержимое страницы
    """
    template = __html[name]
    cf = __conf['FILES']
    rep = []
    if name in cf:
        cfn = cf[name].copy()
        for tag in tags:  # удаление тегов, которые будут заменены после
            if tag in cfn:
                cfn.remove(tag)
        if name in __tags:
            rep += get_replace(cfn, __tags[name], no_empty)
        else:  # нет замены - заменяем пустотой
            rep += get_replace(cfn, no_empty=no_empty)
    for tag in tags:  # механизм обработки спец. тегов, не добавляемых в __tags
        rep.append(('{' + tag + '}', tags[tag]))
    return replace(template, rep)


def make_pages(no_empty=False):
    """Собрать все страницы, кроме главной.

    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: dict, {имя: содержимое} (имена без расширений)
    """
    result = {}
    cm = __conf['MAIN']
    index = __conf['MAIN']['index']
    for page in __html:  # обработка страниц
        if page == index:
            continue
        d = {}
        menus, sidebars = get_menus_and_sidebars(page)
        for menu in menus:  # сборка меню
            d[menu] = make_menu(menu, no_empty)
        for sid in sidebars:  # сборка областей для виджетов
            d[sid] = make_sidebar(sid, no_empty)
        if page == cm['title']:  # заполнение спец. тегов
            d['title'] = _title
        if page == cm['keywords']:
            d['keywords'] = _keywords
        if page == cm['description']:
            d['description'] = _description
        if page == cm['content']:
            d['content'] = _content
        result[page] = make_page(page, d, no_empty)  # сборка страницы
    return result


def make_index(no_empty=False):
    """Собрать всю подтему.

    :param no_empty: bool, True - не заменять пустотой теги без значения
    :return: str, полная страница
    """
    pages = make_pages(no_empty)
    return replace(__html[__conf['MAIN']['index']], get_replace(pages.keys(),
                                                                pages,
                                                                no_empty))
