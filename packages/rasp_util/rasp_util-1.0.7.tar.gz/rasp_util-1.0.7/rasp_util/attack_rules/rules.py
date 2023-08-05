import re
from .risk_level import *


def get_sql_regex():
    """
    查询数据库并获取所有符合要求（比如超过某个级别）的 regex
    :return: 所有正则表达式
    """
    return {"union.*select.*from.*information_schema": 7, "select.*group_concat.*from.*sqlite_master": 7,
            "load_file\(": 7, "benchmark\(": 7, "sleep\(": 7, "is_srvrolemember\(": 7, "updatexml\(": 7,
            "extractvalue\(": 7,
            "(select|null).*(select|null).*(select|null)": 7, ";(select|update|insert|delete)": 7,
            "into (outfile|dumpfile|union|case)": 1, "hex\(": 1, "mid\(": 1, "ord\(": 1, "ascii\(": 1, "bin\(": 1}


def get_input_regex():
    """
    查询数据库并获取所有符合要求（比如超过某个级别）的 regex
    :return: 所有正则表达式
    """
    return {"(\\s+|,|;)(select|file|from|;)(\\s+|,|;)": 1}


# sql注入 是否包含sql注入
def sql_injection(sql_statement):
    regexs = get_sql_regex()
    for regex in regexs.keys():
        if re.search(regex, sql_statement):
            return regexs[regex]
    else:
        return 0


# --------检测是否存在未闭合的单引号---------
def judge_apostrophe(sql_statement):
    level = 5
    if len(re.findall("\'", sql_statement)) % 2 == 1:
        return level
    # -----检测单引号是否符合语法，有必要吗,不符合语法数据库不会执行成功？，暂留

    return 0


def sql_levels_of_danger(sql_statement):
    """
    获取危险等级 0-安全，1-低风险; 4-中风险， 7-高风险; 2 3 5 6 保留值
    :param sql_statement: sql语句
    :return: sql语句 风险值
    """
    sql_statement = sql_statement.lower()

    danger_level = 0

    danger_level = max(sql_injection(sql_statement), danger_level)

    danger_level = max(judge_apostrophe(sql_statement), danger_level)

    return danger_level


# 判断用户输入危险等级
def judge_userinput(userinput):
    regexs = get_input_regex()
    for regex in regexs.keys():
        if re.search(regex, userinput):
            return regexs[regex]
    else:
        return 0


def is_token_changed(userinput):
    level = 4
    return level if len(userinput.split(" ")) >= 2 else 0


# 判断用户输入是否穿越了多个token
def input_of_danger(userinput):
    userinput = userinput.lower()

    danger_level = 0

    danger_level = max(danger_level, judge_userinput(userinput))

    danger_level = max(danger_level, is_token_changed(userinput))

    return danger_level


# 是否包含命令注入
def command_injection(command):
    block_rules = ["&&", "||", "&", ";", "$IFS", "${IFS}"]
    suspect_regexs = [
        "{0,6}/bin/(?:ba)?sh|fsockopen\(.{1,50}/bin/(?:ba)?sh|perl.cat.{1,5}/etc/passwd|nc.{1,30}-e.{1,100}/bin/(?:ba)?", \
        "sh|bash\\s-.{0,4}i.{1,20}/dev/tcp/|subprocess.call\(.", \
        "{0,6}/bin/(?:ba)?sh|fsockopen\(.{1,50}/bin/(?:ba)?sh|perl.", \
        "{1,80}socket.{1,120}open.{1,80}exec\(.{1,5}/bin/(?:ba)?sh"]
    suspect_rules = ["curl", "bash", "cat", "sh"]
    for rule in block_rules:
        if command.find(rule) != -1:
            raise Block_Attack("命令注入攻击：执行敏感命令" + command)
    for rule in suspect_rules:
        if command.find(rule) != -1:
            raise Suspect_Attack("命令注入警告：执行敏感命令" + command)
    for regex in suspect_regexs:
        if re.search(regex, command):
            raise Block_Attack("命令注入警告：渗透命令" + command)


def file_injection(file_path):
    block_exception_protocol = ["file://", "php://", "gopher://", "netdoc://", "dict://", "zip://"]
    block_sensitive_directory = ['/etc/issue', '/etc/shadow', '/etc/passwd', '/etc/hosts', '/etc/apache2/apache2.conf', \
                                 '/root/.bash_history', '/root/.bash_profile', \
                                 'c:\\\\windows\\\\system32\\\\inetsrv\\\\metabase.xml', \
                                 'c:\\\\windows\\\\system32\\\\drivers\\\\etc\\\\hosts']
    block_path_travel = ["/../", "../", "..\\", "\\..\\", "%2e%2e%2f", "%2E%2E%2F"]
    block_write_NTFS = ["::\$(DATA|INDEX)$"]
    block_regexs = [
        "\.(do[c|t][x|m|]?|xl[s|t][x|m|b]?|pp[t|s|a][x|m]|pot[x|m]|7z|tar|gz|bz2|xz|rar|zip|jpg|jpeg|png|gif|bmp|txt|)$"]  # 白名单
    suspect_exception_file_type = ["http://", "https://"]
    file_inject_str = {"文件操作攻击：访问异常网址": block_exception_protocol, \
                       "文件操作攻击：包含敏感目录": block_sensitive_directory, \
                       "文件操作攻击：存在路径穿越行为": block_path_travel}
    file_inject_re = {"文件操作攻击：写NTFS流文件": block_write_NTFS}
    # "文件操作攻击：异常文件类型":block_regexs}

    for inject in file_inject_str:
        for rule in file_inject_str[inject]:
            if file_path.find(rule) != -1:
                raise Block_Attack(inject + file_path)

    for rule in suspect_exception_file_type:
        if file_path.find(rule) != -1:
            raise Suspect_Attack("文件操作警告：访问异常网址" + file_path)

    for inject in file_inject_re:
        for rule in file_inject_re[inject]:
            if re.search(rule, file_path) != None:
                raise Block_Attack(inject + file_path)


if __name__ == "__main__":
    try:
        file_injection("http://152.136.235.152:9000/m3lon.txt")
        # command_injection("ls;bash")
    except Block_Attack as e:
        print(e.errorinfo)

    except Suspect_Attack as e:
        print(e.errorinfo)
