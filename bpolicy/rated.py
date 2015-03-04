# -*- coding: utf-8 -*-

from .consts import POLICY_KIND, DEFAULT_SERVICE
from .error import PolicyError
from .base import Policy, PolicyFactory


class RatedPolicy(Policy):

    kind = POLICY_KIND.RATED

    def __init__(self, factory, next_policy, service):
        self.quota = factory.quota
        super(RatedPolicy, self).__init__(factory, next_policy, service)

    def discount_quota(self, discount):
        origin_quota = self.quota
        self.quota = int(self.quota * discount)
        self.logger.debug('discount current quota from %s to %s', origin_quota, self.quota)
        super(RatedPolicy, self).discount_quota(discount)

    def check_policy(self, identity):
        store_key = self._gen_store_key(self.factory.store_prefix, identity)
        current_counter = self.factory.store.get(store_key)
        if current_counter is None:
            current_counter = 1
            self.factory.store.set(store_key, 1, self.factory.interval)
            self.logger.debug('initial current_counter to 1 for new interval')
        else:
            current_counter += 1
            self.factory.store.incr(store_key, 1)
            self.logger.debug('incr current_counter from %s to %s', current_counter, current_counter + 1)
        if current_counter > self.quota:
            self.logger.debug('max quota encountered: %s / %s', current_counter, self.quota)
            raise PolicyError(self, 'max quota exceed')
        super(RatedPolicy, self).check_policy(identity)


class RatedPolicyFactory(PolicyFactory):

    policy_class = RatedPolicy

    def __init__(self, interval, quota, store, store_prefix='', service=DEFAULT_SERVICE):
        self.interval = interval
        self.quota = quota
        self.store = store
        self.store_prefix = store_prefix
        super(RatedPolicyFactory, self).__init__(service)
