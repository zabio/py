# -*- coding: UTF-8 -*-
import time


def execute(_path, _match, _prefix, _suffix, _unit, _create_new_file):  # 执行
    """
        strftime(format[, tuple]) -> string
    """
    if _create_new_file is True:
        execute_create_new_file(_path, _match, _prefix, _suffix, _unit)
    else:
        execute_replace(_path, _match, _prefix, _suffix, _unit)


def execute_replace(_path, _match, _prefix, _suffix, _unit):
    with open(_path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
    for line in lines:
        if _match in line:
            start = line.find(_prefix)
            end = line.find(_suffix)
            sp = line[start + 2:end]

            value = int(sp[0:sp.find(_unit)])

            if value > 0:
                new_sp = str(value / 2) + _unit
                line = line.replace(sp, new_sp)
        f.write(line)


def execute_create_new_file(_path, _match, _prefix, _suffix, _unit):
    with open(_path, 'r+') as f:
        lines = f.readlines()
        # f.seek(0)
        # f.truncate()
        _f_name = f.name
        _index = _f_name.rfind('.')
        _new_f_name = _f_name[0:_index] + '_' + str(int(time.time())) + _f_name[_index:]
        print(_new_f_name)
        new_file = open(_new_f_name, 'w+')
        for line in lines:
            if _match in line:
                start = line.find(_prefix)
                end = line.find(_suffix)
                sp = line[start + 2:end]

                value = int(sp[0:sp.find(_unit)])

                if value > 0:
                    new_sp = str(value / 2) + _unit
                    line = line.replace(sp, new_sp)
            # f.write(line)
            new_file.write(line)

        new_file.close()
