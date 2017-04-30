"""Модуль для работы с Cookie на отправку."""
from datetime import datetime, timezone


class Cookie:
    """Класс для создания Cookie."""
    def __init__(self, values=None, expires=None, path=None, domain=None,
                 max_age=None, comment=None, comment_url=None, discard=False,
                 port=None, secure=False, httponly=False):
        self._values = {}
        if values and type(values) == dict:
            self._values = values
        self._expires = expires
        self._path = path
        self._domain = domain
        self._max_age = max_age
        self._comment = comment
        self._comment_url = comment_url
        self._discard = discard
        self._port = port
        self._secure = secure
        self._httponly = httponly

    def add(self, name, value):
        """Добавить переменную.

        :param name: str, имя
        :param value: str, содержимое
        """
        self._values[name.strip()] = value.strip()

    def set_expires(self, year, month, day, hour=0, minute=0, second=0,
                    microsecond=0):
        """Установить срок годности печеньки.

        описание параметров в datetime.datetime
        """
        dt = datetime(year, month, day, hour, minute, second, microsecond,
                      timezone.utc)
        self._expires = dt.strftime('%A, %d-%m-%Y %H:%M:%S UTC')

    def set_path(self, path):
        """Установить путь.

        :param path: str
        """
        self._path = path.strip()

    def set_domain(self, domain):
        """Установить домен.

        :param domain: str
        """
        self._domain = domain.strip()

    def set_max_age(self, seconds):
        """Установить срок годноти печеньки.

        :param seconds: str только из цифр (секунды)
        """
        self._max_age = seconds.strip()

    def set_comment(self, comment):
        """Установить комментарий.

        :param comment: str
        """
        self._comment = comment.strip()

    def set_comment_url(self, url):
        """Установить ссылку на комментарий.

        :param url: str
        """
        self._comment_url = url.strip()

    def set_discard(self, discard):
        """Сделать печеньку одноразовой.

        :param discard: bool
        """
        self._discard = discard

    def set_port(self, port):
        """Установить порт.

        :param port: str только из цифр
        """
        self._port = port.strip()

    def set_secure(self, secure):
        """Установить печеньку только для HTTPS.

        :param secure: bool
        """
        self._secure = secure

    def set_httponly(self, httponly):
        """Сделать печеньку доступной только по http.

        :param httponly: bool
        """
        self._httponly = httponly

    def get(self):
        """Получить готовую строку с печенькой для последующей передачи.

        :return: str
        """
        result = ''
        if self._values:
            for key, value in self._values.items():
                result += key + '=' + value + '; '
        if self._expires:
            result += 'Expires=' + self._expires + '; '
        if self._path:
            result += 'Path=' + self._path + '; '
        if self._domain:
            result += 'Domain=' + self._domain + '; '
        if self._max_age:
            result += 'Max-Age=' + self._max_age + '; '
        if self._comment:
            result += 'Comment=' + self._comment + '; '
        if self._comment_url:
            result += 'CommentURL=' + self._comment_url + '; '
        if self._port:
            result += 'Port=' + self._port + '; '
        if self._discard:
            result += 'Discard; '
        if self._secure:
            result += 'Secure; '
        if self._httponly:
            result += 'HttpOnly; '
        result += 'Version=1'
        if self._comment_url or self._port or self._discard:
            return 'Set-Cookie2: ' + result
        else:
            return 'Set-Cookie: ' + result


def get_all(cookies):
    """Собрать все печеньки в одну строку.

    :param cookies: список с Cookie
    :return: str
    """
    result = ''
    for c in cookies:
        result += c.get() + '\n'
    return result.strip()
