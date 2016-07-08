# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import range

import sys
import os.path
import unittest
from mock import Mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import RatedPolicyFactory, PolicyError, MINUTE, FakeStore


class TestRatedPolicy(unittest.TestCase):

    def setUp(self):
        self.store = FakeStore()
        self.next_policy = Mock()
        self.factory = RatedPolicyFactory(interval=10 * MINUTE, quota=10)
        self.policy = self.factory.instance('', self.store, self.next_policy)
        self.identity = 'test_rated_policy_identity'

    def test_rated_policy_quota_exceed(self):
        for _ in range(self.factory.quota):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)

    def test_rated_policy_interval_expired(self):
        for _ in range(self.factory.quota):
            self.policy.check(self.identity)
        self.store._incr_current_timestamp(1 * MINUTE)
        for _ in range(self.factory.quota):
            self.assertRaises(PolicyError, self.policy.check, self.identity)
        self.store._incr_current_timestamp(9 * MINUTE)
        for _ in range(self.factory.quota):
            self.policy.check(self.identity)

    def test_discount_next_policy(self):
        self.policy.discount(0.1)
        assert self.next_policy.discount.called is True
        self.next_policy.discount.assert_called_with(0.1)

if __name__ == '__main__':
    unittest.main()
