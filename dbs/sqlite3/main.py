"""База данных на sqlite3 из стандартной библиотеки."""
import os
import sys
import sqlite3
from core.db.template import DB


class Main(DB):
    _connect = None
    _cursor = None

    def connect(self):
        file = self._file
        if file != ':memory:':
            file = os.path.join(sys.path[0], 'dbs', 'sqlite3', 'dbs',
                                file + '.db')
        self._connect = sqlite3.connect(file, self._timeout)
        self._cursor = self._connect.cursor()
        return True

    def execute(self, command):
        return self._cursor.execute(command)

    def execute_many(self, command, iterator):
        return self._cursor.executemany(command, iterator)

    def execute_script(self, script):
        return self._cursor.executescript(script)

    def fetch_one(self):
        return self._cursor.fetchone()

    def fetch_many(self, size=None):
        if not size:
            size = self._cursor.arraysize
        return self._cursor.fetchmany(size)

    def fetch_all(self):
        return self._cursor.fetchall()

    def commit(self):
        self._connect.commit()

    def rollback(self):
        self._connect.rollback()

    def close(self):
        self._cursor.close()
        self._connect.close()
