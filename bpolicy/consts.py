# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging

from datetime import timedelta
from collections import namedtuple

SECOND = int(timedelta(seconds=1).total_seconds())
MINUTE = int(timedelta(minutes=1).total_seconds())
HOUR = int(timedelta(hours=1).total_seconds())
DAY = int(timedelta(days=1).total_seconds())
WEEK = int(timedelta(weeks=1).total_seconds())

POLICY_KIND = namedtuple('POLICY_KIND', ['CLOCK', 'RATED', 'GENERATIONED'])('clock', 'rated', 'generationed')
DEFAULT_LOGGER_FORMATER = logging.Formatter(fmt='[%(asctime)s]\t[%(levelname)s]\t%(name)-20s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
