# -*- coding: utf-8 -*-


from datetime import timedelta
from collections import namedtuple

SECOND = int(timedelta(seconds=1).total_seconds())
MINUTE = int(timedelta(minutes=1).total_seconds())
HOUR = int(timedelta(hours=1).total_seconds())
DAY = int(timedelta(days=1).total_seconds())
WEEK = int(timedelta(weeks=1).total_seconds())

POLICY_KIND = namedtuple('POLICY_KIND', ['TIMED', 'RATED', 'CERNET', 'GENERATIONED'])('timed', 'rated', 'cernet', 'generationed')
