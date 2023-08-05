
import platform
from rasp_util import auto_patch

def upload_danger(exception):
    if auto_patch.USE_SENTRY:
        import sentry_sdk
        sentry_sdk.capture_exception(exception)
    elif auto_patch.UPLOAD_FUNCTION:
        auto_patch.UPLOAD_FUNCTION(exception)
    else:
        import logging
        info = "{1}:{2}".format(exception.__class__.__name__,exception)
        logger.debug(info)
        print(info)
    


def system():
    """
    获取系统名称，方便命令执行 攻击 的判断
    :return: the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.
            An empty string is returned if the value cannot be determined.
    """
    return platform.system()
