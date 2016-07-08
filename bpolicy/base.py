# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import str
from builtins import object

import logging
from hashlib import md5


class Policy(object):

    kind = NotImplemented

    def __init__(self, service, factory, store, next_policy, prefix):
        self.service = service
        self.factory = factory
        self.store = store
        self.next_policy = next_policy
        self.prefix = prefix
        self.logger = logging.getLogger("bpolicy.{service}.{kind}".format(service=self.service, kind=self.kind))
        self.logger.addHandler(logging.NullHandler())

    def _gen_signature(self):
        return md5(str(self.factory.__dict__).encode()).hexdigest()[:7]

    def _gen_key(self, identity):
        return "bpolicy:{prefix}:{service}:{kind}:{signature}:{identity}".format(
            prefix=self.prefix, service=self.service, kind=self.kind, signature=self._gen_signature(), identity=identity)

    def check(self, identity):
        if self.next_policy:
            self.next_policy.check(identity)

    def _delete(self, identity):
        self.store.delete(self._gen_key(identity))

    def reset(self, identity):
        self._delete(identity)
        if self.next_policy:
            self.next_policy.reset(identity)

    def discount(self, discount):
        if self.next_policy:
            self.next_policy.discount(discount)


class PolicyFactory(object):

    policy_class = NotImplemented

    def instance(self, service, store, next_policy=None, prefix=""):
        return self.policy_class(service, self, store, next_policy, prefix)
