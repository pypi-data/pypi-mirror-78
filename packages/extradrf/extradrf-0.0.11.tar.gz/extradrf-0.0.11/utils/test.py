# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2019/11/24 19:48:13
@Author  :   Shen Xianjie
@Contact :   jay1211@ik.com
@Desc    :   None
'''

import os
import socket
import yaml
# from django.test import TestCase


class BaseController():
    """
    BaseController
    """


class TestCase():
    """
    TestCase
    """


class Controller(object):
    """
    Controller
    """


def func1(arg1):
    """
    param arg1:
    return:
    """


class Logger():
    """
    Logger
    """

    def record(self, content):
        """
        param content:
        return:
        """
        print("I write a log into file: {}".format(content))


class DB():
    """
    DB
    """

    def record(self, content):
        """
        param content:
        return:
        """
        print("I write a db into file: {}".format(content))


def test(recorder):
    """
    param :
    return:
    """
    getattr(recorder, 'record')('shen')


def demo():
    """
    param :
    return:
    """
    logger = Logger()
    db = DB()
    test(logger)
    test(db)


LDAP_HOST = "10.222.10.244"
LDAP_PORT = 389


def test_start_tcp_client():

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # tcp_client.bind((LDAP_HOST, LDAP_PORT))
        tcp_client.connect(("10.222.10.244", 389))
    except socket.error as e:
        print(str(e))
    else:
        print('sending..........')
        tcp_client.sendall(b"{'username':'jay1211', 'password':'Jxs93503'}")

        print('reading...........')
        print(tcp_client.recv(1024))
    tcp_client.close()


class Monster(yaml.YAMLObject):
    yaml_tag = '!monster'
    # yaml_loader = yaml.SafeLoader

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self._hp = hp
        self._ac = ac
        self.attacks = attacks

    def __repr__(self):
        return "%s(name=%r, hp=%r, ac=%r, attacks=%r)" % (
            self.__class__.__name__, self.name, self._hp, self._ac,
            self.attacks)


class Person(yaml.YAMLObject):
    yaml_tag = '!person'

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return '%s(name=%s, age=%d)' % (self.__class__.__name__, self.name, self.age)


def test_yaml():
    from yaml import load, dump

    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    # yaml.load("""
    # - Hesperiidae
    # - Papilionidae
    # - Apatelodidae
    # - Epiplemidae
    # """)

    documents = """
    ---
    name: The Set of Gauntlets 'Pauraegen'
    description: >
        A set of handgear with sparks that crackle
        across its knuckleguards.
    ---
    name: The Set of Gauntlets 'Paurnen'
    description: >
    A set of gauntlets that gives off a foul,
    acrid odour yet remains untarnished.
    ---
    name: The Set of Gauntlets 'Paurnimmen'
    description: >
    A set of handgear, freezing with unnatural cold.
    """

    # yaml.load("""
    # none: [~, null]
    # bool: [true, false, on, off]
    # int: 42
    # float: 3.14159
    # list: [LITE, RES_ACID, SUS_DEXT]
    # dict: {hp: 13, sp: 5}
    # """)

    # obj = yaml.load("""
    # !!python/object:__main__.Hero
    # name: Welthyr Syxgon
    # hp: 1200
    # sp: 0
    # """, )
    # print(obj)
    # print(type(obj))

    monster = yaml.load("""---!monster name:Cave spider hp:[2,6] ac:16 attacks:[BITE,HURT]
    """, Loader=Loader)
    print(monster)
    print(type(monster))
    print(yaml.dump(Monster(name='Cave lizard', hp=[
        3, 6], ac=16, attacks=['BITE', 'HURT'])))
    print(type(yaml.dump(Monster(name='Cave lizard', hp=[
        3, 6], ac=16, attacks=['BITE', 'HURT']))))
    # 输出
    # !Monster
    # ac: 16
    # attacks: [BITE, HURT]
    # hp: [3, 6]
    # name: Cave lizard


class Hero:
    def __init__(self, name, hp, sp):
        self.name = name
        self.hp = hp
        self.sp = sp

    def __repr__(self):
        return "%s(name=%r, hp=%r, sp=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.sp)


def test_dirname():
    dir_name = os.path.dirname(os.path.abspath(__file__)).split(os.sep)[-1]
    print(dir_name)


if __name__ == "__main__":
    test_yaml()
