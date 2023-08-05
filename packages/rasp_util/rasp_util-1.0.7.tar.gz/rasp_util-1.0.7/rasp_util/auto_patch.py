"""
整合所有agent,此文件应该用户程序启动之前执行
"""
import os

# 参数 'path' 可以换成任意存在的环境变量名
# 如果不存在，则输出None

USE_SENTRY = True
UPLOAD_FUNCTION = None

def patch(sentry_dsn=None,upload_func=None,log_file_path=None,log_format=None):
    if sentry_dsn is None:
        sentry_dsn = os.environ.get('sentry_dsn')
    else:
        print(sentry_dsn)
    if sentry_dsn is None:

        global USE_SENTRY,UPLOAD_FUNCTION
        USE_SENTRY = False
        if upload_func:
            UPLOAD_FUNCTION = upload_func
        else:
            DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
            if log_file_path is None:
                log_file_path = './rasp.log'
            if log_format is None:
                log_format = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
            import logging
            logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                                filename=log_file_path,
                                filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                                # a是追加模式，默认如果不写的话，就是追加模式
                                format=log_format,
                                datefmt=DATE_FORMAT
                                # 日志格式
                                )
            print("本地日志模式")
            pass
            
    else:
        import sentry_sdk
        sentry_sdk.init(dsn=sentry_dsn)

    from rasp_util.monkey_patch import sql_patch

    sql_patch.patch()

    from rasp_util.monkey_patch import command_patch

    command_patch.patch()

    from rasp_util.monkey_patch import file_patch

    file_patch.patch()

    from rasp_util.monkey_patch import http_server_patch

    http_server_patch.patch()

    print("use rasp util success")
