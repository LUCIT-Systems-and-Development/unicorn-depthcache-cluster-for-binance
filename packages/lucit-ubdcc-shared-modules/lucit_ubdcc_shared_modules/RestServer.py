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
    def __init__(self, app=None, endpoints=None):
        super().__init__()
        self.app = app
        self.endpoints = endpoints(app=self.app)
        self.endpoints.register()
        LOGGING_CONFIG["formatters"]["access"]["fmt"] = f"%(asctime)s {LOGGING_CONFIG['formatters']['access']['fmt']}"
        self.uvicorn = uvicorn.Server(uvicorn.Config(self.app.get_fastapi_instance(),
                                                     host="0.0.0.0",
                                                     port=self.app.rest_server_port))

    def run(self) -> None:
        self.app.stdout_msg(f"Starting REST Server ...", log="info")
        try:
            self.uvicorn.run()
        except (ConnectionError, HTTPException) as error_msg:
            self.app.stdout_msg(f"ERROR: {error_msg}", log="critical")
        return None

    def stop(self) -> bool:
        self.app.stdout_msg(f"Stopping REST Server ...", log="info")
        self.uvicorn.should_exit = True
        return True
