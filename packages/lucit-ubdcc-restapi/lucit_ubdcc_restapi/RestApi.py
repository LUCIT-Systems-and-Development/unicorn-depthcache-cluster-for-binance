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

from .RestEndpoints import RestEndpoints
from lucit_ubdcc_shared_modules.ServiceBase import ServiceBase


class RestApi(ServiceBase):
    def __init__(self, cwd=None):
        super().__init__(app_name="lucit-ubdcc-restapi", cwd=cwd)

    async def main(self):
        await self.start_rest_server(endpoints=RestEndpoints)
        self.app.set_status_running()
        await self.app.register_or_restart()
        self.db_init()
        while self.app.is_shutdown() is False:
            await self.app.sleep()
            await self.app.ubdcc_node_sync()
