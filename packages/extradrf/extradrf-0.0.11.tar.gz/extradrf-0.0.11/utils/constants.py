# -*- coding: utf-8 -*- 
class Actions(object):
    CREATE = 1
    UPDATE = 2
    DELETE = 3


RELEASE_MODE = 1
BLOCK_MODE = 2
FILTER_MODE = 3

IP_MODES = {
    RELEASE_MODE: '直通模式',
    BLOCK_MODE: '屏蔽模式',
    FILTER_MODE: '过滤模式'
}
