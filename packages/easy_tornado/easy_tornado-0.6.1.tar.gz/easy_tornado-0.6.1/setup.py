#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/8/23 14:29
import ssl

from setuptools import setup, find_packages

ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='easy_tornado',
    version='0.6.1',
    description='A tornado based web framework package',
    author='Wang Shugen',
    author_email='wsg1107556314@163.com',
    url='https://artifacts.wshugen.cn/python',
    packages=find_packages(),
    install_requires=['tornado', 'decorator', 'six', 'urllib3']
)
