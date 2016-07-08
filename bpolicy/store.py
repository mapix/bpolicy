# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import object

from time import time


class Store(object):

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, expire=None):
        raise NotImplementedError

    def incr(self, key, step=1):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class FakeStore(Store):

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

    def incr(self, key, step=1):
        value = self.get(key)
        if value is None:
            return None
        new_value = value + step
        self.cache[key] = (self.cache[key][0], new_value)
        return new_value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def _clear_cache(self, prefix=''):
        for key in list(self.cache.keys()):
            if key.startswith(prefix):
                del self.cache[key]

    def _check_expire(self):
        for k in list(self.cache.keys()):
            timeout, value = self.cache[k]
            if timeout and self._get_current_timestamp() >= timeout:
                del self.cache[k]

    def _get_current_timestamp(self):
        return self.current_timestamp

    def _set_current_timestamp(self, timestamp):
        self.current_timestamp = timestamp

    def _incr_current_timestamp(self, step):
        self.current_timestamp += step
