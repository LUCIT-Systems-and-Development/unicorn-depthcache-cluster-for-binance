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


class Database:
    def __init__(self, app=None):
        self.app = app
        self.data = {}
        self.data_lock = threading.Lock()

    def delete(self, key) -> bool:
        with self.data_lock:
            if key in self.data:
                del self.data[key]
                self.app.stdout_msg(f"# DB entry deleted: {key}", log="debug", stdout=False)
                return True
        self.app.stdout_msg(f"# DB entry {key} not found.", log="debug", stdout=False)
        return False

    def export(self) -> str:
        with self.data_lock:
            return json.dumps(self.data, indent=4)

    def get(self, key):
        return self.data.get(key)

    def get_all(self) -> dict:
        return self.data

    def load(self, data_json) -> bool:
        with self.data_lock:
            self.data = json.loads(data_json)
        return True

    def set(self, key, value) -> bool:
        with self.data_lock:
            self.data[key] = value
        self.app.stdout_msg(f"DB entry added/updated: {key} = {value}", log="debug", stdout=False)
        return True
