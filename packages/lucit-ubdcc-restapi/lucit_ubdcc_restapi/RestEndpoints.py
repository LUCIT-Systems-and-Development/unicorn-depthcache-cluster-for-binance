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
import time


class RestEndpoints(RestEndpointsBase):
    def __init__(self, app=None):
        super().__init__(app=app)

    def register(self):
        super().register()

        @self.fastapi.get("/create_depthcache")
        async def create_depthcache(request: Request):
            return await self.create_depthcache(request=request)

        @self.fastapi.get("/create_depthcaches")
        async def create_depthcaches(request: Request):
            return await self.create_depthcaches(request=request)

        @self.fastapi.get("/get_asks")
        async def get_asks(request: Request):
            return await self.get_asks(request=request)

        @self.fastapi.get("/get_bids")
        async def get_bids(request: Request):
            return await self.get_bids(request=request)

        @self.fastapi.get("/get_cluster_info")
        async def get_cluster_info(request: Request):
            return await self.get_cluster_info(request=request)

        @self.fastapi.get("/get_depthcache_list")
        async def get_depthcache_list(request: Request):
            return await self.get_depthcache_list(request=request)

        @self.fastapi.get("/get_depthcache_info")
        async def get_depthcache_info(request: Request):
            return await self.get_depthcache_info(request=request)

        @self.fastapi.get("/stop_depthcache")
        async def stop_depthcache(request: Request):
            return await self.stop_depthcache(request=request)

        @self.fastapi.get("/submit_license")
        async def submit_license(request: Request):
            return await self.submit_license(request=request)

    async def _get_depthcache_data(self, request: Request, event=None, endpoint=None):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" \
            else None
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        request_url = str(request.url)
        responsible_dcn = await self.app.ubdcc_get_responsible_dcn_addresses(exchange=exchange, market=market)
        limit_count = request.query_params.get("limit_count")
        threshold_volume = request.query_params.get("threshold_volume")
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        if responsible_dcn is None:
            if not exchange or not market:
                return self.get_error_response(event=event, error_id="#1025", process_start_time=process_start_time,
                                               message="Missing required parameter: exchange, market",
                                               url=request_url, used_pods=used_pods)
            addresses = self.app.data['db'].get_responsible_dcn_addresses(exchange=exchange, market=market)
        else:
            addresses = responsible_dcn['addresses']
        if len(addresses) == 0:
            if self.app.data['db'].exists_depthcache(exchange=exchange, market=market):
                return self.get_error_response(event=event, error_id="#4000", process_start_time=process_start_time,
                                               message=f"No DCN found for '{market}' on '{exchange}'!",
                                               url=request_url, used_pods=used_pods)
            else:
                return self.get_error_response(event=event, error_id="#7000", process_start_time=process_start_time,
                                               message=f"DepthCache '{market}' for '{exchange}' not found!",
                                               url=request_url, used_pods=used_pods)
        query = (f"?exchange={exchange}&"
                 f"market={market}&"
                 f"limit_count={limit_count}&"
                 f"threshold_volume={threshold_volume}")
        result_errors = []
        for address, port in addresses:
            self.app.stdout_msg(f"Connecting http://{address}:{port}/{endpoint}{query} ...")
            url = f"http://{address}:{port}" + endpoint + query
            result = await self.app.request(url=url, method="get")
            if result.get('error') is None and result.get('error_id') is None:
                if str(request.query_params.get("debug")).lower() == "true":
                    pod = self.app.data['db'].get_pod_by_address(address=address)
                    used_pods.append([pod.get('NAME'), pod.get('UID')])
                    result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                                 url=request_url, used_pods=used_pods)
                return result
            result_errors.append([address, port, str(result)])
        self.app.stdout_msg(f"No DCN has responded to the request: {result_errors}")
        return self.get_error_response(event=event, error_id="#5000", message=f"No DCN has responded to the request!",
                                       params={"requests": result_errors}, process_start_time=process_start_time,
                                       url=request_url, used_pods=used_pods)

    async def create_depthcache(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "CREATE_DEPTHCACHE"
        endpoint = "/create_depthcache"
        request_url = str(request.url)
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        host = self.app.get_cluster_mgmt_address()
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        desired_quantity = request.query_params.get("desired_quantity")
        update_interval = request.query_params.get("update_interval")
        refresh_interval = request.query_params.get("refresh_interval")
        query = (f"?exchange={exchange}&"
                 f"market={market}&"
                 f"update_interval={update_interval}&"
                 f"refresh_interval={refresh_interval}&"
                 f"desired_quantity={desired_quantity}")
        url = host + endpoint + query
        result = await self.app.request(url=url, method="get")
        if result.get('error') is not None and result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                           params={"error": str(result)}, process_start_time=process_start_time,
                                           url=request_url, used_pods=used_pods)
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'), message=result.get('message'),
                                           process_start_time=process_start_time, url=request_url, used_pods=used_pods)
        else:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result

    async def create_depthcaches(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "CREATE_DEPTHCACHES"
        endpoint = "/create_depthcaches"
        request_url = str(request.url)
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        host = self.app.get_cluster_mgmt_address()
        exchange = request.query_params.get("exchange")
        markets = request.query_params.get("markets")
        desired_quantity = request.query_params.get("desired_quantity")
        update_interval = request.query_params.get("update_interval")
        refresh_interval = request.query_params.get("refresh_interval")
        query = (f"?exchange={exchange}&"
                 f"markets={markets}&"
                 f"update_interval={update_interval}&"
                 f"refresh_interval={refresh_interval}&"
                 f"desired_quantity={desired_quantity}")
        url = host + endpoint + query
        result = await self.app.request(url=url, method="get")
        if result.get('error') is not None and result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                           params={"error": str(result)}, process_start_time=process_start_time,
                                           url=request_url, used_pods=used_pods)
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'), message=result.get('message'),
                                           url=request_url, process_start_time=process_start_time, used_pods=used_pods)
        else:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result

    async def get_asks(self, request: Request):
        event = "GET_ASKS"
        endpoint = "/get_asks"
        return await self._get_depthcache_data(request=request, event=event, endpoint=endpoint)

    async def get_bids(self, request: Request):
        event = "GET_BIDS"
        endpoint = "/get_bids"
        return await self._get_depthcache_data(request=request, event=event, endpoint=endpoint)

    async def get_cluster_info(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "GET_CLUSTER_INFO"
        endpoint = "/get_cluster_info"
        request_url = str(request.url)
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        host = self.app.get_cluster_mgmt_address()
        url = host + endpoint
        result = await self.app.request(url=url, method="get")
        if result.get('error') is None and result.get('error_id') is None:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'), message=result.get('message'),
                                           process_start_time=process_start_time, url=request_url, used_pods=used_pods)
        else:
            response = self.create_cluster_info_response()
            response['error'] = str(result)
            if self.app.data.get('db') is None:
                return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)
            else:
                return self.get_error_response(event=event, error_id="#8000",
                                               message=f"Mgmt service not available! This is cached data from pod "
                                                       f"'{self.app.id['uid']}'!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)

    async def get_depthcache_list(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "GET_DEPTHCACHE_LIST"
        endpoint = "/get_depthcache_list"
        request_url = str(request.url)
        host = self.app.get_cluster_mgmt_address()
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        url = host + endpoint
        result = await self.app.request(url=url, method="get")
        if result.get('error') is None and result.get('error_id') is None:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'), message=result.get('message'),
                                           process_start_time=process_start_time, url=request_url, used_pods=used_pods)
        else:
            response = self.create_depthcache_list_response()
            response['error'] = str(result)
            if self.app.data.get('db') is None:
                return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)
            else:
                return self.get_error_response(event=event, error_id="#8000",
                                               message=f"Mgmt service not available! This is cached data from pod "
                                                       f"'{self.app.id['uid']}'!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)

    async def get_depthcache_info(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "GET_DEPTHCACHE_INFO"
        endpoint = "/get_depthcache_info"
        request_url = str(request.url)
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        host = self.app.get_cluster_mgmt_address()
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        query = (f"?exchange={exchange}&"
                 f"market={market}")
        url = host + endpoint + query
        result = await self.app.request(url=url, method="get")
        if result.get('error') is None and result.get('error_id') is None:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'),
                                           message=result.get('message'), process_start_time=process_start_time,
                                           url=request_url, used_pods=used_pods)
        else:
            response = self.create_depthcache_info_response(exchange=exchange, market=market)
            response['error'] = str(result)
            if self.app.data.get('db') is None:
                return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)
            else:
                return self.get_error_response(event=event, error_id="#8000",
                                               message=f"Mgmt service not available! This is cached data from pod "
                                                       f"'{self.app.id['uid']}'!",
                                               params=response, process_start_time=process_start_time,
                                               url=request_url, used_pods=used_pods)

    async def stop_depthcache(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "STOP_DEPTHCACHE"
        endpoint = "/stop_depthcache"
        request_url = str(request.url)
        host = self.app.get_cluster_mgmt_address()
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        query = (f"?exchange={exchange}&"
                 f"market={market}")
        url = host + endpoint + query
        result = await self.app.request(url=url, method="get")
        if result.get('error') is None and result.get('error_id') is None:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result
        elif result.get('error_id') is not None:
            return self.get_error_response(event=event, error_id=result.get('error_id'), message=result.get('message'),
                                           process_start_time=process_start_time, url=request_url, used_pods=used_pods)
        else:
            return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                           params={"error": str(result)}, process_start_time=process_start_time,
                                           url=request_url, used_pods=used_pods)

    async def submit_license(self, request: Request):
        process_start_time: float | None = time.time() if str(request.query_params.get("debug")).lower() == "true" else None
        event = "SUBMIT_LICENSE"
        request_url = str(request.url)
        used_pods: list = [[self.app.id['name'], self.app.id['uid']]]
        api_secret = request.query_params.get("api_secret")
        license_token = request.query_params.get("license_token")
        endpoint = "/submit_license"
        host = self.app.get_cluster_mgmt_address()
        query = (f"?api_secret={api_secret}&"
                 f"license_token={license_token}")
        url = host + endpoint + query
        result = await self.app.request(url=url, method="get")
        if result.get('error') is None:
            if str(request.query_params.get("debug")).lower() == "true":
                result['debug'] = self.create_debug_response(process_start_time=process_start_time,
                                                             url=request_url, used_pods=used_pods)
            return result
        else:
            return self.get_error_response(event=event, error_id="#9000", message=f"Mgmt service not available!",
                                           params={"error": str(result)}, process_start_time=process_start_time,
                                           url=request_url, used_pods=used_pods)
