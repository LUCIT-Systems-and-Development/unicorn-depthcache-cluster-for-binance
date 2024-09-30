#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/generic_loader/lucit_ubdcc_mgmt/Mgmt.py
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
import socket
import time
from .RestEndpoints import RestEndpoints
from lucit_ubdcc_shared_modules.AppClass import AppClass
from lucit_ubdcc_shared_modules.RestServer import RestServer


class Service:
    def __init__(self, cwd=None):
        self.app_class = AppClass(app_name="lucit-ubdcc-mgmt", cwd=cwd, service_call=self.run, stop_call=self.stop)
        self.app_class.start()
        self.rest_server = None

    def run(self):
        self.rest_server = RestServer(app_class=self.app_class, endpoints=RestEndpoints)
        self.rest_server.start()

        while self.app_class.is_shutdown() is False:
            print(f"Hallo Olli @ {time.time()}")
            time.sleep(2)
            self.app_class.stdout_msg(f"Loop finished ...", log="info")

    def stop(self):
        self.rest_server.stop()
