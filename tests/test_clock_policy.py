# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os.path
import unittest
from mock import patch, Mock
from datetime import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import ClockPolicy, ClockPolicyFactory


class TestClockPolicy(unittest.TestCase):

    def setUp(self):
        self.identity = 'test_clock_identity'
        self.factory = ClockPolicyFactory(start_time=time(hour=0), end_time=time(hour=6), discount=0.4)
        self.next_policy = Mock()
        self.store = Mock()
        self.policy = self.factory.instance('', self.store, self.next_policy)

    @patch.object(ClockPolicy, '_get_current_time')
    def test_timed_policy_hit(self, _get_current_time):
        _get_current_time.return_value = time(hour=3)
        self.policy.check(self.identity)
        assert self.next_policy.discount.called is True
        assert self.next_policy.check.called is True
        self.next_policy.discount.assert_called_with(0.4)
        self.next_policy.check.assert_called_with(self.identity)

    @patch.object(ClockPolicy, '_get_current_time')
    def test_timed_policy_unhit(self, _get_current_time):
        _get_current_time.return_value = time(hour=10)
        self.policy.check(self.identity)
        assert self.next_policy.discount.called is False
        assert self.next_policy.check.called is True
        self.next_policy.check.assert_called_with(self.identity)

    def test_discount_next_policy(self):
        self.policy.discount(0.1)
        assert self.next_policy.discount.called is True
        self.next_policy.discount.assert_called_with(0.1)


if __name__ == '__main__':
    unittest.main()
