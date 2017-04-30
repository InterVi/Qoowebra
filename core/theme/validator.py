"""Модуль для проверки корректности тем."""
import os
import json
from enum import IntEnum
from configparser import ConfigParser

log = []
"""Лог сообщений об ошибках."""


class _CheckResult(IntEnum):
    """Результат проверки в _check_value."""
    ok = 0
    not_key = 1
    not_value = 2


def _check_value(key, section):
    """Проверить ключ в секции.

    :param key: str, ключ
    :param section: str, секция
    :return: _CheckResult
    """
    if key in section:
        if not section[key] or section[key].isspace():
            return _CheckResult.not_value
    else:
        return _CheckResult.not_key
    return _CheckResult.ok


def check_main_conf(path):
    """Проверить главный конфиг темы.

    :param path: str, путь к конфигу
    :return: bool, True - ошибок нет
    """
    parser = ConfigParser()
    parser.read(path, 'utf-8')
    if 'INFO' in parser:
        result = True
        info = parser['INFO']
        for key in ('default', 'name', 'author', 'description'):
            cv = _check_value(key, info)
            if cv == _CheckResult.not_key:
                result = False
                log.append('no key ' + key + ' in ' + path)
            elif cv == _CheckResult.not_value:
                result = False
                log.append('no value in key ' + key + ' in ' + path)
        return result
    else:
        log.append('no INFO in ' + path)
        return False


