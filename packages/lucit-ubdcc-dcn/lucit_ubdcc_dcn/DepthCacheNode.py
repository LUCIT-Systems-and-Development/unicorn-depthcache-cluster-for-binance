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
from lucit_ubdcc_shared_modules.ServiceBase import ServiceBase
from unicorn_binance_local_depth_cache import BinanceLocalDepthCacheManager


class DepthCacheNode(ServiceBase):
    def __init__(self, cwd=None):
        super().__init__(app_name="lucit-ubdcc-dcn", cwd=cwd)

    async def main(self):
        self.app.data['depthcache_instances'] = {}
        self.app.data['local_depthcaches'] = []
        self.app.data['responsibilities'] = []

        self.start_rest_server(endpoints=RestEndpoints)
        self.app.set_status_running()
        self.app.register_or_restart()
        self.db_init()
        while self.app.is_shutdown() is False:
            await self.app.sleep()
            self.app.ubdcc_node_sync()
            self.app.data['responsibilities'] = self.db.get_dcn_responsibilities()
            print(f"Local DepthCaches: {self.app.data['local_depthcaches']}")
            print(f"Responsibilities: {self.app.data['responsibilities']}")
            for dc in self.app.data['responsibilities']:
                if dc not in self.app.data['local_depthcaches']:
                    # Create DC
                    print(f"Adding local DC: {dc}")
                    if self.app.data['depthcache_instances'].get(dc['exchange']) is None:
                        self.app.data['depthcache_instances'][dc['exchange']] = {}
                    if self.app.data['depthcache_instances'][dc['exchange']].get('update_interval') is None:
                        if dc['update_interval'] == 1000:
                            self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = \
                                BinanceLocalDepthCacheManager(exchange=dc['exchange'],
                                                              lucit_api_secret=self.db.get_license_api_secret(),
                                                              lucit_license_token=self.db.get_license_license_token())
                        else:
                            self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']] = \
                                BinanceLocalDepthCacheManager(exchange=dc['exchange'],
                                                              depth_cache_update_interval=dc['update_interval'],
                                                              lucit_api_secret=self.db.get_license_api_secret(),
                                                              lucit_license_token=self.db.get_license_license_token())
                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].create_depth_cache(markets=dc['market'],
                                                                                                                    refresh_interval=dc['refresh_interval'])
                    self.app.data['local_depthcaches'].append(dc)
            for dc in self.app.data['local_depthcaches']:
                if dc not in self.app.data['responsibilities']:
                    # Stop DC
                    print(f"Removing local DC: {dc}")
                    self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].stop_depth_cache(markets=dc['market'])
                    self.app.data['local_depthcaches'].remove(dc)
        print(f"Stopping all DepthCache instances ...")
        for dc in self.app.data['local_depthcaches']:
            for udpate_interval in self.app.data['depthcache_instances'][dc['exchange']]:
                self.app.data['depthcache_instances'][dc['exchange']][udpate_interval].stop_manager()

