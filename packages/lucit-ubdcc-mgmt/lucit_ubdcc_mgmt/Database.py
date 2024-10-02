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
        self._init()
        # Todo: Load Backup if available

    def _init(self) -> bool:
        self.app.stdout_msg(f"Initiating DB ...", log="info")
        self.set(key="depth_caches", value={})
        self.set(key="depth_cache_distribution", value={})
        self.set(key="pods", value={})
        self.set(key="nodes", value={})
        self.update_nodes()
        return True

    def add_pod(self, name=None, uid=None, node=None, role=None, ip=None, api_port=None, last_seen=None,
                status=None) -> bool:
        pod = {"NAME": name,
               "UID": uid,
               "NODE": node,
               "ROLE": role,
               "IP": ip,
               "API_PORT": api_port,
               "LAST_SEEN": last_seen,
               "STATUS": status}
        with self.data_lock:
            self.data['pods'][uid] = pod
        return True

    def delete(self, key) -> bool:
        with self.data_lock:
            if key in self.data:
                del self.data[key]
                self.app.stdout_msg(f"DB entry deleted: {key}", log="debug", stdout=False)
                return True
        self.app.stdout_msg(f"DB entry {key} not found.", log="debug", stdout=False)
        return False

    def delete_pod(self, uid=None):
        if uid is None:
            raise ValueError("Parameter 'uid' is mandatory!")
        with self.data_lock:
            del self.data["pods"][uid]
        self.app.stdout_msg(f"DB pod deleted: {uid}", log="debug", stdout=False)
        return True

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

    def update_nodes(self) -> bool:
        self.set(key="nodes", value=self.app.get_k8s_nodes())
        self.app.stdout_msg(f"DB all nodes updated!", log="debug", stdout=False)
        return True

    def update_pod(self, uid=None, node=None, ip=None, api_port=None, last_seen=None, status=None) -> bool:
        if uid is None:
            raise ValueError("Parameter 'uid' is mandatory!")
        with self.data_lock:
            if node is not None:
                self.data['pods'][uid]['NODE'] = node
            if ip is not None:
                self.data['pods'][uid]['IP'] = ip
            if api_port is not None:
                self.data['pods'][uid]['API_PORT'] = api_port
            if last_seen is not None:
                self.data['pods'][uid]['LAST_SEEN'] = last_seen
            if status is not None:
                self.data['pods'][uid]['STATUS'] = status
        self.app.stdout_msg(f"DB pod updated: {uid}", log="debug", stdout=False)
        return True
