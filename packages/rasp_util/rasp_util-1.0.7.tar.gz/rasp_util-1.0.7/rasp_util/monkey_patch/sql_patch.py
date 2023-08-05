import sys
from importlib.machinery import PathFinder, ModuleSpec, SourceFileLoader
from rasp_util.attack_rules import rules
from rasp_util.attack_rules.risk_level import *
from rasp_util.sentry import util
# import rules, util
# from risk_level import *


# --------------------sqll patch-----------------
def patcher(function):
    def wrapper(*args, **kwargs):
        sql_words = None
        if args is not None and len(args) >= 1:
            sql_words = args[0]
        # ---------------规则-------------------
        if sql_words:
            print("sql 语句： ", sql_words)
            level = rules.sql_levels_of_danger(sql_words)
            if level > 3:
                e = Block_Attack("SQL注入攻击：" + "异常sql " + sql_words)
                util.upload_danger(e)
                raise e
            elif level > 0:
                e = Suspect_Attack("SQL注入警告：" + "异常sql " + sql_words)

        return function(*args, **kwargs)

    return wrapper


class CursorProxy():
    def __init__(self, cursor):
        self.cursor = cursor
        self.execute = patcher(self.cursor.execute)

    def __getattr__(self, key):
        return getattr(self.cursor, key)


class ConnectionProxy():
    def __init__(self, connection):
        self.connection = connection

    def cursor(self, *args, **kwargs):
        real_cursor = self.connection.cursor(*args, **kwargs)
        return CursorProxy(real_cursor)


def patch_connect(real_connect):
    def connect(*args, **kwargs):
        real_connection = real_connect(*args, **kwargs)
        return ConnectionProxy(real_connection)

    return connect


class Finder(PathFinder):

    def __init__(self, module_name):
        self.module_name = module_name

    def find_spec(self, fullname, path=None, target=None):
        if fullname == self.module_name:
            spec = super().find_spec(fullname, path, target)
            loader = CustomLoader(fullname, spec.origin)
            return ModuleSpec(fullname, loader)


class CustomLoader(SourceFileLoader):

    def exec_module(self, module):
        super().exec_module(module)
        module.connect = patch_connect(module.connect)
        return module


def patch(findname='sqlite3.dbapi2'):
    """
    :param findname: 覆盖的sql 所导入相关的包
    :return:
    """
    sys.meta_path.insert(0, Finder(findname))
