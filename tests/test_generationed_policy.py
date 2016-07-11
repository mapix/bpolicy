# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from builtins import range
from past.utils import old_div
import unittest
from mock import patch, Mock

from bpolicy import GenerationedPolicy, GenerationedPolicyFactory, FakeStore, PolicyError, HOUR


class TestGenerationedPolicy(unittest.TestCase):

    def setUp(self):
        self.identity = 'test_generationed_identity'
        self.store = FakeStore()
        self.factory = GenerationedPolicyFactory(quota=100, interval=1 * HOUR, discount=0.5, max_keep_traking=2)
        self.next_policy = Mock()
        self.policy = self.factory.instance('', self.store, self.next_policy)

    @patch.object(GenerationedPolicy, '_get_current_timestamp')
    def test_generationed_policy_exceed(self, _get_current_timestamp):
        _get_current_timestamp.return_value = self.store._get_current_timestamp()
        for _ in range(self.factory.quota):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(int(self.factory.quota * self.factory.discount)):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(int(self.factory.quota * self.factory.discount * self.factory.discount)):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)

        self.store._incr_current_timestamp(self.factory.max_keep_traking * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(min(int(old_div(int(self.factory.quota * self.factory.discount * self.factory.discount), self.factory.quota)), self.factory.quota)):
            self.policy.check(self.identity)

        self.store._incr_current_timestamp(self.factory.max_keep_traking * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(min(int(old_div(min(int(old_div(int(self.factory.quota * self.factory.discount * self.factory.discount), self.factory.quota)), self.factory.quota), self.factory.discount)), self.factory.quota)):
            self.policy.check(self.identity)

        self.store._incr_current_timestamp((self.factory.max_keep_traking + 1 )* HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)


    @patch.object(GenerationedPolicy, '_get_current_timestamp')
    def test_generationed_policy_not_exceed(self, _get_current_timestamp):
        _get_current_timestamp.return_value = self.store._get_current_timestamp()
        for _ in range(self.factory.quota):
            self.policy.check(self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check(self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        _get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check(self.identity)
        self.assertRaises(PolicyError, self.policy.check, self.identity)

if __name__ == '__main__':
    unittest.main()
