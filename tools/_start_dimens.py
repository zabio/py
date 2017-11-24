# -*- coding: UTF-8 -*-
from dimens import execute


def start():
    _option = input('请输入操作命令: [0->sp, 1->dp ,2->通用 ]\n: ')

    if _option == '0':
        switch_op('sp')
    elif _option == '1':
        switch_op('dp')
    elif _option == '2':
        common_execute()
    else:
        print('请输入正确的指令!!!')


def switch_op(_unit):
    _path = input('请输入文件路径\n: ')
    execute(_path, '<dimen', '\">', '</dimen>', _unit, True)


def common_execute():
    print('通用逐行操作  ***一定包含***前缀_*单位_后缀***')
    _path = input('请输入文件路径\n: ')
    _match = input('请输入单行匹配\n: ')
    _prefix = input('请输入前缀\n: ')
    _suffix = input('请输入后缀\n: ')
    _unit = input('请输入单位\n: ')
    execute(_path, _match, _prefix, _suffix, _unit)


start()
