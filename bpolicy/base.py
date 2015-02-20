# -*- coding: utf-8 -*-

from hashlib import md5


class Policy(object):

    kind = NotImplemented

    def __init__(self, factory, next_policy=None, service='bpolicy'):
        self.factory = factory
        self.next_policy = next_policy
        self.service = service

    def discount_quota(self, discount):
        if self.next_policy:
            self.next_policy.discount_quota(discount)

    def _gen_factory_signature(self):
        return md5(str(self.factory.__dict__)).hexdigest()[:7]

    def _gen_memcache_key(self, mc_prefix, identity):
        return '{mc_prefix}{service}:{kind}:{factory_signature}:{identity}'.format(
            mc_prefix=self.factory.mc_prefix,
            service=self.service,
            kind=self.kind,
            factory_signature=self._gen_factory_signature(),
            identity=identity)

    def check_policy(self, identity):
        if self.next_policy:
            self.next_policy.check_policy(identity)


class PolicyFactory(object):

    policy_class = NotImplemented

    def instance(self, next_policy=None):
        return self.policy_class(self, next_policy)
