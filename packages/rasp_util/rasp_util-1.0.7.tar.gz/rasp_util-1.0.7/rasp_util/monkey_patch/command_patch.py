from rasp_util.attack_rules.risk_level import *
from rasp_util.attack_rules import rules
from rasp_util.sentry import util
from rasp_util.hook_func.hook_func import *
from rasp_util.hook_func.operate import *

# 暂未使用
class Operate_exec(Operate):
    def pre_hook(self, *args, **kwargs):
        return (args, kwargs)

    def post_hook(self, retval, *args, **kwargs):
        return retval


class Operate_shell(Operate):
    def pre_hook(self, *args, **kwargs):

        commmand = None
        if args is not None and len(args) >= 1:
            commmand = args[0]
        # ---------------规则-------------------
        if commmand:
            print("commmand : ", commmand)
            try:
                rules.command_injection(commmand)
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
    global exec
    exec = InstallFcnHook(exec, Operate_exec(), True)
    import subprocess, os
    subprocess.check_output = InstallFcnHook(subprocess.check_output, Operate_shell(), True)
    os.system = InstallFcnHook(os.system, Operate_shell(), True)


if __name__ == '__main__':
    # ------test--------------
    # patch()
    import subprocess, os, urllib.request

    os.system("ls;pwd;ifconfig")
    urllib.request.urlopen('http://152.136.235.152:9000/m3lon.txt')
