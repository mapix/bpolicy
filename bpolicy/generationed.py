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
        origin_quota = self.quota
        self.quota = int(self.quota * discount)
        self.logger.debug('discount current quota from %s to %s', origin_quota, self.quota)
        super(GenerationedPolicy, self).discount_quota(discount)

    def get_current_timestamp(self):
        return int(time.time())

    def check_policy(self, identity):
        stats_store_key = self._gen_store_key(self.factory.store_prefix, identity)
        current_discount, current_counter, current_timestamp = (1, 1, self.get_current_timestamp())
        latest_discount, latest_counter, latest_timestamp = self.factory.store.get(stats_store_key) or (current_discount, current_counter - 1, current_timestamp)
        latest_period, current_period = latest_timestamp // self.factory.interval, current_timestamp // self.factory.interval

        if latest_period == current_period:
            current_counter = latest_counter + 1
            current_discount = latest_discount
            self.logger.debug('incr current_counter from %s to %s, keep current_discount %s', current_counter - 1, current_counter, current_discount)
        elif current_period - latest_period < self.factory.max_keep_traking:
            current_discount = latest_discount * self.factory.discount if latest_counter > self.quota * latest_discount else latest_discount / self.factory.discount
            current_discount = min(current_discount, 1)
            self.logger.debug('max_keep_traking encountered, current_discount to %s', current_discount)
        else:
            self.logger.debug('initial a new generation')

        self.factory.store.set(stats_store_key, (current_discount, current_counter, current_timestamp), self.factory.interval * self.factory.max_keep_traking)

        if current_counter > self.quota * current_discount:
            self.logger.debug('max quota encountered: %s / %s', current_counter, self.quota * current_discount)
            raise PolicyError(self, 'max quota exceed')

        super(GenerationedPolicy, self).check_policy(identity)


class GenerationedPolicyFactory(PolicyFactory):

    policy_class = GenerationedPolicy

    def __init__(self, quota, interval, discount, max_keep_traking, store, store_prefix=''):
        self.quota = quota
        self.interval = interval
        self.discount = discount
        self.max_keep_traking = max_keep_traking
        self.store = store
        self.store_prefix = store_prefix
