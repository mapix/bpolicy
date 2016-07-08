# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import object

import web
import logging
from datetime import time
from io import StringIO

import memcache
from bpolicy.consts import MINUTE, HOUR
from bpolicy import RatedPolicyFactory, ClockPolicyFactory, GenerationedPolicyFactory
from bpolicy import DEFAULT_LOGGER_FORMATER
from bpolicy import chained_policy, silent_check

store = memcache.Client(['127.0.0.1:9013'])
rated_factory = RatedPolicyFactory(quota=10, interval=1 * MINUTE)
clock_factory = ClockPolicyFactory(start_time=time(hour=1), end_time=time(hour=6), discount=0.3)
generationed_factory = GenerationedPolicyFactory(quota=10, interval=1 * HOUR, discount=0.5, max_keep_traking=3)


class Store(object):

    def __init__(self, store):
        self.store = store

    def get(self, key):
        return self.store.get(key.encode())

    def set(self, key, value, expire=None):
        return self.store.set(key.encode(), value, expire)

    def incr(self, key, step=1):
        return self.store.incr(key.encode(), step)

    def delete(self, key):
        return self.store.delete(key.encode())


def resetup_bpolicy_logger(stream):
    bpolicy_handler = logging.StreamHandler(stream)
    bpolicy_handler.setFormatter(DEFAULT_LOGGER_FORMATER)
    bpolicy_logger = logging.getLogger('bpolicy')
    for handler in bpolicy_logger.handlers:
        bpolicy_logger.removeHandler(handler)
    bpolicy_logger.addHandler(bpolicy_handler)
    bpolicy_logger.setLevel(logging.DEBUG)


def check_policy(identity):
    return silent_check(chained_policy('hello', [generationed_factory, clock_factory, rated_factory], Store(store)), identity)


class HelloBP(object):

    def GET(self):
        web.header('Content-Type', 'text/html')
        stream = StringIO()
        # there is a bug when StringIO encountered logging
        # so reset handlers each request for demonstrate purpose
        resetup_bpolicy_logger(stream)
        identity = web.ctx.env['REMOTE_ADDR']
        output = ''
        if not check_policy(identity):
            output += '<h1>banned !!!!!</h1>'
        else:
            output += '<h1>hello !!!!!</h1>'
        output += '<p> IPAdress : %s' % identity
        logger_data = stream.getvalue()
        return output + '<br>' + '<div style="background-color:#000;color:red;padding:10px">' + '<br>'.join(logger_data.split('\n')) + '</div>'


urls = ("/", "HelloBP")
app = web.application(urls, globals())


if __name__ == "__main__":
    app.run()
