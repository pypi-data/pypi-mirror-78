from importlib.machinery import SourceFileLoader
import sys
from rasp_util.monkey_patch.finder import *
from rasp_util.attack_rules.risk_level import *
from rasp_util.sentry import util
from rasp_util.attack_rules import rules
import re, urllib


def patcher(function):
    def wrapper(*args, **kwargs):
        self = args[0]

        res = function(*args, **kwargs)

        url_path = self.path
        if url_path:

            path, query = self.path.split('?', 1) if '?' in self.path else (self.path, "")
            if query is None:
                return res
            params = dict((match.group("parameter"),
                           urllib.parse.unquote(
                               ','.join(re.findall(r"(?:\A|[?&])%s=([^&]+)" % match.group("parameter"), query))))
                          for match in re.finditer(r"((\A|[?&])(?P<parameter>[\w\[\]]+)=)([^&]+)", query))
            print(params.values())
            for param in params.values():

                level = rules.input_of_danger(param)
                if level > 3:
                    # 替换为正常输入或者拦截输入？
                    # -------尚未拦截----保留------------
                    self.path = "/"
                    e = Block_Attack("SQL注入攻击：" + "用户异常输入" + param)
                    util.upload_danger(e)
                    raise e
                elif level > 0:
                    e = Suspect_Attack("SQL注入警告：" + "用户异常输入" + param)

        return res

    return wrapper


class HttpServerLoader(SourceFileLoader):

    def exec_module(self, module):
        super().exec_module(module)
        module.BaseHTTPRequestHandler.parse_request = patcher(module.BaseHTTPRequestHandler.parse_request)
        return module


def patch(name="http.server"):
    sys.meta_path.insert(0, Finder(name, HttpServerLoader))
