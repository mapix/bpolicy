# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .consts import POLICY_KIND
from .error import PolicyError
from .base import Policy, PolicyFactory


class RatedPolicy(Policy):

    kind = POLICY_KIND.RATED

    def __init__(self, *args, **kwargs):
        super(RatedPolicy, self).__init__(*args, **kwargs)
        self.quota = self.factory.quota

    def discount(self, discount):
        origin_quota = self.quota
        self.quota = int(self.quota * discount)
        self.logger.debug("discount current quota from %s to %s", origin_quota, self.quota)
        super(RatedPolicy, self).discount(discount)

    def check(self, identity):
        key = self._gen_key(identity)
        counter = self.store.get(key)
        if counter is None:
            counter = 1
            self.store.set(key, 1, self.factory.interval)
            self.logger.debug("initial counter to 1 for new interval")
        else:
            counter += 1
            self.store.incr(key, 1)
            self.logger.debug("incr counter from %s to %s", counter, counter + 1)
        if counter > self.quota:
            self.logger.debug("max quota encountered: %s / %s", counter, self.quota)
            raise PolicyError(self, "max quota exceed")
        super(RatedPolicy, self).check(identity)


class RatedPolicyFactory(PolicyFactory):

    policy_class = RatedPolicy

    def __init__(self, interval, quota):
        self.interval = interval
        self.quota = quota
