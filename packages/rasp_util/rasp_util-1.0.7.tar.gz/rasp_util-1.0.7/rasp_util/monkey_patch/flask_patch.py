from importlib.machinery import SourceFileLoader
import sys
from .finder import *


def patcher(function):
    def wrapper(*args, **kwargs):
        print("---------flask拦截")
        return function(*args, **kwargs)

    return wrapper


class FlaskLoader(SourceFileLoader):

    def exec_module(self, module):
        super().exec_module(module)
        module.Flask.wsgi_app = patcher(module.Flask.wsgi_app)
        return module


def patch(name="flask.app"):
    sys.meta_path.insert(0, Finder(name, FlaskLoader))
