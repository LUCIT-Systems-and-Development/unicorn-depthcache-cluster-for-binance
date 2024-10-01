#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-restapi/lucit_ubdcc_restapi/RestApi.py
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
from .RestEndpoints import RestEndpoints
from lucit_ubdcc_shared_modules.Service import Service


class RestApi(Service):
    def __init__(self, cwd=None):
        super().__init__(app_name="lucit-ubdcc-restapi", cwd=cwd)

    def main(self):
        self.start_rest_server(endpoints=RestEndpoints)
        while self.app_class.is_shutdown() is False:
            print(f"Hallo Olli! @ {self.app_class.app_name} - {time.time()}")
            time.sleep(5)
            self.app_class.stdout_msg(f"Loop finished ...", log="info")
