#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# File: pypi/upload_wheel.sh
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://www.lucit.tech/unicorn-depthcache-cluster-for-binance.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance
# Documentation: https://unicorn-depthcache-cluster-for-binance.docs.lucit.tech
# PyPI: https://pypi.org/project/unicorn-depthcache-cluster-for-binance
# LUCIT Online Shop: https://shop.lucit.services/software
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-depthcache-cluster-for-binance/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2019-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.
#
# create this file:
# ~/.pypirc

set -xeuo pipefail

python3 -m twine upload dist/*
