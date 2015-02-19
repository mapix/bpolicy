# -*- coding: utf-8 -*-


from datetime import datetime

from .consts import POLICY_KIND
from .base import Policy, PolicyFactory


class TimedPolicy(Policy):

    kind = POLICY_KIND.TIMED

    def check_policy(self, identity):
        current_time = datetime.now().time()
        if self.start_time < current_time < self.end_time:
            self.discount_quota(self.factory.discount)
        super(TimedPolicy, self).check_policy(identity)


class TimedPolicyFactory(PolicyFactory):

    policy_class = TimedPolicy

    def __init__(self, start_time, end_time, discount):
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
