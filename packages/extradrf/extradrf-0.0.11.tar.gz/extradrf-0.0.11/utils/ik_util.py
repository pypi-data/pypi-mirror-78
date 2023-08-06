# -*- coding:utf-8 -*-
import psutil
import os
import re
import hashlib
import datetime
from math import ceil
# from re import compile
from functools import lru_cache
from functools import partial
# from blinker import Namespace
from django.conf import settings
import os

# file_path =

def read_file(path):
    bufsize = 65535
    with open(path) as infile:
        while True:
            lines = infile.readlines(bufsize)
            if not lines:
                break
            yield " ".join((map(lambda x: x.strip(" ").strip("\n").strip("\r\n"), lines)))

def handle_uploaded_file(file, path=settings.MEDIA_ROOT):
    file_path = "{}{}{}".format(path, os.sep, file.name)
    # print(file_path)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


def handle_multi_uploaded_file(file_dict, path=settings.MEDIA_ROOT):

    if not os.path.exists(path):
        os.system("mkdir {}".format(path))

    for _, file in file_dict:
        file_path = "{}{}{}".format(path, os.sep, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    file_list = path.rsplit(os.sep, maxsplit=1)
    media_root, file_dirname = file_list[0], file_list[1]

    os.system("cd {}".format(media_root))
    file_zip = zip_file(file_dirname)
    if not file_zip:
        return None
    file_zip_path = "{}{}{}".format(media_root, os.sep, file_zip)
    return file_zip_path


def zip_file(name):
    # tar -czf netopeer.tar.gz netopeer
    cmd = "tar -czf {}.tar.gz {}".format(name, name)
    os.system(cmd)
    return "{}.tar.gz".format(name) if "{}.tar.gz".format(name) else ""


""" 
def test_save_file(dir_path='D:\\shen\\python\\PythonWebDev\\web_develop\\DRF\\tianshu\\isp_manager\\files\\'):
    file_path = dir_path + "test.txt"
    with open(file_path, 'wb+') as destination:
        # for chunk in file.chunks():
        destination.write(b"sss")
    return file_path 
"""


def model_tbl_name(name):
    if not name:
        return ''
    return "tbl_{}".format(name.lower())


def convert(one_string, space_character):
    # one_string:输入的字符串；space_character:字符串的间隔符，以其做为分隔标志
    """ 
    convert("border-bottom-color","-") ==> 'borderBottomColor'
    """
    string_list = str(one_string).split(space_character)  # 将字符串转化为list
    first = string_list[0].lower()
    others = string_list[1:]

    others_capital = [word.capitalize()
                      for word in others]  # str.capitalize():将字符串的首字母转化为大写

    others_capital[0:0] = [first]

    hump_string = ''.join(others_capital)  # 将list组合成为字符串，中间无连接符。

    return hump_string


def get_file_size_by_mbytes(file):
    return ceil(file.size / 1000 / 1000)


def time_delta(d1, d2):
    # d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')
    # d2 = datetime.datetime.strptime(d2, '%Y-%m-%d')
    # datetime.date()
    delta = d1 - d2
    return delta.days


# def create_signal(name="default_signal"):
#     web_signals = Namespace()
#     return web_signals.signal(name)


__formaters = {}
percent_pattern = re.compile(r"%\w")
brace_pattern = re.compile(r"\{[\w\d\.\[\]_]+\}")
UPLOAD_FOLDER = '/tmp/vppmdir'

HERE = os.path.abspath(os.path.dirname(__file__))


def get_file_md5(f, chunk_size=8192):
    h = hashlib.md5()
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()


def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)


get_file_path = partial(os.path.join, UPLOAD_FOLDER)
# get_file_path = partial(os.path.join, HERE, UPLOAD_FOLDER)


def formater(text):
    percent = percent_pattern.findall(text)
    brace = brace_pattern.findall(text)
    if percent and brace:
        raise Exception("mixed format is not allowed")
    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif "%(" in text:
        return lambda *a, **kw: text % kw
    else:
        return text.format


def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f


@lru_cache(typed=True)
def gen_hexdigest(raw_str):
    m2 = hashlib.md5()
    m2.update(raw_str.encode())
    return m2.hexdigest()


def get_match(pattern, str):
    if not pattern:
        # 没有pattern，匹配ip
        pattern = re.compile(
            "(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)")
    m = re.search(pattern, str)
    return m.groups()


def str2line(word_list):

    line = ''
    i = 0
    blank_end = len(word_list) - 1

    for word in word_list:
        line += word
        if i < blank_end:
            line += ' '
        else:
            line += '.'
        i += 1

    return line


def ik_sprintf(format, param_list):

    tmp_list = []
    i = 0
    flag = True
    param_num = len(param_list)
    format_symbol_num = format.count('%')

    if param_num == format_symbol_num:
        str_list = format.split(' ')
        for item in str_list:

            tmp_str = item
            if item.find('%d') >= 0:
                if not isinstance(param_list[i], int):
                    flag = False
                    break

                tmp_str = str(param_list[i])
            elif item.find('%s') >= 0:
                if not isinstance(param_list[i], str):
                    flag = False
                    break

                tmp_str = param_list[i]

            if ' ' != tmp_str:
                tmp_list.append(tmp_str)
                i += 1

        return str2line(tmp_list)
    else:
        return format + 'is in error format!'


