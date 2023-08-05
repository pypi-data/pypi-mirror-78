import os
import sys
import time
import configparser
import subprocess
from pathlib import Path
from atp.server_run import ServerRun
from atp.common_read_write import write_data, read_data


def workspace(sys_name, data):
    """
    创建自动化测试执行工作空间并自动/手动执行
    """
    data_dict = {
        'name': data['name'],
        'platform_url': data['platform_url'],
        'git_url': data['git_url'],
        'redis_ip': data['redis_ip'],
        'redis_key': data['redis_key'],
        'redis_port': data['redis_port'],
        'execution_id': data['execution_id'],
        'test_type': data['test_type'],
    }
    current_path = os.path.abspath(__file__)
    current_dir = Path(os.path.dirname(current_path))
    cwd_dir = Path.cwd()
    work_space = cwd_dir / ('x_atp_server_%s' % data_dict['name'])
    os.mkdir(str(work_space))
    create_profile(data=data_dict, work_space=work_space, current_dir=current_dir)
    print('\n###执行端目录 x_atp_server_%s 已创建完成 ### ' % data_dict['name'])
    # 启动执行端
    if sys_name == 'Linux':
        cmd = 'x-atp-cli -s ' + str(work_space)
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # 等待shell执行执行完成，此处不等待的话，父程序会直接结束，导致 x-atp-cli -s 的指令PPID变为1，会被kill掉
        popen.wait(timeout=10)
        print("### 执行机 %s 已运行 ### " % data_dict['name'])
    else:
        print("### 您需要手动启动执行端服务 ###python %s/server_run.py\n" % work_space)


def create_profile(data, work_space, current_dir):
    """
    在程序执行的当前目录下创建配置文件和执行程序
    """
    # 处理GIT仓库URL里的特殊字符
    data['git_url'] = data['git_url'].replace('%40', '@')
    config = configparser.ConfigParser()
    # 创建config配置文件
    file = 'config.ini'
    config.read(work_space / file)
    config.add_section('ATP-Server')
    # 平台URL、GIT仓库URL、工作空间名、队列IP、队列KEY、队列端口号、注册ID、测试类型
    config.set('ATP-Server', 'platform_url', data['platform_url'])
    config.set('ATP-Server', 'name', data['name'])
    config.set('ATP-Server', 'git_url', data['git_url'])
    config.set('ATP-Server', 'redis_ip', data['redis_ip'])
    config.set('ATP-Server', 'redis_key', str(data['redis_key']))
    config.set('ATP-Server', 'redis_port', str(data['redis_port']))
    config.set('ATP-Server', 'execution_id', str(data['execution_id']))
    config.set('ATP-Server', 'test_type', str(data['test_type']))
    # 保存config配置文件
    with open(work_space / file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    copy_file(current_dir=current_dir, work_space=work_space)


def copy_file(current_dir, work_space):
    # 拷贝server_run执行文件到工作空间
    file_obj = read_data(current_dir / 'server_run.py', '', 'r')
    write_data(work_space / 'server_run.py', file_obj, 'w+', 'w+')
    # 拷贝自动化测试框架执行文件到工作空间
    file_exec = read_data(current_dir / 'exec_testcase.py', '', 'r')
    write_data(work_space / 'exec_testcase.py', file_exec, 'w+', 'w+')
    # 拷贝默认report报告到工作空间
    file_report = read_data(current_dir / 'def_report.xlsx', '', 'rb')
    write_data(work_space / 'def_report.xlsx', file_report, 'wb', 'w+')


def daemon_start(data, work_space, stdin='/dev/null', stdout='/dev/null', stderr='/var/log/x-atp-api-server.error'):
    """
    启动守护进程
    """
    # fork出一个子进程，父进程退出
    try:
        pid = os.fork()
        # 父进程退出函数
        if pid > 0:
            return
    except OSError as e:
        sys.stderr.write("[Api Server Error]> 第一次 fork 失败, " + e.strerror)
        os._exit(1)
    # 创建日志存放目录，设置日志输出文件
    log_file = Path("atp_log")
    if not log_file.is_dir():
        os.mkdir(str(log_file))
    sys.stdin = open(stdin, 'r')
    sys.stdout = open(stdout, 'a+')
    sys.stderr = open(stderr, 'a+')
    # 等待父进程结束
    time.sleep(2)
    # 父进程退出后，子进程由init收养
    # setsid使子进程成为新的会话首进程和进程组的组长，与原来的进程组、控制终端和登录会话脱离
    os.setsid()
    # 防止在类似于临时挂载的文件系统下运行，例如/mnt文件夹下，这样守护进程一旦运行，临时挂载的文件系统就无法卸载了，所以把目录设置到工作目录下
    os.chdir(work_space)
    # 设置用户创建文件的默认权限，设置的是权限“补码”，这里将文件权限掩码设为0，使得用户创建的文件具有最大的权限。否则，默认权限是从父进程继承得来的
    os.umask(0)
    # 第二次进行fork,为了防止会话首进程意外获得控制终端
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            os._exit(0)
    except OSError as e:
        sys.stderr.write("[Api Server Error]> 第二次 fork 失败, " + e.strerror)
        os._exit(1)
    # 此时改程序已经是守护进程了，再执行需要后台执行的程序即可
    r = ServerRun(data)
    r.run()
