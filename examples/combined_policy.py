# -*- coding: utf-8 -*-

import sys
import os.path
import logging
from datetime import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from bpolicy.consts import MINUTE, HOUR
from bpolicy import FakeStore, chained_policy, silent_check
from bpolicy import RatedPolicyFactory, TimedPolicyFactory, CERNetPolicyFactory, GenerationedPolicyFactory
from bpolicy import DEFAULT_LOGGER_FORMATER

bpolicy_handler = logging.StreamHandler(sys.stdout)
bpolicy_handler.setFormatter(DEFAULT_LOGGER_FORMATER)

bpolicy_logger = logging.getLogger('bpolicy')
bpolicy_logger.addHandler(bpolicy_handler)
bpolicy_logger.setLevel(logging.DEBUG)

store = FakeStore()
rated_factory = RatedPolicyFactory(quota=10, interval=1 * MINUTE, store=store)
timed_factory = TimedPolicyFactory(start_time=time(hour=1), end_time=time(hour=6), discount=0.3)
generationed_factory = GenerationedPolicyFactory(quota=10, interval=1 * HOUR, discount=0.5, max_keep_traking=3, store=store)
cernet_factory = CERNetPolicyFactory(discount=0.9)


def get_policy():
    return chained_policy(rated_factory, generationed_factory, timed_factory, cernet_factory)


if __name__ == '__main__':
    identity = '202.102.154.3'
    for i in range(100):
        if not silent_check(get_policy(), identity):
            print 'policy banned'
            continue
        print 'policy ok'
