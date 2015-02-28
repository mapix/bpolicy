# -*- coding: utf-8 -*-

import web
import logging
from datetime import time
from cStringIO import StringIO


def setup_bp_log(stream):
    from bpolicy import DEFAULT_LOGGER_FORMATER
    bpolicy_handler = logging.StreamHandler(stream)
    bpolicy_handler.setFormatter(DEFAULT_LOGGER_FORMATER)
    bpolicy_logger = logging.getLogger('bpolicy')
    for handler in bpolicy_logger.handlers:
        bpolicy_logger.removeHandler(handler)
    bpolicy_logger.addHandler(bpolicy_handler)
    bpolicy_logger.setLevel(logging.DEBUG)


def check_policy(identity):
    from bpolicy.utils import memoize
    from bpolicy import chained_policy, silent_check
    @memoize
    def _get_factories():
        import memcache
        from bpolicy.consts import MINUTE, HOUR
        from bpolicy import RatedPolicyFactory, TimedPolicyFactory, CERNetPolicyFactory, GenerationedPolicyFactory
        store = memcache.Client(['127.0.0.1:9013'])
        rated_factory = RatedPolicyFactory(quota=10, interval=1 * MINUTE, store=store)
        timed_factory = TimedPolicyFactory(start_time=time(hour=1), end_time=time(hour=6), discount=0.3)
        generationed_factory = GenerationedPolicyFactory(quota=10, interval=1 * HOUR, discount=0.5, max_keep_traking=3, store=store)
        cernet_factory = CERNetPolicyFactory(discount=0.9)
        return rated_factory, generationed_factory, timed_factory, cernet_factory
    return silent_check(chained_policy(*_get_factories()), identity)


class HelloBP(object):

    def GET(self):
        web.header('Content-Type', 'text/html')
        stream = StringIO()
        # there is a bug when StringIO encountered logging
        # so reset handlers each request for demonstrate purpose
        setup_bp_log(stream)
        identity = web.ctx.env['REMOTE_ADDR']
        output = ''
        if not check_policy(identity):
            output += '<h1>banned !!!!!</h1>'
        else:
            output += '<h1>hello !!!!!</h1>'
        output += '<p> IPAdress : %s' % identity
        logger_data = stream.getvalue()
        return output + '<br>' + '<div style="background-color:#000;color:red;padding:10px">' + '<br>'.join(logger_data.split('\n')) + '</div>'


urls = ("/", "HelloBP")
app = web.application(urls, globals())


if __name__ == "__main__":
    app.run()
