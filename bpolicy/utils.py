# -*- coding: utf-8 -*-

import csv
import IPy
import os.path
from time import time
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


class FakeMC(object):

    def __init__(self, *args, **kwargs):
        self.cache = {}
        self.current_timestamp = int(time())

    def get(self, key):
        self._check_expire()
        return self.cache.get(key, (0, None))[1]

    def set(self, key, value, expire=None, min_compress_len=0):
        timeout = self._get_current_timestamp() + expire if expire else None
        self.cache[key] = (timeout, value)
        return True

    def incr(self, key, delta=1):
        value = self.get(key)
        if value is None:
            return None
        new_value = value + delta
        self.cache[key] = (self.cache[key][0], new_value)
        return new_value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def _clear_cache(self, prefix=''):
        for key in self.cache.keys():
            if key.startswith(prefix):
                del self.cache[key]

    def _check_expire(self):
        for k in self.cache.keys():
            timeout, value = self.cache[k]
            if timeout and self._get_current_timestamp() >= timeout:
                del self.cache[k]

    def _get_current_timestamp(self):
        return self.current_timestamp

    def _set_current_timestamp(self, timestamp):
        self.current_timestamp = timestamp

    def _incr_current_timestamp(self, delta):
        self.current_timestamp += delta


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
