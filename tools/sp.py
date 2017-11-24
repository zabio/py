# -*- coding: UTF-8 -*-
from dimens import execute


def sp_execute():
    _path = input('请输入文件路径:\t')

    execute(_path, '\">', '</dimen>', 'sp')

