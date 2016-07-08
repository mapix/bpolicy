# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from .consts import POLICY_KIND
from .base import Policy, PolicyFactory


class ClockPolicy(Policy):

    kind = POLICY_KIND.CLOCK

    def _get_current_time(self):
        return datetime.now().time()

    def check(self, identity):
        if self.factory.current_clock_factory:
            current_time = self.factory.current_clock_factory(identity)
        else:
            current_time = self._get_current_time()
        if self.factory.start_time < current_time < self.factory.end_time:
            self.logger.debug('clock policy(%s to %s) encountered, discount all successor policy quota by %s', self.factory.start_time, self.factory.end_time, self.factory.discount)
            self.discount(self.factory.discount)
        else:
            self.logger.debug('clock policy not encountered, silent pass through')
        super(ClockPolicy, self).check(identity)

    def _delete(self, identity):
        pass


class ClockPolicyFactory(PolicyFactory):

    policy_class = ClockPolicy

    def __init__(self, start_time, end_time, discount, current_clock_factory=None):
        self.start_time = start_time
        self.end_time = end_time
        self.discount = discount
        self.current_clock_factory = current_clock_factory
