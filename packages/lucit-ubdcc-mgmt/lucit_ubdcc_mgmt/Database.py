#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/Database.py
#
# Project website: https://www.lucit.tech/unicorn-binance-depthcache-cluster.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster
# Documentation: https://unicorn-binance-depthcache-cluster.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-ubdcc-mgmt
# LUCIT Online Shop: https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import json
import threading
import time


class Database:
    def __init__(self):
        self.data = {}

    def load(self):
        # Todo:
        pass

    def save(self):
        # Todo:
        pass

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        print(f"Entry added/updated: {key} = {value}")

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            print(f"Entry deleted: {key}")
        else:
            print(f"Entry {key} not found.")

    def get_all(self):
        return self.data
