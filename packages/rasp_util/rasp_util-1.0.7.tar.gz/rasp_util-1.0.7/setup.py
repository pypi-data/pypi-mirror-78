from setuptools import setup, find_packages

setup(
    # 以下为必需参数
    name='rasp_util',  # 模块名
    version='1.0.7',  # 当前版本
    python_requires='>=3.4.0', # python环境
    description='RASP project',  # 简短描述
    py_modules=["rasp_util"], # 单文件模块写法
    # ckages=find_packages(exclude=['contrib', 'docs', 'tests']),  # 多文件模块写法
    packages=['rasp_util.attack_rules','rasp_util.hook_func','rasp_util.monkey_patch','rasp_util.sentry','rasp_util'],  #这里是所有代码所在的文件夹名称
    # 以下均为可选参数
    long_description="",# 长描述
    url='https://github.com/pypa/sampleproject', # 主页链接
    author='The Python Packaging Authority', # 作者名
    author_email='pypa-dev@googlegroups.com', # 作者邮箱

    keywords='sample setuptools development',  # 模块的关键词，使用空格分割
    install_requires=['sentry_sdk','future'], # 依赖模块

    # data_files=[('my_data', ['data/data_file'])], # 类似package_data, 但指定不在当前包目录下的文件
)