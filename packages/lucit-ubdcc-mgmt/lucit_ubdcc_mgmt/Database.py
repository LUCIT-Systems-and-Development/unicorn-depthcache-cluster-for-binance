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
from typing import Union


class Database:
    def __init__(self, app=None):
        self.app = app
        self.data = {}
        self.data_lock = threading.Lock()
        self._init()

    def _init(self) -> bool:
        self.app.stdout_msg(f"Initiating Database ...", log="info")
        self.set(key="depthcaches", value={})
        self.set(key="depthcache_distribution", value={})
        self.set(key="pods", value={})
        self.set(key="nodes", value={})
        self.update_nodes()
        return True

    def add_depthcache(self, symbol: str = None, desired_quantity: int = None, update_interval: int = None) -> bool:
        if symbol is None:
            raise ValueError("Parameter 'symbol' is mandatory!")
        depthcache = {"SYMBOL": symbol,
                      "DESIRED_QUANTITY": desired_quantity,
                      "UPDATE_INTERVAL": update_interval}
        with self.data_lock:
            self.data['depthcaches'][symbol] = depthcache
        return True

    def add_depthcache_distribution(self, symbol: str = None, pod_uid: str = None,
                                    last_restart_time: float = None, status: str = None) -> bool:
        if symbol is None or pod_uid is None:
            raise ValueError("Parameter 'symbol' and 'pod_uid' are mandatory!")
        distribution = {"SYMBOL": symbol,
                        "POD_UID": pod_uid,
                        "CREATED_TIME": self.app.get_timestamp(),
                        "LAST_RESTART_TIME": last_restart_time,
                        "STATUS": status}
        with self.data_lock:
            self.data['depthcache_distribution'][f"{symbol}_{pod_uid}"] = distribution
        return True

    def add_pod(self, name: str = None, uid: str = None, node: str = None, role: str = None, ip: str = None,
                api_port_rest: int = None, status: str = None) -> bool:
        if uid is None:
            raise ValueError("Parameter 'uid' is mandatory!")
        pod = {"NAME": name,
               "UID": uid,
               "NODE": node,
               "ROLE": role,
               "IP": ip,
               "API_PORT_REST": api_port_rest,
               "LAST_SEEN": self.app.get_unix_timestamp(),
               "STATUS": status}
        with self.data_lock:
            self.data['pods'][uid] = pod
        return True

    def delete(self, key: str = None) -> bool:
        with self.data_lock:
            if key in self.data:
                del self.data[key]
                self.app.stdout_msg(f"DB entry deleted: {key}", log="debug", stdout=False)
                return True
        self.app.stdout_msg(f"DB entry {key} not found.", log="debug", stdout=False)
        return False

    def delete_depthcache(self, symbol: str = None) -> bool:
        if symbol is None:
            raise ValueError("Parameter 'symbol' is mandatory!")
        with self.data_lock:
            del self.data["depthcaches"][symbol]
        self.app.stdout_msg(f"DB depthcaches deleted: {symbol}", log="debug", stdout=False)
        return True

    def delete_depthcache_distribution(self, symbol: str = None, pod_uid: str = None) -> bool:
        if symbol is None or pod_uid is None:
            raise ValueError("Parameter 'symbol' and 'pod_uid' are mandatory!")
        with self.data_lock:
            del self.data['depthcache_distribution'][f"{symbol}_{pod_uid}"]
        self.app.stdout_msg(f"DB depthcaches deleted: {symbol}", log="debug", stdout=False)
        return True

    def delete_pod(self, uid: str = None) -> bool:
        if uid is None:
            raise ValueError("Parameter 'uid' is mandatory!")
        with self.data_lock:
            del self.data["pods"][uid]
        self.app.stdout_msg(f"DB pod deleted: {uid}", log="debug", stdout=False)
        return True

    def exists_pod(self, uid: str) -> bool:
        if uid is None:
            raise ValueError("Parameter 'uid' ist mandatory!")
        with self.data_lock:
            return uid in self.data['pods']

    def export(self) -> str:
        with self.data_lock:
            return json.dumps(self.data, indent=4)

    def get(self, key: str = None):
        with self.data_lock:
            return self.data.get(key)

    def get_all(self) -> dict:
        with self.data_lock:
            return self.data

    def load(self, data_json: str = None) -> bool:
        with self.data_lock:
            self.data = json.loads(data_json)
        return True

    def set(self, key: str = None, value: Union[dict, str, list, set, tuple] = None) -> bool:
        with self.data_lock:
            self.data[key] = value
        self.app.stdout_msg(f"DB entry added/updated: {key} = {value}", log="debug", stdout=False)
        return True

    def update_nodes(self) -> bool:
        self.set(key="nodes", value=self.app.get_k8s_nodes())
        self.app.stdout_msg(f"DB all nodes updated!", log="debug", stdout=False)
        return True

    def update_depthcache(self, symbol: str = None, desired_quantity: int = None, update_interval: int = None) -> bool:
        if symbol is None:
            raise ValueError("Parameter 'symbol' is mandatory!")
        with self.data_lock:
            if desired_quantity is not None:
                self.data['depthcaches'][symbol]['DESIRED_QUANTITY'] = desired_quantity
            if update_interval is not None:
                self.data['depthcaches'][symbol]['UPDATE_INTERVAL'] = update_interval
        self.app.stdout_msg(f"DB depthcaches updated: {symbol}", log="debug", stdout=False)
        return True

    def update_depthcache_distribution(self, symbol: str = None, pod_uid: str = None,
                                       last_restart_time: float = None, status: str = None) -> bool:
        if symbol is None or pod_uid is None:
            raise ValueError("Parameter 'symbol' and 'pod_uid' are mandatory!")
        with self.data_lock:
            if last_restart_time is not None:
                self.data['depthcache_distribution'][f"{symbol}_{pod_uid}"]['LAST_RESTART_TIME'] = last_restart_time
            if status is not None:
                self.data['depthcache_distribution'][f"{symbol}_{pod_uid}"]['STATUS'] = status
        self.app.stdout_msg(f"DB depthcaches updated: {symbol}_{pod_uid}", log="debug", stdout=False)
        return True

    def update_pod(self, uid: str = None, node: str = None, ip: str = None, api_port_rest: int = None,
                   status: str = None) -> bool:
        if uid is None:
            raise ValueError("Parameter 'uid' is mandatory!")
        with self.data_lock:
            self.data['pods'][uid]['LAST_SEEN'] = self.app.get_unix_timestamp()
            if api_port_rest is not None:
                self.data['pods'][uid]['API_PORT_REST'] = api_port_rest
            if ip is not None:
                self.data['pods'][uid]['IP'] = ip
            if node is not None:
                self.data['pods'][uid]['NODE'] = node
            if status is not None:
                self.data['pods'][uid]['STATUS'] = status
        self.app.stdout_msg(f"DB pod updated: {uid}", log="debug", stdout=False)
        return True
