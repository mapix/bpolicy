# -*- coding: utf-8 -*-

import sys
import os.path
import unittest
from datetime import time as datetime_time
from mock import patch, Mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import MINUTE, HOUR
from bpolicy import FakeStore, PolicyError, TimedPolicy
from bpolicy import GenerationedPolicyFactory, RatedPolicyFactory, TimedPolicyFactory, CERNetPolicyFactory


class TestCombinedPolicy(unittest.TestCase):

    def setUp(self):
        self.store = FakeStore()
        self.mock_policy = Mock()
        self.cernet_policy_factory = CERNetPolicyFactory(discount=0.5)
        self.rated_policy_factory = RatedPolicyFactory(interval=10 * MINUTE, quota=10, store=self.store)
        self.timed_policy_factory = TimedPolicyFactory(start_time=datetime_time(hour=0), end_time=datetime_time(hour=6), discount=0.4)
        self.generationed_policy_factory = GenerationedPolicyFactory(quota=100, interval=1 * HOUR, discount=0.5, max_keep_traking=2, store=self.store)

    @patch.object(TimedPolicy, 'get_current_time')
    def test_timed_and_rated_policy(self, get_current_time):
        get_current_time.return_value = datetime_time(hour=8)
        identity = 'test_timed_and_rated'
        rated_policy = self.rated_policy_factory.instance()
        timed_policy = self.timed_policy_factory.instance(rated_policy)
        for _ in range(self.rated_policy_factory.quota):
            timed_policy.check_policy(identity)
        self.assertRaises(PolicyError, timed_policy.check_policy, identity)
        self.assertRaises(PolicyError, timed_policy.check_policy, identity)

        self.store._incr_current_timestamp(self.rated_policy_factory.interval)
        get_current_time.return_value = datetime_time(hour=4)
        for _ in range(int(self.rated_policy_factory.quota * self.timed_policy_factory.discount)):
            _rated_policy = self.rated_policy_factory.instance()
            timed_policy = self.timed_policy_factory.instance(_rated_policy)
            timed_policy.check_policy(identity)
        _rated_policy = self.rated_policy_factory.instance()
        timed_policy = self.timed_policy_factory.instance(_rated_policy)
        self.assertRaises(PolicyError, timed_policy.check_policy, identity)

    def test_combined_check_policy_run_through(self):
        identity = '202.102.154.3'
        rated_policy = self.rated_policy_factory.instance(self.mock_policy)
        generationed_policy = self.generationed_policy_factory.instance(rated_policy)
        timed_policy = self.timed_policy_factory.instance(generationed_policy)
        cernet_policy = self.cernet_policy_factory.instance(timed_policy)

        cernet_policy.check_policy(identity)
        assert self.mock_policy.check_policy.called is True
        self.mock_policy.check_policy.assert_called_with(identity)

        cernet_policy.discount_quota(0.1)
        assert self.mock_policy.discount_quota.called is True
        self.mock_policy.discount_quota.assert_called_with(0.1)


if __name__ == '__main__':
    unittest.main()
