#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/ServiceBase.py
#
# Project website: https://www.lucit.tech/unicorn-binance-depthcache-cluster.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster
# Documentation: https://unicorn-binance-depthcache-cluster.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-ubdcc-shared-modules
# LUCIT Online Shop: https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import asyncio
from .App import App
from .RestServer import RestServer


class ServiceBase:
    def __init__(self, app_name=None, cwd=None):
        self.rest_server = None
        self.app = App(app_name=app_name,
                       cwd=cwd,
                       service_call=self.run,
                       stop_call=self.stop)
        self.app.start()

    async def main(self) -> None:
        # Override with specific Service main() function
        pass

    def run(self) -> None:
        self.app.stdout_msg(f"Starting the main execution flow ...", log="debug", stdout=False)
        asyncio.run(self.main())

    def start_rest_server(self, endpoints=None) -> bool:
        self.rest_server = RestServer(app=self.app, endpoints=endpoints)
        self.rest_server.start()
        return True

    def stop(self) -> bool:
        try:
            self.rest_server.stop()
            return True
        except AttributeError as error_msg:
            self.app.stdout_msg(f"ERROR: {error_msg}", log="info")
        return False
