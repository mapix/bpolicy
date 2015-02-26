# -*- coding: utf-8 -*-

import sys
import os.path
import unittest
from mock import Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import CERNetPolicyFactory


class TestCERNetPolicy(unittest.TestCase):

    def setUp(self):
        self.next_policy = Mock()
        self.factory = CERNetPolicyFactory(discount=0.5)
        self.policy = self.factory.instance(self.next_policy)

    def test_cernet_policy_hit(self):
        # 210.32.200.89 中国浙江杭州 浙江工业大学 教育网
        identity = '210.32.200.89'
        self.policy.check_policy(identity)
        assert self.next_policy.discount_quota.called is False
        assert self.next_policy.check_policy.called is True
        self.next_policy.check_policy.assert_called_with(identity)

    def test_policy_unhit(self):
        # 124.205.66.195 中国北京 鹏博士/联通
        identity = '124.205.66.195'
        self.policy.check_policy(identity)
        assert self.next_policy.discount_quota.called is True
        assert self.next_policy.check_policy.called is True
        self.next_policy.discount_quota.assert_called_with(0.5)
        self.next_policy.check_policy.assert_called_with(identity)


if __name__ == '__main__':
    unittest.main()
