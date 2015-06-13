#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='bpolicy',
    version='0.2.0',
    author='mapix',
    author_email='mapix.me@gmail.com',
    packages=find_packages(),
    url='https://github.com/mapix/bpolicy',
    description='A collection of basic policies for resources anti-spammer',
    long_description=open('README.rst').read(),
    license='MIT'
)
