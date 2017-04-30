"""Модуль для работы с maker. См. документацию maker и widget_manager."""
_maker_iface = None
_widget_manager = None


def __init__(maker_iface, widget_manager):
    global _maker_iface, _widget_manager
    _maker_iface = maker_iface
    _widget_manager = widget_manager


def add(uuid, module, sidebar, pos, name, widget, plugin):
    _widget_manager.add(uuid, module, sidebar, pos, name, widget, plugin)


def set_data(title, keywords, description, content):
    _maker_iface.set_data(title, keywords, description, content)


def add_tag(page, tag, value):
    _maker_iface.add_tag(page, tag, value)


def add_tag_menu(menu, pos, sub_pos, tag, value):
    _maker_iface.add_tag_menu(menu, pos, sub_pos, tag, value)


def add_tag_widget(sidebar, pos, tag, value):
    _maker_iface.add_tag_widget(sidebar, pos, tag, value)


def add_menu_element(menu, pos, name, link, target):
    _maker_iface.add_menu_element(menu, pos, name, link, target)


def add_menu_sub_element(menu, pos, sub_pos, name, link, target):
    _maker_iface.add_menu_sub_element(menu, pos, sub_pos, name, link, target)


def add_widget(sidebar, pos, name, content):
    _maker_iface.add_widget(sidebar, pos, name, content)
