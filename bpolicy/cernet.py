# -*- coding: utf-8 -*-

import csv
import IPy
import os.path

from .consts import POLICY_KIND
from .base import Policy, PolicyFactory


class CERNetPolicy(Policy):

    kind = POLICY_KIND.CERNET

    def __init__(self, factory, next_policy=None):
        self.discount = factory.discount
        super(CERNetPolicy, self).__init__(factory, next_policy)

    def is_cernet_ipaddr(self, ipstr):
        try:
            return IPy.IP(ipstr) in self.factory.cernet_nets_set
        except ValueError:
            pass

    def check_policy(self, identity):
        if not self.is_cernet_ipaddr(identity):
            self.discount_quota(self.discount)
        super(CERNetPolicy, self).check_policy(identity)


class CERNetPolicyFactory(PolicyFactory):

    policy_class = CERNetPolicy

    def __init__(self, discount):
        self.discount = discount
        cernet_resource = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/cernet_ip.csv')
        cernet_nets = [r[0] for r in csv.reader(open(cernet_resource), delimiter='\t')]
        self.cernet_nets_set = IPy.IPSet([IPy.IP('%s/%s' % (ip_net, (ip_net.count('.') + 1) * 8), make_net=True) for ip_net in cernet_nets])