def check_conf(path):
    """Проверить конфиг подтемы.

    :param path: str, путь к конфигу
    :return: bool, True - ошибок нет
    """
    parser = ConfigParser()
    parser.read(path, 'utf-8')
    result = True

    def check(sec_key, sec):
        """Проверки для parser['MAIN"]['sidebars'] и parser['MAIN']['menus'].

        :param sec_key: str, sidebars или menus
        :param sec: str, SIDEBARS или MENUS
        """
        nonlocal result
        j = ()
        try:
            j = json.loads(parser['MAIN'][sec_key])
        except ValueError:
            result = False
            log.append('broken json ' + sec_key + ' in MAIN in ' + path)
        if 'FILES' in parser:
            p_f = parser['FILES']
            for s in j:
                if s in p_f:
                    j2 = ()
                    try:
                        j2 = json.loads(p_f[s])
                    except ValueError:
                        result = False
                        log.append('broken json ' + s + ' in FILES in ' + path)
                    if sec in parser:
                        p_s = parser[sec]
                        f = False
                        for v in j2:
                            if v in p_s:
                                f = True
                                break
                        if not f:
                            result = False
                            log.append('not found ' + s + ' in ' + sec + ' in '
                                       + path)
                    else:
                        result = False
                        log.append('not ' + sec + ' in ' + path)
                else:
                    result = False
                    log.append('not ' + s + ' in FILES in ' + path)
        else:
            result = False
            log.append('not FILES in ' + path)

    def check2(sec):
        """Проверки лимитов WIDGET_LIMITS или MENU_LIMITS.

        :param sec: str, WIDGET_LIMITS или MENU_LIMITS
        """
        nonlocal result
        for v in parser[sec]:
            if not parser[sec][v].isdigit():
                result = False
                log.append('not digit ' + v + ' in ' + sec + ' in ' + path)

    if 'INFO' in parser:
        for key in ('name', 'description', 'module', 'plugin', 'select'):
            cv = _check_value(key, parser['INFO'])
            if cv == _CheckResult.not_key:
                result = False
                log.append(key + ' not in INFO in ' + path)
            elif cv == _CheckResult.not_value:
                result = False
                log.append('empty value in ' + key + ' in INFO in ' + path)
            elif key == 'select':
                pis = parser['INFO']['select']
                if pis != 'yes' and pis != 'no':
                    result = False
                    log.append('broken value select in INFO in ' + path)
        if 'screenshot' in parser['INFO']:
            pis = parser['INFO']['screenshot']
            if not pis or pis.isspace():
                result = False
                log.append('empty value screenshot in INFO in ' + path)
    else:
        result = False
        log.append('INFO not in ' + path)
    if 'MAIN' in parser:
        for key in ('title', 'keywords', 'description', 'content', 'index',
                    'setting', 'sidebars', 'menus'):
            cv = _check_value(key, parser['MAIN'])
            if cv == _CheckResult.not_key:
                result = False
                log.append(key + ' not in MAIN in ' + path)
            elif cv == _CheckResult.not_value:
                result = False
                log.append('not value in ' + key + ' in MAIN in ' + path)
            elif key == 'setting':
                setting = ()
                try:
                    setting = json.loads(parser['MAIN']['setting'])
                except ValueError:
                    result = False
                    log.append('broken json setting in MAIN in ' + path)
                if 'VARS' in parser:
                    pv = parser['VARS']
                    for var in setting:
                        if var not in pv:
                            result = False
                            log.append(var + ' not in VARS in ' + path)
                        elif not pv[var] or pv[var].isspace():
                            result = False
                            log.append('empty value ' + var + ' in VARS in ' +
                                       path)
                else:
                    result = False
                    log.append('VARS not in ' + path)
            elif key == 'sidebars':
                check(key, 'SIDEBARS')
            elif key == 'menus':
                check(key, 'MENUS')
    else:
        result = False
        log.append('MAIN not in ' + path)
    if 'FILES' in parser:
        nv = False
        pf = parser['FILES']
        for key in pf:
            val = ()
            try:
                val = json.loads(pf[key])
            except ValueError:
                result = False
                log.append('broken json ' + key + ' in FILES in ' + path)
            for e in val:
                if 'SIDEBARS' in parser and e in parser['SIDEBARS']:
                    continue
                elif 'MENUS' in parser and e in parser['MENUS']:
                    continue
                if 'VARS' in parser:
                    if e not in parser['VARS']:
                        result = False
                        log.append('not found ' + e + ' in ' + key +
                                   ' in FILES in VARS in ' + path)
                elif not nv:
                    result = False
                    log.append('not VARS in ' + path)
                    nv = True
    if 'VARS' in parser:
        for var in parser['VARS']:
            try:
                val = json.loads(parser['VARS'][var])
            except ValueError:
                result = False
                log.append('broken json ' + var + ' in VARS in ' + path)
                continue
            if 'TYPE' in val:
                if val['TYPE'] == 'SELECT' and 'DEFAULT' not in val:
                    result = False
                    log.append('not DEFAULT in ' + var + ' in VARS in ' +
                               path)
                elif val['TYPE'] in ('USER_PATH', 'TEXT', 'TEXT_HTML',
                                     'URL_USER_PATH', 'COLOR'):
                    if 'CONTENT' in val and val['CONTENT'] != '{content}':
                        result = False
                        log.append('broken value CONTENT in ' + var +
                                   ' in VARS in ' + path)
            else:
                result = False
                log.append('not TYPE in ' + var + ' in VARS in ' + path)
            if 'CONTENT' not in val:
                result = False
                log.append('not CONTENT in ' + var + ' in VARS in ' + path)
    if 'MENU_LIMITS' in parser:
        check2('MENU_LIMITS')
    if 'WIDGET_LIMITS' in parser:
        check2('WIDGET_LIMITS')
    return result


def check_configs(path):
    """Проверить конфиги подтем.

    :param path: str, путь к папке с конфигами
    :return: bool, True - ошибок нет
    """
    files = os.listdir(path)
    result = True
    for file in files:
        path_file = os.path.join(path, file)
        if not os.path.isfile(path_file) or file[-5:] != '.conf':
            continue
        if not check_conf(path_file):
            result = False
    return result


def check_all(path):
    """Проверить тему.

    :param path: str, путь к теме
    :return: bool, True - ошибок нет
    """
    configs = os.path.join(path, 'conf')
    main = os.path.join(path, 'theme.conf')
    result = True
    if os.path.isdir(configs):
        if not check_configs(configs):
            result = False
    else:
        result = False
        log.append('not dir ' + configs)
    if os.path.isfile(main):
        if not check_main_conf(main):
            result = False
    else:
        result = False
        log.append('not config ' + main)
    return result
