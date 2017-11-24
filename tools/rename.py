# -*- coding: UTF-8 -*-
import os
from number_format import change


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


rename()
