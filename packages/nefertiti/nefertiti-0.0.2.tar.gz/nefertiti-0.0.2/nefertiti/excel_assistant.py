import math
import re


def parse_pretty_number(number_str):
    """如果内容为 ="数字" 格式, 则提取数字部分"""
    result = re.search(r'^="((?:\-)?[\d,\.]+)"$', number_str)
    if result:
        return result.group(1)
    return number_str


def get_pretty_number(number):
    """输出带公式的数字

    Excel显示数字时，如果数字大于12位，它会自动转化为科学计数法；
    如果数字大于15位，它不仅用于科学技术法表示，还会只保留高15位，其他位都变0。
    :param number:
    :return:
    """
    if number and (type(number) in [int, float] or re.match(r'(\-)?[\d,\.]+', number)):
        return '="{}"'.format(number)
    return number


def column_index(key):
    """将Excel列编号转化成从0开始的序号

    :param key: 列名, 如"A", "BX"
    :return: 从0开始的列序号
    """
    key = key.upper()
    length = len(key)
    index = -1
    for i in range(length):
        index = index + (ord(key[length - 1 - i]) - 64) * int(math.pow(26, i))
    return index


def column_key(index):
    """将Excel列序号转化成大写字母编号

    :param index: 从0开始的列序号
    :return: 列名, 如"A", "ZB"
    """
    key = chr(index % 26 + 65)
    while index > 25:
        index = index // 26
        key = chr(index % 26 + 64) + key
    return key


if __name__ == '__main__':
    print(column_index('A'))  # 0
    print(column_index('B'))  # 1
    print(column_index('C'))  # 2
    print(column_index('Q'))  # 16
    print(column_index('Z'))  # 25
    print(column_index('AB'))  # 27
    print(column_index('BO'))  # 66
    a = get_pretty_number(123456789123456789)
    print(a)
    print(parse_pretty_number(a))

    a = get_pretty_number('123,456,789,123,456,789')
    print(a)
    print(parse_pretty_number(a))

    a = get_pretty_number(123456789.123456789)
    print(a)
    print(parse_pretty_number(a))
