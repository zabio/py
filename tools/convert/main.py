import os

import re

from convert.function import *


def start():
    path = input('请输入文件路径:\t') + r'/'
    path = re.sub('[\s+]', '', path)

    # try:
    files = os.listdir(path)
    execute(path, files)
    # except IOError:
    #    print("Error: 请输入有效的文件路径!!!")


def execute(path, files):
    option = input("请输入操作 0:插入,1:替换,2:替换 start_end ,3:删除,4:删除 start_end  ===>\t:")

    select_option(path, option)

    is_continue = input('是否继续: [y:是，n:否] ===>\t')
    if is_continue == "y":
        execute(path, files)
    else:
        exit()


def select_option(path, option):
    files = os.listdir(path)
    if option == '0':
        text = input("请输入插入的字符===>\t:")
        index = input("请输入插入的index[0:开始,-1:结尾,else:中间]===>\t:")
        rename0(path, files, text, int(index))
    elif option == '1':
        old_str = input("请输入需要替换的字符===>\t:")
        new_str = input("请输入替换的字符===>\t:")
        rename1(path, files, old_str, new_str)
    elif option == '2':
        start_index = input("请输入需要替换的开始位置===>\t:")
        end_index = input("请输入需要替换的结束位置===>\t:")
        new_str = input("请输入替换的字符===>\t:")
        rename2(path, files, new_str, int(start_index), int(end_index))
    elif option == '3':
        old_str = input("请输入需要删除的字符===>\t:")
        rename3(path, files, old_str)
    elif option == '4':
        start_index = input("请输入开始位置===>\t:")
        end_index = input("请输入位置===>\t:")
        rename4(path, files, int(start_index), int(end_index))


def rename0(path, files, text, index):
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]
            new_file_name = insert(file_name, text, index)
            print(new_file_name)
            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, new_file_name))


def rename1(path, files, old_str, new_str):
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]
            new_file_name = replace(file_name, old_str, new_str)
            print(new_file_name)
            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, new_file_name))


def rename2(path, files, new_str, start_index, end_index):
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]
            new_file_name = replace2(file_name, new_str, start_index, end_index)
            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, new_file_name))


def rename3(path, files, old_str):
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]

            new_file_name = delete(file_name, old_str)

            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, new_file_name))


def rename4(path, files, start_index, end_index):
    for f in files:
        # 如果不是文件夹
        if not os.path.isdir(f):
            # 文件名
            file_name = os.path.splitext(f)[0]
            # 文件扩展名
            file_type = os.path.splitext(f)[1]
            new_file_name = delete2(file_name, start_index, end_index)
            new_file_name += file_type
            print(new_file_name)
            # 使用join
            os.rename(os.path.join(path, f), os.path.join(path, new_file_name))


start()
