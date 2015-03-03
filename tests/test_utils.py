# -*- coding: utf-8 -*-

import sys
import os.path
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy.utils import is_cernet_ipaddr, is_private_ipaddr, is_valid_ipaddr


class TestUtils(unittest.TestCase):

    def test_is_cernet_ipaddr(self):
        # 210.32.200.89 中国浙江杭州 浙江工业大学 教育网
        assert is_cernet_ipaddr('210.32.200.89') is True
        # 166.111.4.100 中国北京 清华大学 教育网
        assert is_cernet_ipaddr('166.111.4.100') is True
        # 202.119.160.5 中国南京 南京工程学院 教育网
        assert is_cernet_ipaddr('202.119.160.5') is True
        # 124.205.66.195 中国北京 鹏博士/联通
        assert is_cernet_ipaddr('124.205.66.195') is False


    def test_is_private_ipaddr(self):
        assert is_private_ipaddr('N/A') is None
        assert is_private_ipaddr('10.0.2.15') is True
        assert is_private_ipaddr('192.168.0.100') is True
        assert is_private_ipaddr('124.205.66.195') is False


    def test_is_valid_ipaddr(self):
        assert is_valid_ipaddr('') is False
        assert is_valid_ipaddr('N/A') is False
        assert is_valid_ipaddr('unknow') is False
        assert is_valid_ipaddr('10.0.2.15') is True
        assert is_valid_ipaddr('124.205.66.195') is True


if __name__ == '__main__':
    unittest.main()
