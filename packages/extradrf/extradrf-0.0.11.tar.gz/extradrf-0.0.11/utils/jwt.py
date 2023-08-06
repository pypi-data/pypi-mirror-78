#!/usr/bin/env python
# encoding: utf-8
# @author: dongwei
# @license: (C) Copyright 2019, IKGlobal Corporation Limited.
# @contact: dongwei@ikglobal.com
# @file: convert.py
# @time: 2019/11/30 4:43 下午
# @desc:

import json
from base64 import urlsafe_b64decode


def decode64(s: bytes) -> str:
    s_bin = s.encode('ascii')
    s_bin += b'=' * (4 - len(s) % 4)
    return urlsafe_b64decode(s_bin)


class ModuleAuthInfo:
    def __init__(self, read, write):
        self.read = read
        self.write = write


class JWTModel:

    def __init__(self, token_info):
        self.token_info = token_info
        _, self.b64_message, _ = token_info.split('.')
        self.message = json.loads(decode64(self.b64_message))
        self.user_id = self.message['user_id']
        self.username = self.message['username']
        self.domain_id = self.message['domain_id']
        self.domain_name = self.message['domain_name']
        self.system_admin = self.message['system_admin']
        self.modules = self.message['modules']
        self.modules_dict = {}
        self.parse_modules()

    def parse_modules(self):
        for m in self.modules:
            self.modules_dict[m['name'].lower()] = ModuleAuthInfo(m['read'], m['write'])

    def has_permission(self, path_info, opt):
        paths = path_info.split('/')
        service_name = paths[1]
        app_name = paths[2]
        path = service_name + app_name
        # service_name = "isp"
        if path in self.modules_dict:
            module = self.modules_dict[path]
        elif app_name in self.modules_dict:
            module = self.modules_dict[app_name]
        elif service_name in self.modules_dict:
            module = self.modules_dict[service_name]
        else:
            return False
        if module.write:
            return True
        elif module.read and 'GET' == opt:
            return True
        return False
