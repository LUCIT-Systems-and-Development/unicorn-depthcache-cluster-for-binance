#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/Database.py
#
# Project website: https://www.lucit.tech/unicorn-binance-depthcache-cluster.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster
# Documentation: https://unicorn-binance-depthcache-cluster.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-ubdcc-shared-modules
# LUCIT Online Shop: https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import etcd3
import os


class Database:
    def __init__(self):
        if os.getenv('LUCIT_UBDCC_DEV_MODE') == 'TRUE':
            self.client = etcd3.client(host='localhost', port=2379)
        else:
            self.client = etcd3.client(host='etcd-service.lucit-ubdcc.svc.cluster.local', port=2379)

    def put(self, key, value):
        self.client.put(key, value)

    def get(self, key):
        read_value, _ = self.client.get(key)
        return read_value

    def delete(self, key):
        self.client.delete(key)

    def close(self):
        self.client.close()
