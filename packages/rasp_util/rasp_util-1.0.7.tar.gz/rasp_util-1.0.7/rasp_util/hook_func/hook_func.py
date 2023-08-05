"""
针对函数的hook 的类
"""
from .operate import Operate

class InstallFcnHook(object):
    def __init__(self, fcn, execute: Operate, debug=False):
        self.debug = debug
        self._fcn = fcn
        self.execute = execute

    def __call__(self, *args, **kwargs):
        # print(args)
        # print(kwargs)
        _hook_args = args
        _hook_kwargs = kwargs
        # (_hook_args, _hook_kwargs) = self.execute.pre_hook(*args, **kwargs)
        #  self.execute.pre_hook(*args, **kwargs)
        #  retval = self._fcn(*_hook_args, **_hook_kwargs)
        #
        #  retval = self.execute.post_hook(retval, *_hook_args, **_hook_kwargs)
        try:
            self.execute.pre_hook(*args, **kwargs)
        except:
            # print("存在异常")
            block_file=open("hook_content.txt", "wb")
            block_file.write("存在攻击行为，访问失败！".encode("utf-8"))
            block_file.close()
            if self.debug:
                return open("hook_content.txt", "rb").read()
            else:
                return open("hook_content.txt", "rb")

        else:
            return self._fcn(*_hook_args, **_hook_kwargs)
        # if self.execute.pre_hook(*args,**kwargs):
        #     return self._fcn(*_hook_args, **_hook_kwargs)
        # else:
        #     return open("hook_content.txt", "rb")

# if __name__ =="__main__":
#     print(open("hook_content.txt", "rb").read())