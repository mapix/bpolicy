# -*- coding: utf-8 -*-


from .consts import POLICY_KIND
from .error import PolicyError
from .base import Policy, PolicyFactory


class RatedPolicy(Policy):

    kind = POLICY_KIND.RATED

    def __init__(self, factory, next_policy=None):
        self.quota = factory.quota
        super(RatedPolicy, self).__init__(factory, next_policy)

    def discount_quota(self, discount):
        self.quota = self.quota * discount
        super(RatedPolicy, self).discount_quota(discount)

    def check_policy(self, identity):
        mc_key = self._gen_memcache_key(self.factory.mc_prefix, identity)
        current_counter = self.factory.mc_client.get(mc_key)
        if current_counter is None:
            current_counter = 1
            self.factory.mc_client.set(mc_key, 1, self.factory.interval)
        else:
            current_counter += 1
            self.factory.mc_client.incr(mc_key, 1)
        if current_counter > self.quota:
            raise PolicyError(self, 'max quota exceed')
        super(RatedPolicy, self).check_policy(identity)


class RatedPolicyFactory(PolicyFactory):

    policy_class = RatedPolicy

    def __init__(self, interval, quota, mc_client, mc_prefix=''):
        self.interval = interval
        self.quota = quota
        self.mc_client = mc_client
        self.mc_prefix = mc_prefix
