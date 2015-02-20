# -*- coding: utf-8 -*-

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

    def get(self, key):
        now = time()
        for k in self.cache.keys():
            (timeout, value) = self.cache[k]
            if timeout and now >= timeout:
                del self.cache[k]

        return self.cache.get(key, (0, None))[1]

    def set(self, key, value, expire=0, min_compress_len=0):
        timeout = 0
        if expire != 0:
            timeout = time() + expire
        self.cache[key] = (timeout, value)
        return True

    def add(self, key, value, expire=0, min_compress_len=0):
        if self.get(key) is not None:
            return False
        return self.set(key, value, expire, min_compress_len)

    def incr(self, key, delta=1):
        value = self.get(key)
        if value is None:
            return None
        new_value = int(value) + delta
        self.cache[key] = (self.cache[key][0], new_value)
        return new_value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]
