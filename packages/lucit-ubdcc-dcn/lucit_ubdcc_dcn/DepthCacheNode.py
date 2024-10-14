#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-dcn/lucit_ubdcc_dcn/DepthCacheNode.py
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

from .RestEndpoints import RestEndpoints
from lucit_licensing_python.exceptions import NoValidatedLucitLicense
from lucit_ubdcc_shared_modules.ServiceBase import ServiceBase
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager, DepthCacheNotFound

INIT_INTERVAL: float = 2.0


class DepthCacheNode(ServiceBase):
    def __init__(self, cwd=None):
        super().__init__(app_name="lucit-ubdcc-dcn", cwd=cwd)

    async def main(self):
        self.app.data['depthcache_instances'] = {}
        self.app.data['local_depthcaches'] = []
        self.app.data['responsibilities'] = []
        await self.start_rest_server(endpoints=RestEndpoints)
        self.app.set_status_running()
        await self.app.register_or_restart()
        self.db_init()
        while self.app.is_shutdown() is False:
            await self.app.sleep()
            await self.app.ubdcc_node_sync()
            self.app.data['responsibilities'] = self.db.get_dcn_responsibilities()
            self.app.stdout_msg(f"Local DepthCaches: {self.app.data['local_depthcaches']}", log="info")
            self.app.stdout_msg(f"Responsibilities: {self.app.data['responsibilities']}", log="info")
            for dc in self.app.data['responsibilities']:
                if self.app.is_shutdown() is True:
                    break
                if dc not in self.app.data['local_depthcaches']:
                    # Create DC
                    self.app.stdout_msg(f"Adding local DC: {dc}", log="info")
                    if self.app.data['depthcache_instances'].get(dc['exchange']) is None:
                        self.app.data['depthcache_instances'][dc['exchange']] = {}
                    if self.app.data['depthcache_instances'][dc['exchange']].get(dc['update_interval']) is None:
                        if self.app.data['db'].get_license_status() == "VALID":
                            if dc['update_interval'] == 1000:
                                try:
                                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = \
                                        BinanceLocalDepthCacheManager(exchange=dc['exchange'],
                                                                      init_interval=INIT_INTERVAL,
                                                                      lucit_api_secret=self.db.get_license_api_secret(),
                                                                      lucit_license_token=self.db.get_license_license_token())
                                except NoValidatedLucitLicense as error_msg:
                                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = None
                                    self.app.stdout_msg(error_msg, log="critical")
                                    await self.app.ubdcc_update_depthcache_distribution(exchange=dc['exchange'],
                                                                                        market=dc['market'],
                                                                                        status="stopped")
                            else:
                                try:
                                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = \
                                        BinanceLocalDepthCacheManager(exchange=dc['exchange'],
                                                                      depth_cache_update_interval=dc['update_interval'],
                                                                      init_interval=INIT_INTERVAL,
                                                                      lucit_api_secret=self.db.get_license_api_secret(),
                                                                      lucit_license_token=self.db.get_license_license_token())
                                except NoValidatedLucitLicense as error_msg:
                                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = None
                                    self.app.stdout_msg(error_msg, log="critical")
                                    await self.app.ubdcc_update_depthcache_distribution(exchange=dc['exchange'],
                                                                                        market=dc['market'],
                                                                                        status="stopped")
                        else:
                            await self.app.ubdcc_update_depthcache_distribution(exchange=dc['exchange'],
                                                                                market=dc['market'],
                                                                                status="stopped")
                            self.app.stdout_msg(f"UBLDC intance cannot be started because no valid license is "
                                                f"available!", log="critical")
                    if self.app.data['depthcache_instances'][dc['exchange']].get(dc['update_interval']) is not None:
                        self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].create_depth_cache(
                            markets=dc['market'],
                            refresh_interval=dc['refresh_interval']
                        )
                        await self.app.ubdcc_update_depthcache_distribution(exchange=dc['exchange'],
                                                                            market=dc['market'],
                                                                            status="running")
                        self.app.data['local_depthcaches'].append(dc)
                    await self.app.ubdcc_node_sync()
            for dc in self.app.data['local_depthcaches']:
                if self.app.is_shutdown() is True:
                    break
                if dc not in self.app.data['responsibilities']:
                    # Stop DC
                    self.app.stdout_msg(f"Removing local DC: {dc}", log="info")
                    try:
                        self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].stop_depth_cache(
                            markets=dc['market']
                        )
                    except DepthCacheNotFound as error_msg:
                        self.app.stdout_msg(f"DepthCache not found: {error_msg}", log="error")
                    self.app.data['local_depthcaches'].remove(dc)
                    await self.app.ubdcc_node_sync()
        self.app.stdout_msg(f"Stopping all DepthCache instances ...", log="error")
        for dc in self.app.data['local_depthcaches']:
            for update_interval in self.app.data['depthcache_instances'][dc['exchange']]:
                self.app.data['depthcache_instances'][dc['exchange']][update_interval].stop_manager()
