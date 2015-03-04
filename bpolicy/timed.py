# -*- coding: utf-8 -*-

from datetime import datetime

from .consts import POLICY_KIND, DEFAULT_SERVICE
from .base import Policy, PolicyFactory


class TimedPolicy(Policy):

    kind = POLICY_KIND.TIMED

    def get_current_time(self):
        return datetime.now().time()

    def check_policy(self, identity):
        if self.factory.start_time < self.get_current_time() < self.factory.end_time:
            self.logger.debug('timed policy(%s to %s) encountered, discount all successor policy quota by %s', self.factory.start_time, self.factory.end_time, self.factory.discount)
            self.discount_quota(self.factory.discount)
        else:
            self.logger.debug('timed policy not encountered, silent pass through')
        super(TimedPolicy, self).check_policy(identity)


class TimedPolicyFactory(PolicyFactory):

    policy_class = TimedPolicy

    def __init__(self, start_time, end_time, discount, service=DEFAULT_SERVICE):
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
        super(TimedPolicyFactory, self).__init__(service)
