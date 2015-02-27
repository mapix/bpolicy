# -*- coding: utf-8 -*-

import sys
import os.path
import unittest
from mock import patch, Mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from bpolicy import GenerationedPolicy, GenerationedPolicyFactory, FakeStore, PolicyError, HOUR


class TestGenerationedPolicy(unittest.TestCase):

    def setUp(self):
        self.identity = 'test_generationed_identity'
        self.store = FakeStore()
        self.factory = GenerationedPolicyFactory(quota=100, interval=1 * HOUR, discount=0.5, max_keep_traking=2, store=self.store)
        self.next_policy = Mock()
        self.policy = self.factory.instance(self.next_policy)

    @patch.object(GenerationedPolicy, 'get_current_timestamp')
    def test_generationed_policy_exceed(self, get_current_timestamp):
        get_current_timestamp.return_value = self.store._get_current_timestamp()
        for _ in range(self.factory.quota):
            self.policy.check_policy(self.identity)
        self.assertRaises(PolicyError, self.policy.check_policy, self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(int(self.factory.quota * self.factory.discount)):
            self.policy.check_policy(self.identity)
        self.assertRaises(PolicyError, self.policy.check_policy, self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(int(self.factory.quota * self.factory.discount * self.factory.discount)):
            self.policy.check_policy(self.identity)
        self.assertRaises(PolicyError, self.policy.check_policy, self.identity)

        self.store._incr_current_timestamp(self.factory.max_keep_traking * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(min(int(int(self.factory.quota * self.factory.discount * self.factory.discount) / self.factory.quota), self.factory.quota)):
            self.policy.check_policy(self.identity)

        self.store._incr_current_timestamp(self.factory.max_keep_traking * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(min(int(min(int(int(self.factory.quota * self.factory.discount * self.factory.discount) / self.factory.quota), self.factory.quota) / self.factory.discount), self.factory.quota)):
            self.policy.check_policy(self.identity)

        self.store._incr_current_timestamp((self.factory.max_keep_traking + 1 )* HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check_policy(self.identity)
        self.assertRaises(PolicyError, self.policy.check_policy, self.identity)


    @patch.object(GenerationedPolicy, 'get_current_timestamp')
    def test_generationed_policy_not_exceed(self, get_current_timestamp):
        get_current_timestamp.return_value = self.store._get_current_timestamp()
        for _ in range(self.factory.quota):
            self.policy.check_policy(self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check_policy(self.identity)

        self.store._incr_current_timestamp(1 * HOUR)
        get_current_timestamp.return_value = self.store._get_current_timestamp()

        for _ in range(self.factory.quota):
            self.policy.check_policy(self.identity)
        self.assertRaises(PolicyError, self.policy.check_policy, self.identity)

if __name__ == '__main__':
    unittest.main()
