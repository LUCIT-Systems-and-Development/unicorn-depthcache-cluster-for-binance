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

from .Database import Database
from lucit_ubdcc_shared_modules.RestEndpointsBase import RestEndpointsBase, Request


class RestEndpoints(RestEndpointsBase):
    def __init__(self, app=None):
        super().__init__(app=app)
        self.db: Database = self.app.data['db']

    def register(self):
        super().register()

        @self.fastapi.get("/create_depthcache")
        async def create_depthcache(request: Request):
            # Todo: Manage DB to create the DepthCache on a DepthCacheNode
            return {"event": "CREATE_DEPTHCACHE",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_cluster_info")
        async def get_cluster_info(request: Request):
            return await self.get_cluster_info(request=request)

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
            return await self.ubdcc_node_cancellation(request=request)

        @self.fastapi.get("/ubdcc_node_registration")
        async def ubdcc_node_registration(request: Request):
            return await self.ubdcc_node_registration(request=request)

        @self.fastapi.get("/ubdcc_node_sync")
        async def ubdcc_node_sync(request: Request):
            return await self.ubdcc_node_sync(request=request)

    async def get_cluster_info(self, request: Request):
        response = {"db": {"depthcaches": self.db.get('depthcaches'),
                           "depthcache_distribution": self.db.get('depthcache_distribution'),
                           "nodes": self.db.get('nodes'),
                           "pods": self.db.get('pods')},
                    "version": self.app.get_version()}
        return self.get_ok_response(event="GET_CLUSTER_INFO", params=response)

    async def ubdcc_node_cancellation(self, request: Request):
        uid = request.query_params.get("uid")
        if not uid:
            return self.get_error_response(event="UBDCC_NODE_CANCELLATION",
                                           message="Missing required parameter: uid")
        if not self.db.exists_pod(uid=uid):
            return self.get_error_response(event="UBDCC_NODE_CANCELLATION",
                                           message=f"A pod with the uid '{uid}' does not exist!")
        # Todo: Tasks to remove the pod (restructuring DC distribution)
        result = self.db.delete_pod(uid=uid)
        if result is True:
            return self.get_ok_response(event="UBDCC_NODE_CANCELLATION")
        else:
            return self.get_error_response(event="UBDCC_NODE_CANCELLATION", message="An unknown error has occurred!")

    async def ubdcc_node_registration(self, request: Request):
        name = request.query_params.get("name")
        uid = request.query_params.get("uid")
        node = request.query_params.get("node")
        role = request.query_params.get("role")
        api_port_rest = request.query_params.get("api_port_rest")
        status = request.query_params.get("status")
        if not name or not uid or not node or not role or not api_port_rest or not status:
            return self.get_error_response(event="UBDCC_NODE_CANCELLATION",
                                           message="Missing required parameter: name, uid, node, role, api_port_rest, "
                                                   "status")
        if self.db.exists_pod(uid=uid):
            return self.get_error_response(event="UBDCC_NODE_REGISTRATION",
                                           message=f"A pod with the uid '{uid}' already exists!")
        result = self.db.add_pod(name=name,
                                 uid=uid,
                                 node=node,
                                 role=role,
                                 ip=request.client.host,
                                 api_port_rest=api_port_rest,
                                 status=status)
        if result is True:
            return self.get_ok_response(event="UBDCC_NODE_REGISTRATION")
        else:
            return self.get_error_response(event="UBDCC_NODE_REGISTRATION", message="An unknown error has occurred!")

    async def ubdcc_node_sync(self, request: Request):
        uid = request.query_params.get("uid")
        node = request.query_params.get("node")
        status = request.query_params.get("status")
        if not self.db.exists_pod(uid=uid):
            return self.get_error_response(event="UBDCC_NODE_SYNC", message=f"Registration for pod '{uid}' not found!")
        result = self.db.update_pod(uid=uid,
                                    node=node,
                                    ip=request.client.host,
                                    status=status)
        if result is True:
            return self.get_ok_response(event="UBDCC_NODE_SYNC")
        else:
            return self.get_error_response(event="UBDCC_NODE_SYNC", message="An unknown error has occurred!")
