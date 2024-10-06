#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-restapi/lucit_ubdcc_restapi/RestEndpoints.py
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
    def __init__(self, app=None):
        super().__init__(app=app)

    def register(self):
        super().register()

        @self.fastapi.get("/create_depthcache")
        async def create_depthcache(request: Request):
            # Todo: Manage DB to create the DepthCache on a DepthCacheNode
            return {"event": "CREATE_DEPTHCACHE",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_asks")
        async def get_asks(request: Request):
            # Todo: Return information about the UBDCC
            return {"event": "GET_ASKS",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_bids")
        async def get_bids(request: Request):
            # Todo: Return information about the UBDCC
            return {"event": "GET_BIDS",
                    "result": "NOT_IMPLEMENTED"}

        @self.fastapi.get("/get_cluster_info")
        async def get_cluster_info(request: Request):
            return await self.get_cluster_info(request=request)

        @self.fastapi.get("/get_depthcache_list")
        async def get_depthcache_list(request: Request):
            return await self.get_depthcache_list(request=request)

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

        @self.fastapi.get("/submit_license")
        async def submit_license(request: Request):
            return await self.submit_license(request=request)

    async def get_cluster_info(self, request: Request):
        endpoint = "/get_cluster_info"
        host = self.app.get_cluster_mgmt_address()
        url = host + endpoint
        result = self.app.request(url=url, method="get")
        if result.get('error') is None and result.get('error_id') is None:
            return result
        else:
            response = self.create_cluster_info_response()
            response['error'] = str(result)
            if self.app.data.get('db') is None:
                return self.get_error_response(event="GET_CLUSTER_INFO", error_id="#1012",
                                               message=f"Mgmt service not available!",
                                               params=response)
            else:
                return self.get_error_response(event="GET_CLUSTER_INFO", error_id="#1013",
                                               message=f"Mgmt service not available! This is cached data from pod "
                                                       f"'{self.app.id['uid']}'!",
                                               params=response)

    async def get_depthcache_list(self, request: Request):
        return self.app.data['db-rest']['depthcaches']

    async def submit_license(self, request: Request):
        api_secret = request.query_params.get("api_secret")
        license_token = request.query_params.get("license_token")
        endpoint = "/submit_license"
        host = self.app.get_cluster_mgmt_address()
        query = (f"?api_secret={api_secret}&"
                 f"license_token={license_token}")
        url = host + endpoint + query
        return self.app.request(url=url, method="get")
