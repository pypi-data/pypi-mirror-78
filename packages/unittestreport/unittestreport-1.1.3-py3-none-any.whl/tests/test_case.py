"""
============================
Author:柠檬班-木森
Time:2020/8/19   17:46
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
# from unittestreport import ddt, data

import unittest

from unittestreport.core.dataDriver import ddt, list_data,json_data,yaml_data


@ddt
class TestClass(unittest.TestCase):
    cases = [{'case_id': 1, 'title': '用例1', 'data': '用例参数', 'expected': '预期结果'},
             {'case_id': 2, 'title': '用例2', 'data': '用例参数', 'expected': '预期结果'},
             {'case_id': 3, 'title': '用例3', 'data': '用例参数', 'expected': '预期结果'}]

    # @list_data(cases)
    # def test_case(self, data):
    #     pass

    @json_data("cases.json")
    def test_case01(self, data):
        print(data)

    # @yaml_data("cases.yaml")
    # def test_case02(self, data):
    #     pass
    #

# class TestClass(unittest.TestCase):
#
#     def test_case_01(self):
#         a = 100
#         b = 99
#         assert a == b
#
#     def test_case_02(self):
#         a = 100
#         b = 100
#         assert a == b
#
#     def test_case_03(self):
#         a = 100
#         b = 101
#         assert a == b
#
#     @data(1, 2, 3, 4, 5)
#     def test_01case(self,i):
#         assert 100 == 100
