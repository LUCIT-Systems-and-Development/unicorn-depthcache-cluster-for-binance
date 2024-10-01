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
from lucit_ubdcc_shared_modules.Service import Service


class Mgmt(Service):
    def __init__(self, cwd=None):
        self.db = None
        super().__init__(app_name="lucit-ubdcc-mgmt", cwd=cwd)

    def db_init(self) -> bool:
        print(f"# Init Database ...")
        if self.db is None:
            self.db = Database()
            # Todo:
            #   1. Load Backup if available

            # Init variables
            self.db.set("nodes", {})
            self.db.set("depth_caches", {})
            self.db.set("depth_cache_distribution", {})
            return True
        return False

    def main(self):
        self.db_init()
        self.start_rest_server(endpoints=RestEndpoints)
        while self.app_class.is_shutdown() is False:
            print(f"Hallo Olli! @ {self.app_class.app_name} - {time.time()}")
            time.sleep(5)
            self.app_class.stdout_msg(f"Loop finished ...", log="info")
