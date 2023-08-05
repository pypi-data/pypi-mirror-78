import os
import platform
import unittest
from x_sweetest import Autotest
from atp.common_read_write import write_data, read_data


class ExecTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        case_data = read_data('./run_case_data.json', 'json', 'r')
        cls.plan_name = case_data.get('test_name', '')
        cls.test_type = case_data.get('test_type', '')

    def test_run(self):
        """测试主方法"""
        global msg
        # 环境配置信息
        if os.path.exists('testcase/' + self.plan_name + '-TestCase.xlsx'):
            # 获取测试配置
            if self.test_type.lower() == 'api':
                # API测试配置参数
                desired_caps = {'platformName': 'api'}
            else:
                sys_name = platform.system()
                if sys_name == 'Linux':
                    # Linux平台下web测试配置参数
                    desired_caps = {'platformName': 'Desktop', 'browserName': 'Chrome', 'headless': True}
                else:
                    # 非linux平台下web测试配置参数
                    desired_caps = {'platformName': 'Desktop', 'browserName': 'Chrome'}
            # 通过X-Sweetest执行自动化测试
            server_url = ''
            # 测试用例集文件里的Sheet表单名称
            sheet_name = '*'
            msg = '执行测试所需数据准备正常'
        else:
            desired_caps = {}
            server_url = ''
            sheet_name = ''
            msg = '未获取有效执行数据'
        # 通过X-Sweetest执行自动化测试，初始化自动化实例
        sweet = Autotest(self.plan_name, sheet_name, desired_caps, server_url)
        # 执行自动化测试
        sweet.plan()
        # 创建并写入测试详情文件
        write_data('details/details.txt', sweet.report_data, 'json', 'w+')

    @classmethod
    def tearDownClass(cls):
        # 写入执行完成状态，数据处理模块确认状态后上传报告
        write_data('./run_case_data.json', {'status': True, 'msg': msg}, flag='json', mode='w+')


if __name__ == '__main__':
    unittest.main()
