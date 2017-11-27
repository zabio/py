# -*- coding: UTF-8 -*-
import os
import re

from number_format import *


def rename():
    path = input('请输入文件路径:\t') + r'/'

    files = os.listdir(path)
    for f in files:
        # 文件名
        file_name = os.path.splitext(f)[0]
        # 文件扩展名
        file_type = os.path.splitext(f)[1]

        index = file_name.find('集') + 1

        new_file_name = file_name[index - 3:index]

        new_file = path + new_file_name + file_type

        os.rename(path + f, change(new_file))


def replace():
    path = input('请输入文件路径:\t') + r'/'
    path = re.sub('[\s+]', '', path)
    replace_execute(path)


def replace_execute(path):
    old_str = input('请输入要替换的文字:\t')
    replace_str = input('请输入替换后的文字: 0->默认: \t')
    if replace_str == "0":
        replace_str = ""
    files = os.listdir(path)
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]
            new_file_name = file_name.replace(old_str, replace_str)
            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, change(new_file_name, "第", "集")))

    is_continue = input('是否继续: [y:是，n:否] \t')
    if is_continue:
        replace_execute(path)
    else:
        exit()


# rename()
replace()
