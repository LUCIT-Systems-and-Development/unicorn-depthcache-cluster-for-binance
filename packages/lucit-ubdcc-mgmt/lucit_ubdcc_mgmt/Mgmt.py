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

from .Database import Database
from .RestEndpoints import RestEndpoints
from lucit_ubdcc_shared_modules.ServiceBase import ServiceBase


class Mgmt(ServiceBase):
    def __init__(self, cwd=None):
        self.db = None
        super().__init__(app_name="lucit-ubdcc-mgmt", cwd=cwd)

    def db_init(self) -> bool:
        self.app.stdout_msg(f"Starting database ...", log="info")
        if self.db is None:
            self.db = Database(app=self.app)
            return True
        return False

    def main(self):
        self.db_init()
        self.start_rest_server(endpoints=RestEndpoints)
        self.db.add_pod(name="testname1",
                        uid="USAIDFJSDLFJ23323wsfdsfDF",
                        node="A",
                        role="rolle",
                        ip="1.1.1.1",
                        api_port=42930,
                        last_seen="now",
                        status="OK")
        self.db.add_pod(name="testname2",
                        uid="safdSAIDFJSDLFJ23323ws3221fdsfDF",
                        node="A",
                        role="rolle",
                        ip="1.1.1.2",
                        api_port=42940,
                        last_seen="now",
                        status="OK")
        self.app.stdout_msg(f"PODS: {self.db.get('pods')}")
        self.db.delete_pod(uid="USAIDFJSDLFJ23323wsfdsfDF")
        self.app.stdout_msg(f"PODS: {self.db.get('pods')}")
        while self.app.is_shutdown() is False:
            self.app.stdout_msg(f"Starting cronjobs ...", log="info")
            self.app.stdout_msg(f"Updating DB key 'nodes' ...", log="info")
            self.db.update_nodes()
            self.app.stdout_msg(self.db.get("nodes"), log="info")
            self.app.stdout_msg(f"Finished cronjobs!")
            self.app.sleep(seconds=30)
