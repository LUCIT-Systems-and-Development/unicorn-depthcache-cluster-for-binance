#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: packages/lucit-ubdcc-dcn/setup.py
#
# Part of ‘UNICORN Binance DepthCache Cluster’
# Project website: https://www.lucit.tech/unicorn-depthcache-cluster-for-binance.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance
# Documentation: https://unicorn-depthcache-cluster-for-binance.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-ubdcc-dcn
# LUCIT Online Shop: https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

from Cython.Build import cythonize
from setuptools import setup

name = "lucit-ubdcc-dcn"
source_dir = "lucit_ubdcc_dcn"

# Setup
with open("README.md", "r") as fh:
    print("Using README.md content as `long_description` ...")
    long_description = fh.read()

setup(
    name=name,
    version="0.1.4",
    author="LUCIT Systems and Development",
    author_email='info@lucit.tech',
    url="https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance",
    description="LUCIT UBDCC REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='LSOSL - LUCIT Synergetic Open Source License',
    install_requires=['lucit-licensing-python>=1.8.2', 'lucit-ubdcc-shared-modules==0.1.4',
                      'unicorn_binance_local_depth_cache==2.6.0'],
    keywords='',
    project_urls={
        'Howto': 'https://www.lucit.tech/unicorn-depthcache-cluster-for-binance.html#howto',
        'Documentation': 'https://www.lucit.tech/unicorn-depthcache-cluster-for-binance.html',
        'Wiki': 'https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/wiki',
        'Author': 'https://www.lucit.tech',
        'Changes': 'https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/blob/master/packages/lucit-ubdcc-dcn/CHANGELOG.md',
        'License': 'https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/blob/master/LICENSE',
        'Issue Tracker': 'https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/issues',
        'Chat': 'https://gitter.im/unicorn-trading-suite/unicorn-depthcache-cluster-for-binance',
        'Telegram': 'https://t.me/unicorndevs',
        'Get Support': 'https://www.lucit.tech/get-support.html',
        'LUCIT Online Shop': 'https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance',
    },
    ext_modules=cythonize(['lucit_ubdcc_dcn/__init__.py',
                           'lucit_ubdcc_dcn/RestEndpoints.py',
                           'lucit_ubdcc_dcn/DepthCacheNode.py'],
                          compiler_directives={'language_level': "3"}),
    python_requires='>=3.12.0',
    package_data={'': ['lucit_ubdcc_dcn/*.so']},
    exclude_package_data={'': ['lucit_ubdcc_dcn/*.py']},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Cython",
        "License :: Other/Proprietary License",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: AsyncIO",
    ],
)
