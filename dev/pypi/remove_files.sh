#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# File: pypi/remove_files.sh
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

set -xuo

rm ./build -r
rm ./dist -r
rm ./wheelhouse -r
rm ./*.egg-info -r

rm lucit_ubdcc_mgmt/*.so
rm lucit_ubdcc_mgmt/*.c
rm lucit_ubdcc_shared_modules/*.so
rm lucit_ubdcc_shared_modules/*.c
