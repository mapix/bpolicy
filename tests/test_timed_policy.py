# -*- coding: utf-8 -*-

import sys
import os.path
import unittest
from mock import patch, Mock
from datetime import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import TimedPolicy, TimedPolicyFactory


class TestTimedPolicy(unittest.TestCase):

    def setUp(self):
        self.identity = 'test_timed_identity'
        self.factory = TimedPolicyFactory(start_time=time(hour=0), end_time=time(hour=6), discount=0.4)
        self.next_policy = Mock()
        self.policy = self.factory.instance(self.next_policy)

    @patch.object(TimedPolicy, 'get_current_time')
    def test_timed_policy_hit(self, get_current_time):
        get_current_time.return_value = time(hour=3)
        self.policy.check_policy(self.identity)
        assert self.next_policy.discount_quota.called is True
        assert self.next_policy.check_policy.called is True
        self.next_policy.discount_quota.assert_called_with(0.4)
        self.next_policy.check_policy.assert_called_with(self.identity)

    @patch.object(TimedPolicy, 'get_current_time')
    def test_timed_policy_unhit(self, get_current_time):
        get_current_time.return_value = time(hour=10)
        self.policy.check_policy(self.identity)
        assert self.next_policy.discount_quota.called is False
        assert self.next_policy.check_policy.called is True
        self.next_policy.check_policy.assert_called_with(self.identity)

    def test_discount_next_policy(self):
        self.policy.discount_quota(0.1)
        assert self.next_policy.discount_quota.called is True
        self.next_policy.discount_quota.assert_called_with(0.1)


if __name__ == '__main__':
    unittest.main()
