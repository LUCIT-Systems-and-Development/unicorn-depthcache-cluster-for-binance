#!/usr/bin/bash
# -*- coding: utf-8 -*-
#
# File: pypi/create_wheel.sh
#
# Part of ‘UNICORN Binance DepthCache Cluster’
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

#set -xeuo pipefail
#set -xeu pipefail

security-check() {
    echo -n "Did you change the version in \`CHANGELOG.md\` and used \`dev/set_version.py\`? [yes|NO] "
    local SURE
    read SURE
    if [ "$SURE" != "yes" ]; then
        exit 1
    fi
}

compile() {
    echo "ok, lets go ..."
    python3 setup.py bdist_wheel sdist
}

security-check
compile
