#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='bpolicy',
    version='0.1.3',
    author='mapix',
    author_email='mapix.me@gmail.com',
    packages=find_packages(),
    url='https://github.com/mapix/bpolicy',
    description='A collection of basic policies for resources anti-spammer',
    long_description=open('README.rst').read(),
    install_requires=['IPy==0.81'],
    package_data = {
        'bpolicy': ['data/*']
    },
    license='MIT'
)
