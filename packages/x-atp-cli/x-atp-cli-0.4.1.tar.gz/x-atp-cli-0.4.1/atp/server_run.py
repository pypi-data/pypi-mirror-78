import os
import sys
import time
import shutil
import json
import platform
import configparser
import requests
import redis
import subprocess
from git import Repo
from atp.common_read_write import write_data, read_data


class ServerRun:
    """
    API自动化测试执行端
    """

    def __init__(self, run_data):
        # 工作空间名
        self.NAME = run_data['name']
        # 平台URL
        self.PLATFORM_URL = run_data['platform_url']
        # 队列IP、队列KEY、队列端口号
        self.REDIS_IP = run_data['redis_ip']
        self.REDIS_KEY = int(run_data['redis_key'])
        self.REDIS_PORT = int(run_data['redis_port'])
        # GIT仓库URL
        self.GIT_URL = run_data['git_url']
        if self.GIT_URL.count('@') - 1 != 0:
            self.GIT_URL = self.GIT_URL.replace('@', '%40', self.GIT_URL.count('@') - 1)
        # 执行端注册ID
        self.EXECUTION_ID = int(run_data['execution_id'])
        # 执行端的类型 web or api
        self.TEST_TYPE = run_data['test_type']
        # 通过队列IP、队列KEY、队列端口号参数连接Redis数据库
        self.POOL = redis.ConnectionPool(host=self.REDIS_IP, port=self.REDIS_PORT, db=self.REDIS_KEY,
                                         decode_responses=True)
        self.REDIS_POOL = redis.Redis(connection_pool=self.POOL)
        # 初始日志文件的起始行号
        self.initial_log_line = 0
        # 初始日志文件的日期前缀
        self.initial_log_time = ''

    @staticmethod
    def mkdir_and_del(src_path):
        """
        删除旧文件夹再创建新文件夹
        """
        if os.path.isdir(src_path):
            shutil.rmtree(src_path)
        os.mkdir(src_path)

    @staticmethod
    def reset_file_tree(file_name, project_name, test_type, test_environment):
        """
        将Git用例仓库里的project_name项目目录中的file_name文件复制到执行目录中
        """
        case_path = os.path.join(os.getcwd(), "git_case")
        lib_dst_path = os.path.join(
            case_path, project_name + "-Project-" + test_type, test_environment, file_name)
        # 确定Git用例存储库中是否有一个lib_dst_path目录
        if os.path.isdir(lib_dst_path):
            lib_src_path = os.path.join(os.getcwd(), file_name)
            # 确定执行目录下是否有一个lib_src_path目录
            if os.path.isdir(lib_src_path):
                shutil.rmtree(lib_src_path)
            shutil.copytree(lib_dst_path, lib_src_path)

    def pull_case(self):
        """
        clone（拉取）和pull（更新）测试用例仓库的内容
        """
        git_case_path = os.path.join(os.getcwd(), "git_case")
        if os.path.isdir(git_case_path):
            print("[%s Server Run Info]> 发现 git_case 目录, 执行更新最新测试用例流程" % self.TEST_TYPE)
            repo = Repo.init(path=git_case_path)
            remote = repo.remote()
            remote.pull()
            print("[%s Server Run Info]> 已更新 GitLab 仓库中 git_case 项目的测试用例" % self.TEST_TYPE)
        else:
            print("[%s Server Run Info]> 找不到 git_case 目录, 执行下载新测试用例流程" % self.TEST_TYPE)
            Repo.clone_from(url=self.GIT_URL, to_path=git_case_path)
            print("[%s Server Run Info]> 已下载 GitLab 仓库中 git_case 项目的测试用例" % self.TEST_TYPE)

    def all_mkdir_copy(self, test_project, test_environment):
        """
        复制指定测试项目、测试类型、测试环境中的相关目录到自动化运行目录下
        """
        ServerRun.reset_file_tree(file_name="lib", project_name=test_project, test_type=self.TEST_TYPE,
                                  test_environment=test_environment)
        ServerRun.reset_file_tree(file_name="data", project_name=test_project, test_type=self.TEST_TYPE,
                                  test_environment=test_environment)
        ServerRun.reset_file_tree(file_name="element", project_name=test_project, test_type=self.TEST_TYPE,
                                  test_environment=test_environment)
        ServerRun.reset_file_tree(file_name="testcase", project_name=test_project, test_type=self.TEST_TYPE,
                                  test_environment=test_environment)
        ServerRun.reset_file_tree(file_name="files", project_name=test_project, test_type=self.TEST_TYPE,
                                  test_environment=test_environment)
        ServerRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "JUnit"))
        ServerRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "report"))
        ServerRun.mkdir_and_del(src_path=os.path.join(os.getcwd(), "details"))

    @staticmethod
    def read_log_file(log_file_list):
        """
        从以日期为维度统计的日志中提取出本次的日志文件，保存至log/new.log
        """
        log_file_dict = {"0": "None"}
        # 用这个变量控制每一行都是不重复的
        previous_row = ''
        # 整理每一行日志
        for i in range(len(log_file_list)):
            # 不读取空行
            if log_file_list[i] == '':
                continue
            # 不读取和上一行重复的数据
            if log_file_list[i] == previous_row:
                continue
            # 判断当前行是否包含特殊分割符
            if ']: #  ' in log_file_list[i]:
                # 将日志信息按用途分类
                log_file_dict[i] = {
                    'time': log_file_list[i][:23],
                    'grade': log_file_list[i][25:log_file_list[i].find(']')],
                    'message': log_file_list[i][log_file_list[i].find(']') + 6:],
                }
            else:
                # 如果是错误信息，上传特殊格式
                log_file_dict[i] = {
                    'time': '',
                    'grade': '',
                    'message': log_file_list[i].replace(' ', '&nbsp;'),
                }
            # 更新上一行的数据
            previous_row = log_file_list[i]
        # 在log目录下写入新的日志文件
        write_data(os.path.join("log", "new.log"), log_file_dict, 'json', 'w+')

    def write_test_data_and_run(self, test_name, test_type):
        """写入测试所需数据并执行测试"""
        run_case_data = {'test_name': test_name, 'test_type': test_type, 'status': False}
        write_data('./run_case_data.json', run_case_data, 'json', 'w+')
        sys_name = platform.system()
        if sys_name == 'Linux':
            # 启动run_case模块
            popen = subprocess.Popen('nohup python3 ./exec_testcase.py &', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        else:
            # 有的Windows系统中必须有环境变量python3,如果变量无配置python3的则无法启动
            popen = subprocess.Popen('start python3 ./exec_testcase.py', shell=True)
        # 存储超时的报错信息变量
        timeout_msg = ''
        # 隐式等待/避免执行端假死,linux环境下能用，Windows环境下无效
        try:
            popen.wait(timeout=3600)
        except Exception as exc:
            timeout_msg = exc
            popen.kill()
        # 获取标准输出内容
        log_stdout = popen.stdout.read().decode()
        # 将标准输出的每行转化为list的元素
        log_stdout_list = log_stdout.split('\n')
        # 将超时信息加入list元素中
        log_stdout_list.append(str(timeout_msg))
        # 调用日志处理函数，将日志输出到log/new.log
        self.read_log_file(log_file_list=log_stdout_list)

    def post_heartbeat(self, status, localtime=None, task_dict=None, remark=None):
        """
        # 描述:
            发送心跳请求到ATP服务器（失败重试，直至恢复连接）
        # 用法0（第一次）:
            self.post_heartbeat(status=0)
        # 用法1（正常）:
            self.post_heartbeat(status=1, localtime=[调用时间])
        # 用法2（任务无法完成/放弃任务，需要在备注中提交错误信息）:
            self.post_heartbeat(status=2, localtime=[调用时间], task_dict=[任务字典], remark=[备注])
        # 用法3（开始执行任务）:
            self.post_heartbeat(status=3, localtime=[调用时间], task_dict=[任务字典])
        # 用法4（任务执行完成，上传测试报告）:
            self.post_heartbeat(status=4, localtime=[调用时间], task_dict=[任务字典])
        # 用法5（执行端异常，需要在备注中提交异常信息）:
            self.post_heartbeat(status=5, remark=[备注])
        # 用法6（执行端离线）:
            self.post_heartbeat(status=6)
        # 用法7（执行端变更信息，需要在备注中提交变更信息字典字符串）:
            self.post_heartbeat(status=7, remark=[备注])
        """
        if not localtime:
            localtime = time.asctime(time.localtime(time.time()))
        # ATP平台端上执行端心跳的API接口
        heartbeat_api_url = self.PLATFORM_URL + 'software/execution/heartbeat/'
        # 心跳请求连接次数
        connect = 0
        # 开始发送心跳请求（不成功便成仁，真男人从不回头看爆炸）
        while True:
            # 捕获异常
            try:
                # 执行端心跳参数
                up_data = {'id': self.EXECUTION_ID, 'status': status, 'task_dict': json.dumps(task_dict),
                           'remark': remark}
                # 状态为4时，组织待上传的次数报告文件
                if status == 4:
                    # 设置默认日志内容，如果没有生成则上传默认文件内容
                    files_report_obj = read_data(os.path.join('def_report.xlsx'), '', 'rb')
                    files_junit_obj = b'None'
                    files_details_obj = b'None'
                    files_log_obj = b'None'
                    # 如果文件存在则取出XXX-Report@XXXXXX_XXX.xlsx的测试报告文件名
                    for _root, _dirs, files in os.walk(os.path.join('report', task_dict['test_name'])):
                        if files:
                            files_report = files[0]
                            files_report_obj = read_data(os.path.join('report', task_dict['test_name'], files_report),
                                                         '', 'rb')
                    # 如果文件存在则取出XXX-Report@XXXXXX_XXX.xml的测试汇总文件名
                    for _root, _dirs, files in os.walk('JUnit'):
                        if files:
                            files_junit = files[0]
                            files_junit_obj = read_data(os.path.join('JUnit', files_junit), '', 'rb')

                    # 读取测试详情文件
                    if os.path.isfile(os.path.join('details', 'details.txt')):
                        files_details_obj = read_data(os.path.join('details', 'details.txt'), '', 'rb')
                    # 读取测试日志文件
                    if os.path.isfile(os.path.join('log', 'new.log')):
                        files_log_obj = read_data(os.path.join('log', 'new.log'), '', 'rb')
                    # 汇总XXX-Report@XXXXXX_XXX.xlsx、XXX-Report@XXXXXX_XXX.xml、details.txt、new.log文件对象
                    files_obj = {
                        'file_obj': (str(task_dict['queue_id']) + '.xlsx', files_report_obj),
                        'file_obj_junit': (str(task_dict['queue_id']) + '.xml', files_junit_obj),
                        'file_obj_details': (str(task_dict['queue_id']) + '.txt', files_details_obj),
                        'file_obj_log': (str(task_dict['queue_id']) + '.log', files_log_obj)
                    }
                else:
                    files_obj = {}
                # 向ATP平台端发送执行端心跳请求
                requests_data = requests.post(heartbeat_api_url, data=up_data, files=files_obj)
                requests_json = requests_data.json()
                # 判断平台端心跳状态处理结果
                if requests_json['code'] == 200:
                    # 心跳请求响应成功，结束死循环
                    print('[Heartbeat][' + localtime + ']> ' + str(requests_json['data']))
                    break
                # 服务器内部错误错误
                else:
                    print('[Heartbeat Error][' + localtime + ']> > ' + str(requests_json))
            # 网络请求错误
            except Exception as exc:
                print('[Heartbeat Error][' + localtime + ']> ' + str(exc))
            # 30秒后重新发送心跳请求
            time.sleep(30)
            connect += 1
            print('[Heartbeat Error][' + localtime + ']> 进行第 ' + str(connect) + ' 次重新连接')

    def run(self):
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "log"))
        self.mkdir_and_del(src_path=os.path.join(os.getcwd(), "snapshot"))
        self.pull_case()
        print('[%s Server Run Info]> 检测是否有历史任务未完成' % self.TEST_TYPE)
        # 上报第一次/刚启动执行端的心跳
        self.post_heartbeat(status=0)
        while True:
            time.sleep(10)
            try:
                # 获取Redis任务队列的信息长度
                length = self.REDIS_POOL.llen(self.EXECUTION_ID)
                # 生成当前时间字符串，用于打印输出
                localtime = time.asctime(time.localtime(time.time()))
                # 如果Redis任务队列的信息长度小于0，那就说明没有任务
                if length > 0:
                    print('[%s Server Run Info][%s]> 发现新的任务信息' % (self.TEST_TYPE, localtime))
                    self.pull_case()
                    value_dict = json.loads(self.REDIS_POOL.lpop(self.EXECUTION_ID))
                    # 上报开始执行任务的心跳
                    self.post_heartbeat(status=3, localtime=localtime, task_dict=value_dict)
                    try:
                        print('[Queue Task Dict]> ' + str(value_dict))
                        print('[%s Server Run Info]> 重置 X-Sweetest 测试运行环境' % self.TEST_TYPE)
                        self.all_mkdir_copy(test_project=value_dict['test_project'],
                                            test_environment=value_dict['test_environment'])
                        print('[%s Server Run Info]> X-Sweetest 测试运行环境就绪' % self.TEST_TYPE)
                        # 执行sweetest，并返回执行结果
                        self.write_test_data_and_run(test_name=value_dict['test_name'], test_type=self.TEST_TYPE)
                        print('[%s Server Run Info]> X-Sweetest 测试完成并上传测试报告' % self.TEST_TYPE)
                        # 上报任务执行完成的心跳
                        self.post_heartbeat(status=4, localtime=localtime, task_dict=value_dict)
                        print('[%s Server Run Info]> 测试报告上传完毕' % self.TEST_TYPE)
                    except Exception as exc:
                        # 上报任务无法完成的心跳
                        self.post_heartbeat(status=2, localtime=localtime, task_dict=value_dict, remark=str(exc))
                        print('[%s Server Run Error]> ' + str(exc) % self.TEST_TYPE)
                else:
                    # 上报正常的心跳
                    self.post_heartbeat(status=1, localtime=localtime)
                # 调用Flush，从内存中刷入日志文件
                sys.stdout.flush()
            except Exception as exc:
                # 上报执行端异常的心跳
                self.post_heartbeat(status=5, remark=str(exc))
                print('[%s Server Run Error]> ' + str(exc) % self.TEST_TYPE)


if __name__ == '__main__':
    # 读取工作空间目录下的config配置文件
    config_file = 'config.ini'
    config = configparser.RawConfigParser()
    config.read(config_file, encoding='utf-8')
    # 读取配置中的ATP-Server内容
    data = dict(config.items('ATP-Server'))
    # 创建自动化测试执行端对象
    r = ServerRun(run_data=data)
    # 启动API自动化测试执行端
    r.run()
