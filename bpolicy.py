# -*- coding: utf-8 -*-

from datetime import datetime


__all__ = ['PolicyError', 'Policy', 'RatedPolicy', 'AntiDisturbPeriodsPolicy', 'GenerationedPolicy']


class PolicyError(Exception):

    pass


class Policy(object):

    ''' 控制策略
    '''

    def __init__(self, next_policy, *args, **kwargs):
        self.next_policy = next_policy

    def discount_quota(self, discount):
        if self.next_policy:
            self.next_policy.discount_quota(discount)

    def check_policy(self, identity):
        if self.next_policy:
            self.next_policy.check_policy(identity)


class RatedPolicy(Policy):

    ''' 频次策略

    将频次限制分配到多维度, 比如, 一个频次是按天有一个最大配额, 按小时有一个稍微小点点额配额, 按分钟有一个更小的配额.
    '''

    def __init__(self, next_policy, interval, quota, mc, mc_prefix):
        self.interval = interval
        self.quota = quota
        self.mc = mc
        self.mc_prefix = mc_prefix
        super(RatedPolicy, self).__init__(next_policy)

    def discount_quota(self, discount):
        self.quota = self.quota * discount
        super(RatedPolicy, self).discount_quota(discount)

    def check_policy(self, identity):
        key = '{prefix}:{identity}'.format(prefix=self.mc_prefix, identity=identity)
        current = self.mc.get(key)
        if current is None:
            current = 1
            self.mc.set(key, 1, self.interval)
        else:
            current += 1
            self.mc.inrc(key, 1)
        if current > self.quota:
            raise PolicyError('')
        super(RatedPolicy, self).check_policy(identity)


class AntiDisturbPeriodsPolicy(Policy):

    ''' 防打扰区间策略

    按日常作息时间区分, 比如凌晨到5点, 可以调整配额, 使得尽量炸弹不在这里爆炸, 白天的时候可以调整的更宽松一些. 主要以其他方式控制.
    '''

    def __init__(self, next_policy, start_time=None, end_time=None, discount=0.5):
        self.start_time = start_time if start_time else datetime.time(hour=12)
        self.end_time = end_time if end_time else datetime.time(hour=6)
        self.discount = discount
        super(AntiDisturbPeriodsPolicy, self).__init__(next_policy)

    def check_policy(self, identity):
        current_time = datetime.now().time()
        if self.start_time < current_time < self.end_time:
            self.discount_quota(self.discount)
        super(AntiDisturbPeriodsPolicy, self).check_policy(identity)


class GenerationedPolicy(Policy):
    ''' 分代策略

    '''
    """
    在编程语言自动gc 的算法中有分代算法
    luoweifeng
    同样
    luoweifeng
    这里也可以按照分带的思路来搞
    luoweifeng
    这种对 恶意攻击很有效果, 对普通用户影响会稍微小些
    luoweifeng
    比如, 当前的配额限制是一小时 50次
    luoweifeng
    那如果这一个小时内, 50次没有满
    luoweifeng
    那下一个小时清零
    luoweifeng
    否则, 下一个小时的配额自动减少
    luoweifeng
    配额初始为 25
    luoweifeng
    这样, 如果是一个攻击类型的IP
    py
    现在的策略其实是没分代。
    luoweifeng
    在这种分代规则中, 就很快灯枯油尽
    luoweifeng
    而正常的访问不太会影响
    luoweifeng
    这样就可以将 配额初始调大一些
    luoweifeng
    正常的访问就很少能触发规则, 而异常流量则会指数级的缩小

    """
    def __init__(self, next_policy):
        pass


class CERNetPolicy(Policy):

    ''' 网络策略

    IPv4 的紧缺性以及为隔离内外资源导致的 NAT 泛滥的情况
    特定网段限制调高, 教育网为主, 相关的可参照 sms_service. 但预计效果不容乐观, 各大公司等出口IP一般都是统一的, NAT 的毒瘤不止在教育网.
    '''

    pass
