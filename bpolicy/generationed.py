# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from past.utils import old_div
import time

from .consts import POLICY_KIND
from .error import PolicyError
from .base import Policy, PolicyFactory


class GenerationedPolicy(Policy):

    kind = POLICY_KIND.GENERATIONED

    def __init__(self, *args, **kwargs):
        super(GenerationedPolicy, self).__init__(*args, **kwargs)
        self.quota = self.factory.quota

    def discount(self, discount):
        origin_quota = self.quota
        self.quota = int(self.quota * discount)
        self.logger.debug('discount current quota from %s to %s', origin_quota, self.quota)
        super(GenerationedPolicy, self).discount(discount)

    def _get_current_timestamp(self):
        return int(time.time())

    def check(self, identity):
        key = self._gen_key(identity)
        current_discount, counter, current_timestamp = (1, 1, self._get_current_timestamp())
        latest_discount, latest_counter, latest_timestamp = self.store.get(key) or (current_discount, counter - 1, current_timestamp)
        latest_period, current_period = latest_timestamp // self.factory.interval, current_timestamp // self.factory.interval

        if latest_period == current_period:
            counter = latest_counter + 1
            current_discount = latest_discount
            self.logger.debug('incr counter from %s to %s, keep current_discount %s', counter - 1, counter, current_discount)
        elif current_period - latest_period < self.factory.max_keep_traking:
            current_discount = latest_discount * self.factory.discount if latest_counter > self.quota * latest_discount else old_div(latest_discount, self.factory.discount)
            current_discount = min(current_discount, 1)
            self.logger.debug('max_keep_traking encountered, current_discount to %s', current_discount)
        else:
            self.logger.debug('initial a new generation')

        self.store.set(key, (current_discount, counter, current_timestamp), self.factory.interval * self.factory.max_keep_traking)

        if counter > self.quota * current_discount:
            self.logger.debug('max quota encountered: %s / %s', counter, self.quota * current_discount)
            raise PolicyError(self, 'max quota exceed')

        super(GenerationedPolicy, self).check(identity)


class GenerationedPolicyFactory(PolicyFactory):

    policy_class = GenerationedPolicy

    def __init__(self, quota, interval, discount, max_keep_traking):
        self.quota = quota
        self.interval = interval
        self.discount = discount
        self.max_keep_traking = max_keep_traking
