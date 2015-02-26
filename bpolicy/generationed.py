# -*- coding: utf-8 -*-


import time

from .consts import POLICY_KIND
from .error import PolicyError
from .base import Policy, PolicyFactory


class GenerationedPolicy(Policy):

    kind = POLICY_KIND.GENERATIONED

    def __init__(self, factory, next_policy=None):
        self.quota = factory.quota
        super(GenerationedPolicy, self).__init__(factory, next_policy)

    def discount_quota(self, discount):
        self.quota = self.quota * discount
        super(GenerationedPolicy, self).discount_quota(discount)

    def get_current_timestamp(self):
        return int(time.time())

    def check_policy(self, identity):
        stats_mc_key = self._gen_memcache_key(self.factory.mc_prefix, identity)
        current_discount, current_counter, current_timestamp = (1, 1, self.get_current_timestamp())
        latest_discount, latest_counter, latest_timestamp = self.factory.mc_client.get(stats_mc_key) or (current_discount, current_counter - 1, current_timestamp)
        latest_period, current_period = latest_timestamp // self.factory.interval, current_timestamp // self.factory.interval

        if latest_period == current_period:
            current_counter = latest_counter + 1
            current_discount = latest_discount
        elif current_period - latest_period < self.factory.max_keep_traking:
            current_discount = latest_discount * self.factory.discount if latest_counter > self.quota * latest_discount else latest_discount / self.factory.discount
            current_discount = min(current_discount, 1)

        self.factory.mc_client.set(stats_mc_key, (current_discount, current_counter, current_timestamp), self.factory.interval * self.factory.max_keep_traking)

        if current_counter > self.quota * current_discount:
            raise PolicyError(self, 'max quota exceed')

        super(GenerationedPolicy, self).check_policy(identity)


class GenerationedPolicyFactory(PolicyFactory):

    policy_class = GenerationedPolicy

    def __init__(self, quota, interval, discount, max_keep_traking, mc_client, mc_prefix=''):
        self.quota = quota
        self.interval = interval
        self.discount = discount
        self.max_keep_traking = max_keep_traking
        self.mc_client = mc_client
        self.mc_prefix = mc_prefix
