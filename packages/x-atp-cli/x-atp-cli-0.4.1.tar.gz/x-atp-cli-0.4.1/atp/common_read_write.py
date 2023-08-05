import json


def write_data(file_name, data_, flag='', mode='w+'):
    """
    # 描述:
        公共写方法
    # 用法0（写入json数据）:
        write_data('./json_data.json', {'key': 'value'}, 'json', 'w+')
    # 用法1（写入文本）:
        write_data('./json_data.txt', '{"key": "value"}', 'w+', 'w+')
    # 用法2（写入二进制数据）:
        write_data('./json_data.xlsx', '{"key": "value"}', 'wb', 'w+')
    # 用法3（追加写入文本）:
        write_data('./json_data.txt', '{"key": "value"}\n', 'a+', 'a+')
    """
    if flag.lower() == 'json' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8') as fp:
            fp.write(json.dumps(data_))
    elif flag.lower() == 'eval' and mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(eval(data_))
    elif flag.lower() == 'wb' and mode.lower() == 'w+':
         with open(file_name, 'wb')as fp:
             fp.write(data_)
    elif mode.lower() == 'w+':
        with open(file_name, 'w+', encoding='utf-8')as fp:
            fp.write(data_)
    else:
        with open(file_name, 'a+', encoding='utf-8')as fp:
            fp.write(data_)


def read_data(file_name, flag='json', mode='r'):
    """
    # 描述:
        公共读方法
    # 用法0（读取json数据）:
        read_data('./json_data.json', 'json', 'r')
    # 用法1（读取文本）:
        read_data('./json_data.txt', '', 'r')
    """
    if mode == 'r':
        with open(file_name, 'r', encoding='utf-8')as fp:
            data_ = fp.read()
    elif mode == 'rb':
        # 不加encoding
        with open(file_name, 'rb')as fp:
            data_ = fp.read()
    else:
        with open(file_name, 'r+', encoding='utf-8')as fp:
            data_ = fp.read()
    if flag == 'json':
        return json.loads(data_)
    elif flag == 'eval':
        return eval(data_)
    else:
        return data_
