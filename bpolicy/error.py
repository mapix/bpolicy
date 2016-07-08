# -*- coding: utf-8 -*-


from __future__ import unicode_literals
class PolicyError(Exception):

    def __init__(self, policy, message):
        self.policy = policy
        super(PolicyError, self).__init__(message)

    def __str__(self):
        return '{class_name}({policy}: {message})'.format(class_name=self.__class__.__name__, policy=self.policy.kind, message=self.message)
