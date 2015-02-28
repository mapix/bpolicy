# -*- coding: utf-8 -*-

import logging
from hashlib import md5


class Policy(object):

    kind = NotImplemented

    def __init__(self, factory, next_policy=None, service='bpolicy', logger=None):
        self.factory = factory
        self.next_policy = next_policy
        self.service = service
        logger_name = '{service}.{kind}'.format(service=service, kind=self.kind)
        self.logger = logger if logger else logging.getLogger(logger_name)
        self.logger.addHandler(logging.NullHandler())

    def discount_quota(self, discount):
        if self.next_policy:
            self.logger.debug('discount next_policy quota')
            self.next_policy.discount_quota(discount)

    def _gen_factory_signature(self):
        return md5(str(self.factory.__dict__)).hexdigest()[:7]

    def _gen_store_key(self, store_prefix, identity):
        return '{store_prefix}{service}:{kind}:{factory_signature}:{identity}'.format(
            store_prefix=self.factory.store_prefix,
            service=self.service,
            kind=self.kind,
            factory_signature=self._gen_factory_signature(),
            identity=identity)

    def check_policy(self, identity):
        if self.next_policy:
            self.logger.debug('check next policy')
            self.next_policy.check_policy(identity)


class PolicyFactory(object):

    policy_class = NotImplemented

    def instance(self, next_policy=None, **kwargs):
        return self.policy_class(self, next_policy, **kwargs)
