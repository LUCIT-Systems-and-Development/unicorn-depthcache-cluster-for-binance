#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/RestEndpoints.py
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

from lucit_ubdcc_shared_modules.RestEndpointsBase import RestEndpointsBase, Request


class RestEndpoints(RestEndpointsBase):
    def __init__(self, app_class=None):
        super().__init__(app_class=app_class)

    def register(self):
        super().register()

        @self.fastapi.get("/create_depthcache")
        async def create_depthcache(request: Request):
            # Todo: Manage DB to create the DepthCache on a DepthCacheNode
            return {"event": "CREATE_DEPTHCACHE",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_cluster_info")
        async def get_cluster_info(request: Request):
            # Todo: Return information about the UBDCC
            return {"event": "GET_CLUSTER_INFO",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_depthcache_list")
        async def get_depthcache_list(request: Request):
            # Todo: Return a list of all DepthCaches
            return {"event": "GET_DEPTHCACHE_LIST",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_depthcache_status")
        async def get_depthcache_status(request: Request):
            # Todo: Return the status of the DepthCache
            return {"event": "GET_DEPTHCACHE_STATUS",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/stop_depthcache")
        async def stop_depthcache(request: Request):
            # Todo: Manage DB to stop the DepthCache
            return {"event": "STOP_DEPTHCACHE",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/ubdcc_node_cancellation")
        async def ubdcc_node_cancellation(request: Request):
            # Todo: Manage Db and remove the node
            return {"event": "UBDCC_NODE_CANCELLATION",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/ubdcc_node_registration")
        async def ubdcc_node_registration(request: Request):
            # Todo: Manage Db and add the node
            return {"event": "UBDCC_NODE_REGISTRATION",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/ubdcc_node_sync")
        async def ubdcc_node_sync(request: Request):
            # Todo: Manage Db and update the node (take and give!)
            return {"event": "UBDCC_NODE_SYNC",
                    "result": "NOT_IMPLEMENTED"}