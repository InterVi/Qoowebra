"""Модуль с шаблонами для баз данных."""


class DB:
    """Шаблон для базы данных SQL."""
    def __init__(self, file=':memory:', timeout=5.0, host=None, port=None,
                 user=None, password=None, prefix=None):
        """

        :param file: str, имя файла
        :param timeout: число
        :param host: str, хост
        :param port: порт
        :param user: str, имя пользователя
        :param password: str, пароль
        :param prefix: str, префикс для таблиц БД
        """
        self._file = file
        self._timeout = timeout
        self._host = host
        self._post = port
        self._user = user
        self._password = password
        self.prefix = prefix

    def connect(self):
        """Подключение к БД.

        :return: True при успехе
        """
        return False

    def execute(self, command):
        """Выполнить команду.

        :param command: str, команда
        :return: результат
        """
        pass

    def execute_many(self, command, iterator):
        """Выполнить команду с подстановкой значений из итератора.

        :param command: str, команда
        :param iterator: итератор
        :return: результат
        """
        pass

    def execute_script(self, script):
        """Выполнить скрипт.

        :param script: str, скрипт
        :return: результат
        """
        pass

    def fetch_one(self):
        """Получить следующий ряд из результата запроса."""
        pass

    def fetch_many(self, size):
        """Получить следующую часть из результата запроса.

        :param size: число
        :return: результат
        """
        pass

    def fetch_all(self):
        """Получить весь результат запроса."""
        pass

    def commit(self):
        """Сохранить изменения в БД."""
        pass

    def rollback(self):
        """Откатить изменения в БД на один коммит назад."""
        pass

    def close(self):
        """Закрыть соединение."""
        pass