def test_ik_sprintf():

    print(ik_sprintf('%s %s %s', ['l', 'z', 'c']))
    print(ik_sprintf('%s %d %d %d', ['l', 0, 0, 354318]))


def fiber_list_name_map(fiber_list, name_list):

    i = 0
    for name in name_list:
        fiber_list[i]['name'] = name
        i += 1

    return fiber_list


def remove_ip_mask_len(str_ip):
    idx = str_ip.find('/')
    if idx >= 0:
        return str_ip[0: idx]
    else:
        return str_ip


def ik_cmd_make(cmd_word_list):
    '''
    把命令的封装放在一个地方，管理起来比较方便
    eg ['ifconfig', 'eth1', 'down']
    to 'ifconfig eth1 down'
    '''
    i = 0
    str_cmd = ''
    blank_end = len(cmd_word_list) - 1
    for cmd_word in cmd_word_list:
        str_cmd += cmd_word
        if i < blank_end:
            str_cmd += ' '
        i += 1

    return str_cmd


IPV4_MASK = {
    0: '0.0.0.0',
    1: '128.0.0.0',
    2: '192.0.0.0',
    3: '224.0.0.0',
    4: '240.0.0.0',
    5: '248.0.0.0',
    6: '252.0.0.0',
    7: '254.0.0.0',
    8: '255.0.0.0',
    9: '255.128.0.0',
    10: '255.192.0.0',
    11: '255.224.0.0',
    12: '255.240.0.0',
    13: '255.248.0.0',
    14: '255.252.0.0',
    15: '255.254.0.0',
    16: '255.255.0.0',
    17: '255.255.128.0',
    18: '255.255.192.0',
    19: '255.255.224.0',
    20: '255.255.240.0',
    21: '255.255.248.0',
    22: '255.255.252.0',
    23: '255.255.254.0',
    24: '255.255.255.0',
    25: '255.255.255.128',
    26: '255.255.255.192',
    27: '255.255.255.224',
    28: '255.255.255.240',
    29: '255.255.255.248',
    30: '255.255.255.252',
    31: '255.255.255.254',
    32: '255.255.255.255'
}

IPV4_MASK_R = {
    '0.0.0.0': 0,
    '128.0.0.0': 1,
    '192.0.0.0': 2,
    '224.0.0.0': 3,
    '240.0.0.0': 4,
    '248.0.0.0': 5,
    '252.0.0.0': 6,
    '254.0.0.0': 7,
    '255.0.0.0': 8,
    '255.128.0.0': 9,
    '255.192.0.0': 10,
    '255.224.0.0': 11,
    '255.240.0.0': 12,
    '255.248.0.0': 13,
    '255.252.0.0': 14,
    '255.254.0.0': 15,
    '255.255.0.0': 16,
    '255.255.128.0': 17,
    '255.255.192.0': 18,
    '255.255.224.0': 19,
    '255.255.240.0': 20,
    '255.255.248.0': 21,
    '255.255.252.0': 22,
    '255.255.254.0': 23,
    '255.255.255.0': 24,
    '255.255.255.128': 25,
    '255.255.255.192': 26,
    '255.255.255.224': 27,
    '255.255.255.240': 28,
    '255.255.255.248': 29,
    '255.255.255.252': 30,
    '255.255.255.254': 31,
    '255.255.255.255': 32
}


def cal_ipv4_mask_len(mask_val):
    return IPV4_MASK_R.get(mask_val, None)
    # for key in IPV4_MASK:
    #     if mask_val == IPV4_MASK[key]:
    #         return key

    # return None


def set_bit(value, index):
    """
    将第 index 位设置为 1
    """

    mask = 1 << index
    value &= ~mask
    value |= mask

    return value


def clear_bit(value, index):
    """
    将第 index 位设置为 0
    """

    mask = 1 << index
    value &= ~mask
    return value


def ipv4_addr_chk(str_ip):
    str_ip = str_ip.lstrip(' ')
    ip_and_len = str_ip.split('/')
    compile_ip = re.compile(
        '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(ip_and_len[0]):
        return True
    else:
        return False


def str2int(str_number):

    if isinstance(str_number, str):
        if str_number.isdigit():
            return int(str_number)

    return None


def test():
    test_ik_sprintf()


# 显示当前 python 程序占用的内存大小
def show_memory_info(hint):
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    return '{} memory used: {} MB'.format(hint, memory)


def show_memory_info2():
    pid = os.getpid()
    p = psutil.Process(pid)
    p_name = p.name()

    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    return 'pid:{} p_name:{} memory used: {} MB'.format(pid, p_name, memory)


def func():
    # show_memory_info('initial')
    # a = [i for i in range(10000000)]#返回a不会及时销毁其占用的内存，会一直持有内存
    show_memory_info('after a created')
    # return a

# a = func()
# show_memory_info('finished')


if __name__ == "__main__":
    print(show_memory_info)
    # print(test_save_file())
    # key = "web_develop:users:%s"
    # _id = 1
    # print(format(key % "{id_}", id_=_id))
    # print(type(time_delta("2018-1-1", "2019-1-1")))
