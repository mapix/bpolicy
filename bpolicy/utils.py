# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from .error import PolicyError


def chained_policy(service, factories, store, prefix=""):
    policy = None
    for factory in reversed(factories):
        policy = factory.instance(service, store, policy, prefix)
    return policy


def silent_check(policy, identity):
    success = True
    try:
        policy.check(identity)
    except PolicyError:
        success = False
    return success
