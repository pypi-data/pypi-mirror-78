from rasp_util.hook_func.operate import Operate
from rasp_util.attack_rules import  rules
from rasp_util.sentry import util
from rasp_util.hook_func.hook_func import InstallFcnHook
from rasp_util.attack_rules.risk_level import *


class Operate_open(Operate):
    def pre_hook(self, *args, **kwargs):

        file_path = args[0]
        # open("./rasp_util/util.py","rb")
        print("open : ", file_path)
        try:
            rules.file_injection(file_path)
        except Block_Attack as e:
            print("阻断", e.errorinfo)
            util.upload_danger(e)
            raise e
        except Suspect_Attack as e:
            print("可疑", e.errorinfo)
            util.upload_danger(e)

    def post_hook(self, retval, *args, **kwargs):

        return retval


def patch():
    import builtins
    import urllib.request
    builtins.open = InstallFcnHook(builtins.open, Operate_open())
    urllib.request.urlopen = InstallFcnHook(urllib.request.urlopen, Operate_open())


if __name__ == '__main__':
    # ------test--------------
    patch()
    content = open("../hook.py")
    open("dsvw.py")
    print(content.readline())
    # urllib.request.urlopen('http://152.136.235.152:9000/m3lon.txt')
