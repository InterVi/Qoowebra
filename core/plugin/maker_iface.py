"""Прослойка между maker и event_manager."""
__event_manager = None
__maker = None


def __init__(event_manager, maker):
    """Инициализация модуля.

    :param event_manager: инициализированный модуль event_manager
    :param maker: инициализированный модуль maker
    """
    global __event_manager, __maker
    __event_manager = event_manager
    __maker = maker


def set_data(title, keywords, description, content):
    __maker.set_data(*__event_manager.set_data(title, keywords, description,
                                               content))


def add_tag(page, tag, value):
    __maker.add_tag(*__event_manager.add_tag(page, tag, value))


def add_tag_menu(menu, pos, sub_pos, tag, value):
    __maker.add_tag_menu(*__event_manager.add_tag_menu(menu, pos, sub_pos, tag,
                                                       value))


def add_tag_widget(sidebar, pos, tag, value):
    __maker.add_tag_widget(*__event_manager.add_tag_widget(sidebar, pos, tag,
                                                           value))


def add_menu_element(menu, pos, name, link, target):
    __maker.add_menu_element(*__event_manager.add_menu_element(menu, pos, name,
                                                               link, target))


def add_menu_sub_element(menu, pos, sub_pos, name, link, target):
    __maker.add_menu_sub_element(*__event_manager.add_menu_sub_element(menu,
                                                                       pos,
                                                                       sub_pos,
                                                                       name,
                                                                       link,
                                                                       target))


def add_widget(sidebar, pos, name, content):
    __maker.add_widget(*__event_manager.add_widget(sidebar, pos, name,
                                                   content))
