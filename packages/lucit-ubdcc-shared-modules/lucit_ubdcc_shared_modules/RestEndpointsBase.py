#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/RestEndpointsBase.py
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

from fastapi import Request


class RestEndpointsBase:
    def __init__(self, app_class=None):
        self.app_class = app_class
        self.fastapi = app_class.fastapi

    def get_fastapi_instance(self):
        return self.fastapi

    def register(self):
        self.app_class.stdout_msg(f"# Registering REST endpoints ...", log="info")

        @self.fastapi.get("/test")
        async def test(request: Request):
            return {"message": f"Hello World!",
                    "headers": f"{request.headers}",
                    "app": f"{self.app_class.app}"}
