import re
import sys
import os
import uuid
import json
import zipfile
import argparse
import platform
import requests
import subprocess
import configparser
from pathlib import Path
from atp.server import workspace, copy_file, daemon_start


def main():
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(description='X ATP CLI Client (X 自动化测试平台命令行客户端)')
    parser.add_argument('-v', '--version', help='输出客户端版本信息', action='version', version='%(prog)s v0.4.1')
    parser.add_argument('-d', '--demo', help='在当前目录下创建 `x_sweetest_example` 项目',
                        action='store_true')
    parser.add_argument('-r', '--run', dest='atp_server_url',
                        help='运行 X-ATP 自动测试执行端服务 (E.g x-atp-cli -r http://127.0.0.1 -t api -n 执行端001)',
                        action='store')
    parser.add_argument('-t', '--type', dest='test_type', help='测试执行端类型 api|web (与 -r 配合使用)',
                        action='store')
    parser.add_argument('-n', '--name', dest='workspace_name', help='执行端工作区的标识名称 (与 -r 配合使用)',
                        action='store', default='')
    parser.add_argument('-u', '--updata', dest='updata_cli',
                        help='更新指定目录下执行端，config.ini不变（E.g x-atp-cli -u /usr/执行端001)',
                        action='store', default='')
    parser.add_argument('-s', '--start', dest='start_cli',
                        help='根据指定目录下的config.ini启动执行端，如果同名执行端已经执行会先结束执行端进程，再重新启动（E.g x-atp-cli -s /usr/执行端001)',
                        action='store', default='')
    args = parser.parse_args()

    if args.demo:
        x_sweetest_dir = Path(__file__).resolve().parents[0]
        example_dir = x_sweetest_dir / 'example' / 'x_sweetest_example.zip'
        extract(str(example_dir), Path.cwd())
        print('成功创建 `x_sweetest_example` 项目\n' +
              '快速体验, 请输入以下命令 (进入演示目录并开始运行脚本):\n\n' +
              'cd x_sweetest_example\npython echo.py\n')

    if args.atp_server_url:
        if not re.match(r'(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?',
                        args.atp_server_url,
                        re.IGNORECASE):
            print('[Cli Error]> 这不是有效的URl地址')
            return
        if args.test_type.lower() in ('api', 'web'):
            data_json = get_initialization(test_type=args.test_type.lower(), atp_server_url=args.atp_server_url,
                                           workspace_name=args.workspace_name)
            workspace(sys_name=platform.system(), data=data_json['data'])
        else:
            print('[Cli Error]> 缺少 -t api|web 参数')

    if args.updata_cli:
        # 获取工作路径和当前文件路径
        work_space = Path(args.updata_cli)
        current_path = os.path.abspath(__file__)
        current_dir = Path(os.path.dirname(current_path))
        # 更新最新代码到工作目录
        copy_file(current_dir=current_dir, work_space=work_space)
        print('### 目录 ###\n %s \n### 文件下代码文件已更新 ###' % work_space)

    if args.start_cli:
        # 判断输入的目录路径是否正确
        if os.path.isdir(args.start_cli):
            # 如果是linux平台，则先关闭执行端，再重启
            if platform.system() == 'Linux':
                # 获取执行端名称
                cli_name = args.start_cli.split('/')[-1][13:]
                # 关闭指定执行机的shell指令，关闭PPID为1的孤儿进程。
                cmd = 'ps -ef|grep ' + cli_name + '|grep -v grep|awk \'$3 == 1{print $2}\'|xargs -i kill -9 {}'
                # 执行指令，并获取执行结果
                popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                # 等待执行结束
                try:
                    popen.wait(timeout=5)
                    # 获取工作目录
                    work_space = Path(args.start_cli)
                    # 读取工作目录下的配置文件
                    config = configparser.RawConfigParser()
                    config.read(work_space / 'config.ini', encoding='utf-8')
                    data = dict(config.items('ATP-Server'))
                    # 启动执行端
                    daemon_start(data=data, work_space=work_space)
                    print('###  执行端 %s 成功运行  ###' % cli_name)
                except Exception as exc:
                    popen.kill()
                    print(exc)
            else:
                print(
                    "### 检测到您的操作系统不支持 -s 参数指令 ###\n 请执行： x-atp-cli -u %s 更新执行端目录下代码\n再手动启动执行端：python server_run.py" % args.start_cli)
        else:
            print("### %s 目录不存在，请输入正确的执行端目录的绝对路径 ###")


def extract(z_file, path):
    """
    解压缩文件到指定目录
    """
    f = zipfile.ZipFile(z_file, 'r')
    for file in f.namelist():
        f.extract(file, path)


def get_initialization(test_type, atp_server_url, workspace_name):
    # 对输入的URL做判断，末尾没加"/" 统一处理加上"/"
    if not atp_server_url.endswith('/'):
        atp_server_url += '/'
    # ATP平台端初始化执行端的API接口
    initialization_api_url = atp_server_url + 'software/execution/initialization/'
    # 如果执行工作区名称为默认值，生成随机数
    if workspace_name == '':
        # 根据当前网卡和时间组成随机数
        workspace_name = uuid.uuid4().hex
    # api、web执行端的向平台注册的通用参数
    type_data = {'api': 0, 'web': 3}
    up_data = {'name': workspace_name, 'execution_type': type_data[test_type],
               'information': json.dumps({'system': platform.system()})}
    # 向ATP平台端发送初始化执行端请求
    requests_data = requests.post(initialization_api_url, data=up_data)
    requests_json = requests_data.json()
    print('[Cli info]> ' + str(requests_json))
    # 判断平台端初始化结果
    if requests_json['code'] != 200:
        print('[Cli Error]> 执行端服务初始化失败')
        sys.exit()
    # 附带上经过上面处理的ATP平台URl
    requests_json['data']['platform_url'] = atp_server_url
    # 加上测试类型
    requests_json['data']['test_type'] = test_type
    return requests_json


if __name__ == '__main__':
    main()
