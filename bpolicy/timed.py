# -*- coding: utf-8 -*-


from datetime import datetime

from .consts import POLICY_KIND
from .base import Policy, PolicyFactory


class TimedPolicy(Policy):

    kind = POLICY_KIND.TIMED

    def get_current_time(self):
        return datetime.now().time()

    def check_policy(self, identity):
        if self.factory.start_time < self.get_current_time() < self.factory.end_time:
            self.discount_quota(self.factory.discount)
        super(TimedPolicy, self).check_policy(identity)


class TimedPolicyFactory(PolicyFactory):

    policy_class = TimedPolicy

    def __init__(self, start_time, end_time, discount):
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
