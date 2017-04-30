"""Главный модуль, через который проходят все вызовы."""
import time
time_start = time.time()
import os
import cgi
import cgitb
import cProfile
import core.core as core
from core.cookies import get_all


def get_file(path):
    """Получить путь к несуществующему файлу с цифрой на конце. Применяется
    для создания логов.

    :param path: str, путь к файлу (без цифры)
    :return: str
    """
    i = 1
    while os.path.isfile(path):
        if i == 1:
            path += '.1'
        else:
            path = path[:-2] + '.' + str(i)
        i += 1
    return path


if __name__ == '__main__':
    core.__init__()  # инициализация модуля
    str_time = time.strftime('%b %Y %H:%M:%S', time.localtime())
    profile = cProfile.Profile()
    if core.config['MAIN']['cgitb'] == 'yes':  # включить вывод ошибок
        if core.config['MAIN']['tolog'] == 'yes':  # вывод в лог
            cgitb.enable(0, get_file(os.path.join(core.PATH_CGITB, str_time
                                                  + 'log')))
        else:
            cgitb.enable()
    if core.config['MAIN']['profile'] == 'yes':  # включить профилирование
        profile.enable()
    header, content, cookies = core.run(cgi.FieldStorage())  # получение данных
    # вывод заголовка
    for line in header:
        print(line)
    print(get_all(cookies))  # вывод куков (относятся к заголовку)
    print('\n')
    print(content)  # вывод содержимого
    if core.config['MAIN']['print_time'] == 'yes':  # вывод времени генерации
        print('<!-- Page generated for: ' + str(time.time() - time_start)
              + 's -->')
    if core.config['MAIN']['profile'] == 'yes':  # сохранение профиля
        profile.disable()
        profile.dump_stats(get_file(os.path.join(core.PATH_PROFILE, str_time
                                                 + 'log')))
