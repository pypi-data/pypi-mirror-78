"""
hook 前后执行的操作代码 先用继承，后期考虑 使用 lambda表达式
"""


class Operate:

    def pre_hook(self, *args, **kwargs):
        '''
        函数执行前 操作 ， 考虑可以过滤参数
        :param args:
        :param kwargs:
        :return:
        '''
        return (args, kwargs)

    def post_hook(self, retval, *args, **kwargs):
        '''
        函数执行后操作，  考虑可以拦截一些攻击返回的敏感的结果
        :param retval:
        :param args:
        :param kwargs:
        :return:
        '''
        return retval
