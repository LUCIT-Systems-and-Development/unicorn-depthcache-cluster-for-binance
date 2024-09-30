#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/RestServer.py
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
import uvicorn
from fastapi import HTTPException
from uvicorn.config import LOGGING_CONFIG


class RestServer(threading.Thread):
    def __init__(self, app_class=None, endpoints=None):
        super().__init__()
        self.app_class = app_class
        self.endpoints = endpoints(app_class=self.app_class)
        self.endpoints.register()
        LOGGING_CONFIG["formatters"]["access"]["fmt"] = f"%(asctime)s {LOGGING_CONFIG['formatters']['access']['fmt']}"
        self.uvicorn = uvicorn.Server(uvicorn.Config(self.app_class.get_fastapi_instance(), host="0.0.0.0", port=8080))

    def run(self):
        print(f"# Starting REST Server ...")
        try:
            self.uvicorn.run()
        except (ConnectionError, HTTPException) as error_msg:
            self.app_class.stdout_msg(f"# ERROR: {error_msg}", log="critical")

    def stop(self):
        print(f"# Stopping REST Server ...")
        self.uvicorn.should_exit = True
