# -*- coding: UTF-8 -*-


def rename():
    path = input('请输入文件路径:\t')

    with open(path, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if '<dimen' in line:
                start = line.find('\">')
                end = line.find('</dimen>')
                sp = line[start + 2:end]

                value = int(sp[0:sp.find('sp')])

                if value > 0:
                    new_sp = str(value / 2) + 'sp'
                    line = line.replace(sp, new_sp)

            f.write(line)


rename()
