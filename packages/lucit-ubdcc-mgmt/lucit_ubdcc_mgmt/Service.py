#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/generic_loader/lucit_ubdcc_mgmt/Service.py
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
from lucit_ubdcc_shared_modules.AppClass import AppClass


class Service:
    def __init__(self, cwd=None):
        self.app_class = AppClass(app_name="lucit-ubdcc-mgmt", cwd=cwd, service_call=self.run)
        self.app_class.start()

    def run(self):
        service_name = f"{self.app_class.app_name}lucit-ubdcc.svc.cluster.local"
        while self.app_class.is_shutdown() is False:
            try:
                service_ip = socket.gethostbyname(service_name)
            except socket.gaierror:
                service_ip = "unknown"
            print(f"Hallo Olli @ {service_ip} {time.time()}")
            time.sleep(10)
            self.app_class.stdout_msg(f"Loop finished ...", log="info")
