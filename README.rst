BPOLICY
=======

A collection of basic policies for resources anti-spammer.

.. image:: http://img3.douban.com/view/biz/raw/public/f477075ba610e94.jpg
   :height: 240px
   :width: 300 px

Install from Pypi
-----------------
::

    pip install bpolicy


Basic Example
-------------
::

    import memcache
    from bpolicy.consts import MINUTE, HOUR
    from bpolicy import RatedPolicyFactory, ClockPolicyFactory, GenerationedPolicyFactory
    from bpolicy import chained_policy, silent_check

    store = memcache.Client(['127.0.0.1:9013'])
    rated_factory = RatedPolicyFactory(quota=10, interval=1 * MINUTE)
    clock_factory = ClockPolicyFactory(start_time=time(hour=1), end_time=time(hour=6), discount=0.3)
    generationed_factory = GenerationedPolicyFactory(quota=10, interval=1 * HOUR, discount=0.5, max_keep_traking=3)


    def check_policy(identity):
        return silent_check(chained_policy('hello', [generationed_factory, clock_factory, rated_factory], store), identity)


    identity = "88.88.23.1"
    for i in range(100):
        if check_policy(identity):
            print "success"
        else:
            print "banded"
