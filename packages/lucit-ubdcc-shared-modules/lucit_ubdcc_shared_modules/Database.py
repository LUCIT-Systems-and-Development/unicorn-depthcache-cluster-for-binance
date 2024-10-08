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

import threading
import time


class Database:
    def __init__(self, app=None):
        self.app = app
        self.app.data['db'] = self
        self.data = {}
        self.data_lock = threading.Lock()
        self._init()

    def _init(self) -> bool:
        self.app.stdout_msg(f"Initiating Database ...", log="info")
        self.set(key="depthcaches", value={})
        self.set(key="license", value={"api_secret": "",
                                       "license_token": "",
                                       "status": "INVALID"})
        self.set(key="nodes", value={})
        self.set(key="pods", value={})
        self.set(key="timestamp", value=float())
        self.update_nodes()
        return True

    def _set_update_timestamp(self) -> bool:
        self.data['timestamp'] = self.app.get_unix_timestamp()
        return True

    def is_empty(self) -> bool:
        if len(self.data['pods']) == 0 and \
                len(self.data['depthcaches']) == 0 and \
                len(self.data['license']['api_secret']) == 0 and \
                len(self.data['license']['license_token']) == 0:
            return True
        return False

    def add_depthcache(self,
                       exchange: str = None,
                       symbol: str = None,
                       desired_quantity: int = None,
                       update_interval: int = None,
                       refresh_interval: int = None) -> bool:
        if exchange is None or symbol is None:
            raise ValueError("Missing mandatory parameter: exchange, symbol")
        if desired_quantity is None or desired_quantity == "None":
            desired_quantity = 1
        if update_interval is None or update_interval == "None":
            update_interval = "1000ms"
        if refresh_interval is None or refresh_interval == "None":
            refresh_interval = None
        depthcache = {"DESIRED_QUANTITY": int(desired_quantity),
                      "DISTRIBUTION": [],
                      "EXCHANGE": exchange,
                      "REFRESH_INTERVAL": refresh_interval,
                      "SYMBOL": symbol,
                      "UPDATE_INTERVAL": update_interval}
        with self.data_lock:
            if self.data['depthcaches'].get('exchange') is None:
                self.data['depthcaches'][exchange] = {}
            self.data['depthcaches'][exchange][symbol] = depthcache
            self._set_update_timestamp()
        return True

    def add_depthcache_distribution(self,
                                    exchange: str = None,
                                    symbol: str = None,
                                    pod_uid: str = None,
                                    last_restart_time: float = None,
                                    status: str = None) -> bool:
        if exchange is None or symbol is None or pod_uid is None:
            raise ValueError("Missing mandatory parameter: exchange, pod_uid, symbol")
        distribution = {"POD_UID": pod_uid,
                        "CREATED_TIME": self.app.get_timestamp(),
                        "LAST_RESTART_TIME": last_restart_time,
                        "STATUS": status}
        with self.data_lock:
            self.data['depthcaches'][exchange][symbol]['DISTRIBUTION'] = distribution
            self._set_update_timestamp()
        return True

    def add_pod(self, name: str = None, uid: str = None, node: str = None, role: str = None, ip: str = None,
                api_port_rest: int = None, status: str = None, version: str = None) -> bool:
        if uid is None:
            raise ValueError("Missing mandatory parameter: uid")
        pod = {"NAME": name,
               "UID": uid,
               "NODE": node,
               "ROLE": role,
               "IP": ip,
               "API_PORT_REST": api_port_rest,
               "LAST_SEEN": self.app.get_unix_timestamp(),
               "STATUS": status,
               "VERSION": version}
        with self.data_lock:
            self.data['pods'][uid] = pod
            self._set_update_timestamp()
        return True

    def delete(self, key: str = None) -> bool:
        with self.data_lock:
            if key in self.data:
                del self.data[key]
                self._set_update_timestamp()
                self.app.stdout_msg(f"DB entry deleted: {key}", log="debug", stdout=False)
                return True
        self.app.stdout_msg(f"DB entry {key} not found.", log="debug", stdout=False)
        return False

    def delete_depthcache(self, exchange: str = None, symbol: str = None) -> bool:
        if exchange is None or symbol is None:
            raise ValueError("Missing mandatory parameter: exchange, symbol")
        with self.data_lock:
            try:
                del self.data["depthcaches"][exchange][symbol]
            except KeyError:
                return True
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB depthcaches deleted: {exchange}, {symbol}", log="debug")
        return True

    def delete_depthcache_distribution(self, exchange: str = None, symbol: str = None, pod_uid: str = None) -> bool:
        if exchange is None or symbol is None or pod_uid is None:
            raise ValueError("Missing mandatory parameter: exchange, pod_uid, symbol")
        with self.data_lock:
            del self.data["depthcaches"][exchange][symbol]['DISTRIBUTION'][pod_uid]
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB depthcache distribution deleted: {exchange}, {symbol}, {pod_uid}", log="debug")
        return True

    def delete_pod(self, uid: str = None) -> bool:
        if uid is None:
            raise ValueError("Missing mandatory parameter: uid")
        with self.data_lock:
            del self.data["pods"][uid]
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB pod deleted: {uid}", log="debug", stdout=True)
        return True

    def delete_old_pods(self) -> bool:
        old_pods = []
        max_age = 60
        with self.data_lock:
            for uid in self.data['pods']:
                if (time.time() - max_age) > self.data['pods'][uid]['LAST_SEEN']:
                    old_pods.append(uid)
        for uid in old_pods:
            self.delete_pod(uid=uid)
        return True

    def exists_pod(self, uid: str) -> bool:
        if uid is None:
            raise ValueError("Missing mandatory parameter: uid")
        with self.data_lock:
            return uid in self.data['pods']

    def get(self, key: str = None):
        with self.data_lock:
            return self.data.get(key)

    def get_all(self) -> dict:
        with self.data_lock:
            return self.data

    def get_backup_dict(self) -> dict:
        with self.data_lock:
            return self.app.sort_dict(input_dict=self.app.data['db'].data)

    def get_best_dcn(self, excluded_pods):
        available_pods = {}
        for pod in self.data['pods']:
            if pod['ROLE'] == "lucit-ubdcc-dcn":
                available_pods[pod['UID']] = self.data['nodes'][pod['NODE']]
        delta_pods = {uid: cpu for uid, cpu in available_pods.items() if uid not in excluded_pods}
        if not delta_pods:
            return None
        best_pod = min(delta_pods, key=lambda uid: delta_pods[uid])
        return best_pod

    def get_license_api_secret(self) -> str:
        with self.data_lock:
            return self.data['license']['api_secret']

    def get_license_license_token(self) -> str:
        with self.data_lock:
            return self.data['license']['license_token']

    def get_license_status(self) -> str:
        with self.data_lock:
            return self.data['license']['status']

    def get_pod_by_uid(self, uid=None) -> dict | None:
        if uid is None:
            raise ValueError("Missing mandatory parameter: uid")
        with self.data_lock:
            try:
                return self.data['pods'][uid]
            except KeyError:
                return None

    def replace_data(self, data: dict = None):
        with self.data_lock:
            self.data = data
        return True

    def set(self, key: str = None, value: dict | str | float | list | set | tuple = None) -> bool:
        with self.data_lock:
            self.data[key] = value
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB entry added/updated: {key} = {value}", log="debug", stdout=False)
        return True

    def set_license_status(self, status: str = None) -> bool:
        if status is None:
            raise ValueError("Missing mandatory parameter: status")
        with self.data_lock:
            self.data['license']['status'] = status
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB license status change to: {status}", log="debug", stdout=False)
        return True

    def submit_license(self, api_secret: str = None, license_token: str = None) -> bool:
        if api_secret is None or license_token is None:
            raise ValueError("Missing mandatory parameter: api_secret, license_token")
        with self.data_lock:
            self.data['license']['api_secret'] = api_secret
            self.data['license']['license_token'] = license_token
            self._set_update_timestamp()
        self.app.stdout_msg(f"DB license submitted: {api_secret}, {license_token}", log="debug", stdout=False)
        return True

    def update_nodes(self) -> bool:
        nodes = self.app.get_k8s_nodes()
        if nodes:
            self.set(key="nodes", value=nodes)
            self.app.stdout_msg(f"DB all nodes updated!", log="debug", stdout=False)
            return True
        else:
            self.app.stdout_msg(f"Timed update of the DB key 'nodes': Query of the k8s nodes was empty, no "
                                f"update is performed!", log="error", stdout=True)
            return False

    def update_depthcache(self,
                          desired_quantity: int = None,
                          exchange: str = None,
                          refresh_interval: int = None,
                          symbol: str = None,
                          update_interval: int = None) -> bool:
        if exchange is None or symbol is None:
            raise ValueError("Missing mandatory parameter: exchange, symbol")
        with self.data_lock:
            if desired_quantity is not None:
                self.data['depthcaches'][exchange][symbol]['DESIRED_QUANTITY'] = desired_quantity
                self._set_update_timestamp()
            if update_interval is not None:
                self.data['depthcaches'][exchange][symbol]['UPDATE_INTERVAL'] = update_interval
                self._set_update_timestamp()
            if refresh_interval is not None:
                self.data['depthcaches'][exchange][symbol]['REFRESH_INTERVAL'] = refresh_interval
                self._set_update_timestamp()
        self.app.stdout_msg(f"DB depthcaches updated: {exchange}, {symbol}, {desired_quantity}, {update_interval}",
                            log="debug")
        return True

    def update_depthcache_distribution(self,
                                       exchange: str = None,
                                       symbol: str = None,
                                       pod_uid: str = None,
                                       last_restart_time: float = None,
                                       status: str = None) -> bool:
        if exchange is None or symbol is None or pod_uid is None:
            raise ValueError("Missing mandatory parameter: exchange, pod_uid, symbol")
        with self.data_lock:
            if last_restart_time is not None:
                self.data['depthcaches'][exchange][symbol][pod_uid]['DISTRIBUTION']['LAST_RESTART_TIME'] = \
                    last_restart_time
                self._set_update_timestamp()
            if status is not None:
                self.data['depthcaches'][exchange][symbol][pod_uid]['DISTRIBUTION']['STATUS'] = status
                self._set_update_timestamp()
        self.app.stdout_msg(f"DB depthcache distribution updated: {exchange}, {symbol}, {pod_uid}, {last_restart_time},"
                            f"{status}", log="debug")
        return True

    def update_pod(self, uid: str = None, node: str = None, ip: str = None, api_port_rest: int = None,
                   status: str = None) -> bool:
        if uid is None:
            raise ValueError("Missing mandatory parameter: uid")
        with self.data_lock:
            self.data['pods'][uid]['LAST_SEEN'] = self.app.get_unix_timestamp()
            if api_port_rest is not None:
                self.data['pods'][uid]['API_PORT_REST'] = api_port_rest
                self._set_update_timestamp()
            if ip is not None:
                self.data['pods'][uid]['IP'] = ip
                self._set_update_timestamp()
            if node is not None:
                self.data['pods'][uid]['NODE'] = node
                self._set_update_timestamp()
            if status is not None:
                self.data['pods'][uid]['STATUS'] = status
                self._set_update_timestamp()
        self.app.stdout_msg(f"DB pod updated: {uid}", log="debug", stdout=False)
        return True
