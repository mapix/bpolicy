# -*- coding: utf-8 -*-

import csv
import IPy
import os.path
from .error import PolicyError


def chained_policy(*factories):
    policy = None
    for factory in factories:
        policy = factory.instance(policy)
    return policy


def silent_check(policy, identity):
    success = True
    try:
        policy.check_policy(identity)
    except PolicyError:
        success = False
    return success


class memoize(object):

    def __init__ (self, func):
        self.func = func
        self.mem = {}

    def __call__ (self, *args, **kwargs):
        if (args, str(kwargs)) in self.mem:
            result = self.mem[args, str(kwargs)]
        else:
            result = self.func(*args, **kwargs)
            self.mem[args, str(kwargs)] = result
        return result


@memoize
def load_cernet_data():
    cernet_resource = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/cernet_ip.csv')
    cernet_nets = [r[0] for r in csv.reader(open(cernet_resource), delimiter='\t')]
    return IPy.IPSet([IPy.IP('%s/%s' % (ip_net, (ip_net.count('.') + 1) * 8), make_net=True) for ip_net in cernet_nets])


def is_cernet_ipaddr(ipstr):
    try:
        return IPy.IP(ipstr) in load_cernet_data()
    except ValueError:
        pass


def is_private_ipaddr(ipstr):
    try:
        return IPy.IP(ipstr).iptype() == 'PRIVATE'
    except ValueError:
        pass


def is_valid_ipaddr(ipstr):
    success = False
    try:
        IPy.parseAddress(ipstr)
        success = True
    except ValueError:
        pass
    return success
