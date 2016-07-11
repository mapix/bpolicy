# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import range

import unittest
from datetime import time as datetime_time
from mock import patch, Mock

from bpolicy import MINUTE, HOUR
from bpolicy import FakeStore, PolicyError, ClockPolicy
from bpolicy import GenerationedPolicyFactory, RatedPolicyFactory, ClockPolicyFactory


class TestCombinedPolicy(unittest.TestCase):

    def setUp(self):
        self.store = FakeStore()
        self.mock_policy = Mock()
        self.rated_policy_factory = RatedPolicyFactory(interval=10 * MINUTE, quota=10)
        self.clock_policy_factory = ClockPolicyFactory(start_time=datetime_time(hour=0), end_time=datetime_time(hour=6), discount=0.4)
        self.generationed_policy_factory = GenerationedPolicyFactory(quota=100, interval=1 * HOUR, discount=0.5, max_keep_traking=2)

    @patch.object(ClockPolicy, '_get_current_time')
    def test_clock_and_rated_policy(self, _get_current_time):
        _get_current_time.return_value = datetime_time(hour=8)
        identity = 'test_clock_and_rated'
        rated_policy = self.rated_policy_factory.instance('', self.store)
        clock_policy = self.clock_policy_factory.instance('', self.store, rated_policy)
        for _ in range(self.rated_policy_factory.quota):
            clock_policy.check(identity)
        self.assertRaises(PolicyError, clock_policy.check, identity)
        self.assertRaises(PolicyError, clock_policy.check, identity)

        self.store._incr_current_timestamp(self.rated_policy_factory.interval)
        _get_current_time.return_value = datetime_time(hour=4)
        for _ in range(int(self.rated_policy_factory.quota * self.clock_policy_factory.discount)):
            _rated_policy = self.rated_policy_factory.instance('', self.store)
            clock_policy = self.clock_policy_factory.instance('', self.store, _rated_policy)
            clock_policy.check(identity)
        _rated_policy = self.rated_policy_factory.instance('', self.store)
        clock_policy = self.clock_policy_factory.instance('', self.store, _rated_policy)
        self.assertRaises(PolicyError, clock_policy.check, identity)


if __name__ == '__main__':
    unittest.main()
