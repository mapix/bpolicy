# -*- coding: utf-8 -*-

from .consts import POLICY_KIND
from .base import Policy, PolicyFactory
from .utils import load_cernet_data, is_cernet_ipaddr


class CERNetPolicy(Policy):

    kind = POLICY_KIND.CERNET

    def __init__(self, factory, next_policy=None):
        self.discount = factory.discount
        super(CERNetPolicy, self).__init__(factory, next_policy)

    def check_policy(self, identity):
        if is_cernet_ipaddr(identity):
            self.logger.debug('%r is valid cernet ipaddress, silent pass through', identity)
        else:
            self.logger.debug('%r is not valid cernet ipaddress, discount all successor policy quota by %s', identity, self.discount)
            self.discount_quota(self.discount)
        super(CERNetPolicy, self).check_policy(identity)


class CERNetPolicyFactory(PolicyFactory):

    policy_class = CERNetPolicy

    def __init__(self, discount):
        self.discount = discount
        load_cernet_data()
