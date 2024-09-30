#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/Mgmt.py
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

import time
from .Database import Database
from .RestEndpoints import RestEndpoints
from lucit_ubdcc_shared_modules import AppClass, RestServer


class Service:
    def __init__(self, cwd=None):
        self.app_class = AppClass.AppClass(app_name="lucit-ubdcc-mgmt",
                                           cwd=cwd,
                                           service_call=self.run,
                                           stop_call=self.stop)
        self.rest_server = None
        self.app_class.start()

    def run(self):
        bl = Mgmt(service=self)
        bl.main()

    def stop(self):
        try:
            self.rest_server.stop()
        except AttributeError as error_msg:
            print(f"ERROR: {error_msg}")


class Mgmt:
    def __init__(self, service=None):
        self.service = service
        self.db = Database()
        self.db.set("nodes", {})
        self.db.set("depth_caches", {})
        self.db.set("depth_cache_distribution", {})

    def main(self):
        self.service.rest_server = RestServer.RestServer(app_class=self.service.app_class, endpoints=RestEndpoints)
        self.service.rest_server.start()
        while self.service.app_class.is_shutdown() is False:
            print(f"Hallo Olli! @ {self.service.app_class.app_name} - {time.time()}")
            time.sleep(5)
            self.service.app_class.stdout_msg(f"Loop finished ...", log="info")