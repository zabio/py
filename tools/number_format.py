# -*- coding: UTF-8 -*-
from convertChineseDigitsToArabic import convert_chinese_digits2_arabic


def change(string):
    split = list(string)
    new_str = ''
    for s in split:
        new_str += format_number(s)
    return new_str


def change(text, start_str, end_str):
    index_start = text.indexof(start_str)
    index_end = text.indexof(end_str)
    digits = text[index_start, index_end]
    arabic = format_chinese_digits(digits)
    text = text.replace(digits, arabic)
    return text


# 九 万 八 千 七 百 六 十 五
# 1  2  3  4  5  6  7  8  9
def format_chinese_digits(chinese_digits):
    return convert_chinese_digits2_arabic(chinese_digits)


def format_number(big_number):
    if big_number == '一':
        return '1'
    elif big_number == '二':
        return '2'
    elif big_number == '三':
        return '3'
    elif big_number == '四':
        return '4'
    elif big_number == '五':
        return '5'
    elif big_number == '六':
        return '6'
    elif big_number == '七':
        return '7'
    elif big_number == '八':
        return '8'
    elif big_number == '九':
        return '9'
    elif big_number == '零':
        return '0'
    elif big_number == '十':
        return '10'
    elif big_number == '百':
        return '100'
    elif big_number == '千':
        return '1000'
    elif big_number == '万':
        return '10000'
    else:
        return big_number
