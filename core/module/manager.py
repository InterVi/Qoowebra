"""Управление модулями."""
import os
import sys
import core.module.data_iface as data_iface
from core.module.validator import is_valid


class ModuleManager:
    """Менеджер модулей."""
    def __init__(self, maker, maker_iface, event_manager, db, field_storage,
                 plugin_manager, widget_manager, domain):
        self.maker = maker
        self.maker_iface = maker_iface
        self.event_manager = event_manager
        self.db = db
        self.field_storage = field_storage
        self.plugin_manager = plugin_manager
        self.widget_manager = widget_manager
        self.DOMAIN = domain
        self.PATH = os.path.join(sys.path[0], 'modules')
        data_iface.__init__(maker_iface, widget_manager)

    def get_modules(self, valid=True):
        result = {}
        for d in os.listdir(self.PATH):
            file = os.path.join(self.PATH, d)
            if not os.path.isdir(file) or d == '__pycache__':
                continue
            if valid and not is_valid(file):
                continue
            pack = __import__(file)
            result[pack.NAME] = {
                'DESCRIPTION': pack.DESCRIPTION,
                'AUTHOR': pack.AUTHOR,
                'EMAIL': pack.EMAIL,
                'URL': pack.URL,
                'path': file,
                'module': pack.get_main()
            }
        return result

    @staticmethod
    def __get_from_path__(path):
        pack = __import__(path)
        return {
                'DESCRIPTION': pack.DESCRIPTION,
                'AUTHOR': pack.AUTHOR,
                'EMAIL': pack.EMAIL,
                'URL': pack.URL,
                'path': path,
                'module': pack.get_main()
            }

    def init_module(self, module, name):
        return module(name, self, data_iface)

    def get_module(self, module, name, valid=True):
        return self.init_module(self.get_modules(valid)[module][module], name)
