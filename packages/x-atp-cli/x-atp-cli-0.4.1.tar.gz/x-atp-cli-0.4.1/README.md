## X-ATP CLI Client

X自动化测试平台命令行客户端。

```shell
usage: x-atp-cli [-h] [-v] [-d] [-r ATP_SERVER_URL] [-t TEST_TYPE]
                 [-n WORKSPACE_NAME]

X ATP CLI Client (X 自动化测试平台命令行客户端)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         输出客户端版本信息
  -d, --demo            在当前目录下创建 `x_sweetest_example` 项目
  -r ATP_SERVER_URL, --run ATP_SERVER_URL
                        运行 X-ATP 自动测试执行端服务 (E.g x-atp-cli -r http://127.0.0.1
                        -t api -n 执行端001)
  -t TEST_TYPE, --type TEST_TYPE
                        测试执行端类型 api|web (与 -r 配合使用)
  -n WORKSPACE_NAME, --name WORKSPACE_NAME
                        执行端工作区的标识名称 (与 -r 配合使用)
```

## Sweetest of X-ATP

**X-Sweetest** 是基于 [Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/) 协议对 [Sweetest](https://github.com/tonglei100/sweetest) 的二次开发项目。

打开 PowerShell 或其他 Shell命令窗口，并转到指定目录，例如：`D:\Autotest`，输入以下命令快速开始体验。

```shell
x-atp-cli -d
cd x_sweetest_example
python echo.py
```

如果您以前使用过 [Sweetest](https://github.com/tonglei100/sweetest)，只需删除 <del>`from sweetest import Autotest`</del>，然后再添加 `from x_sweetest import Autotest`，例如：

```python
# from sweetest import Autotest
from x_sweetest import Autotest
import sys
......
```

### Change

同步Sweetest源码版本 —— [e0216c2f401a59dd34520f14bfb62ab89202d11d](https://github.com/tonglei100/sweetest/commit/e0216c2f401a59dd34520f14bfb62ab89202d11d)

#### v0.1.6

解决问题：TestCase文件 `输出数据` 字段不支持接口返回的 `[{'id':1},{'id':2}]` 格式的json数据。

更改 `keywords/http.py` 文件中的内容：

```python
            logger.info('%s: %s' % (k, repr(g.var[k])))
        elif k == 'json':
            sub_str = output.get('json', '{}')
            # 如果准备传递给 `injson` 模块处理的字符串中，第一个字符串等于 `[` 号
            if sub_str[0] == '[':
                # 取出 `[x]` 中的值，即第一维数组的下标
                index = sub_str.split(']')[0][1:]
                # 消除前面取第一维数组行为的影响，还原源处理字符串
                sub = json2dict(sub_str[len(index)+2:])
                # 取指定下标的第二维，即字典数据
                result = check(sub, response['json'][int(index)])
            else:
                sub = json2dict(output.get('json', '{}'))
                result = check(sub, response['json'])
            # logger.info('Compare json result: %s' % result)
            var = dict(var, **result['var'])
```

`xxx-TestCase.xlsx` 测试用例文件的编辑示例如下：

……|输出数据|……
-|-|-
……|json=[0]{'id':'\<id1\>'}|……
……|json=[-1]{'id':'\<id2\>'}|……

#### v0.1.7&v0.3.8

优化问题：简化TestCase文件 `测试数据` 字段中导入文件功能的编写格式，添加 `form` 用法。

更改 `keywords/http.py` 文件中的内容：

```python
        if _data['params']:
            logger.info(f'PARAMS: {_data["params"]}')

    elif kw == 'post':
        # 如果 `测试数据` 字段中包含 'form' 的json数据
        if 'form' in data:
            # 将 'form' json数据转为字典数据
            form_dict = json2dict(data['form'])
            try:
                fields_dict = {}
                for form_k, form_v in form_dict.items():
                    if form_k != 'file':
                        fields_dict[form_k] = form_v
                # 取出待上传的文件名称
                form_name = form_dict['file'][0].split("/")[-1]
                # fields_dict 是 MultipartEncoder 中 fields 字段需要的字典
                fields_dict.update({'file': (form_name, open(form_dict['file'][0], 'rb'), form_dict['file'][1])})
                # 使用 MultipartEncoder 模块对上传的文件进行解析
                form_data = MultipartEncoder(fields=fields_dict)
                # 在请求头里添加上传文件类型
                form_headers = {'Content-Type': form_data.content_type}
                http.r.headers.update(form_headers)
                r = getattr(http.r, kw)(http.baseurl + url, data=form_data, timeout=timeout)
            except:
                logger.exception("***form can be only one Key-value***")
        else:
            r = getattr(http.r, kw)(http.baseurl + url,
                                    data=_data['data'], json=_data['json'], files=_data['files'], timeout=timeout, **data)
        logger.info(f'BODY: {r.request.body}')

    elif kw in ('put', 'patch'):
```

`xxx-TestCase.xlsx` 测试用例文件的编辑示例如下：

……|测试数据|……
-|-|-
……|form={r'./files/test.xls': 'application/vnd.ms-excel'}|……
……|form={r'./files/test.zip': 'application/zip}|……
……|form={"phoneInfo": "mi6xbuild", 'file': [r'./files/1.jpg', 'application/octet-stream']},,|……

#### v0.2.2

解决问题：TestCase文件 `预期结果` 字段不支持接口返回的 `[{'status':1},{'status':2}]` 格式的json数据。

更改 `keywords/http.py` 文件中的内容：

```python
    expected['text'] = expected.get('text', None)
    json_str = expected.get('json', '{}')
    # 确保第一维数组的下标是存在的
    if json_str[0] == '[' and json_str[1] != ']':
        # 取出第一维数组的下标
        index = json_str.split(']')[0][1:]
        expected['json'] = json2dict(json_str[len(index) + 2:])
        # 在预期结果数据中，加入预期的第一维数组的下标
        expected['json_index'] = int(index)
    else:
        expected['json'] = json2dict(expected.get('json', '{}'))
    expected['cookies'] = json2dict(expected.get('cookies', '{}'))
```

以及：

```python
            logger.info('cookies var: %s' % (repr(result['var'])))

    if expected['json']:
        # 如果预期结果数据中存在第一维数组下标
        if 'json_index' in expected:
            # 取指定下标的第二维字典数据，并传递给 `injson` 模块处理
            result = check(expected['json'], response['json'][expected['json_index']])
        else:
            result = check(expected['json'], response['json'])
        logger.info('json check result: %s' % result)
        if result['code'] != 0:
```

`xxx-TestCase.xlsx` 测试用例文件的编辑示例如下：

……|预期结果|……
-|-|-
……|json=[0]{'status':0}|……
……|json=[-1]{'status':1}|……

#### v0.2.5

解决问题：PUT 请求方法不支持二进制传输。

更改 `keywords/http.py` 文件中的内容：

```python
        logger.info(f'BODY: {r.request.body}')

    elif kw in ('put', 'patch'):
        # 如果 `测试数据` 字段中包含 'binary' 的json数据
        if 'binary' in data:
            binary_dict = json2dict(data['binary'])
            try:
                if len(binary_dict) == 1:
                    for binary_k, binary_v in binary_dict.items():
                        # 在请求头里添加上传二进制数据的类型
                        binary_headers = {'Content-Type': binary_v}
                        http.r.headers.update(binary_headers)
                        # 读取待上传的文件的二进制数据，并传递到待发送的http请求中
                        with open(binary_k, 'rb') as binary_f:
                            r = getattr(http.r, kw)(http.baseurl + url, data=binary_f, timeout=timeout)
            except:
                logger.exception("*** binary can be only one Key-value***")
        else:
            r = getattr(http.r, kw)(http.baseurl + url,
                                    data=_data['data'], timeout=timeout, **data)
        logger.info(f'BODY: {r.request.body}')
```

`xxx-TestCase.xlsx` 测试用例文件的编辑示例如下：

……|测试数据|……
-|-|-
……|binary={r'./data/2209.jpg':'image/jpeg'}|……

#### v0.3.1

优化问题：修改请求头的 `user-agent` 标识符，便于开发提取日志，同时避免被判断为爬虫。

更改 `keywords/http.py` 文件中的内容：

```python
            http.r.headers.update(eval(http.headers_get))

    # 变更 user-agent 标识符，便于被测试服务端提取访问记录
    http.r.headers.update({'user-agent': 'AutoTest'})

    logger.info('URL: %s' % http.baseurl + url)
```

#### v0.3.3

解决问题：Element文件的 `value` 字段中使用 `{x}` 写法时，如果上一个接口获取到的 `x` 是 `int` 类型，会报异常。

更改 `keywords/http.py` 文件中的内容：

```python
    element = step['element']
    # 获取 Elements 中的 url，兼容 `{x}` 中的参数为非 str 类型的情况
    url = str(e.get(element)[1])
    if url.startswith('/'):
```

#### v0.3.7

解决问题：TestCase文件的 `预期结果` 字段中使用 `status_code=200,,` 写法时，如果前后有多余的空格，会报异常。

更改 `keywords/http.py` 文件中的内容：

```python
    if expected['status_code']:
        # 对比 实际响应状态码 与 预期响应状态码
        if str(expected['status_code']).strip() != str(response['status_code']).strip():
            raise Exception(
                f'status_code | EXPECTED:{repr(expected["status_code"])}, REAL:{repr(response["status_code"])}')
```

#### v0.3.9

解决问题：TestCase文件的 `测试数据` 字段中包括纯文本的 `<>` 时，会统一按变量匹配处理，而不是纯文本处理，会报异常。

更改 `utility.py` 文件中的内容：

```python
            data = data.replace(left_angle, '<').replace(right_angle, '>')
    # 将输入的 \< 和 \> 转换为纯文本的 <>
    data = data.replace(left_angle, '<').replace(right_angle, '>')
    return data
```

`xxx-TestCase.xlsx` 测试用例文件的编辑示例如下：

……|测试数据|……
-|-|-
……|headers={'terminal':"app"},,json={"name": "yt\\<\\>"}|……

#### v0.4.0

优化问题：测试报告 Excel 文件中的错误信息中，没有 HTTP 接口的请求 URL，定位问题不方便。

更改 `keywords/http.py` 文件中的内容：

```python
    var = {}  # 存储所有输出变量

    # 测试报告 “备注” 列显示URL请求地址
    REQUEST_URL = f'URL: {http.baseurl + url}\n'

    if expected['status_code']:
        # 对比 实际响应状态码 与 预期响应状态码
        if str(expected['status_code']).strip() != str(response['status_code']).strip():
            # 抛异常行加：{REQUEST_URL}
            raise Exception(
                f'{REQUEST_URL}status_code | EXPECTED:{repr(expected["status_code"])}, REAL:{repr(response["status_code"])}')

    if expected['text']:
        if expected['text'].startswith('*'):
            if expected['text'][1:] not in response['text']:
                raise Exception(f'{REQUEST_URL}text | EXPECTED:{repr(expected["text"])}, REAL:{repr(response["text"])}')
    # 下面的所有 Exception 都加上 {REQUEST_URL} 变量
```
