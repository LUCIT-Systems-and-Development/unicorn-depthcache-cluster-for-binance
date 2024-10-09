#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-dcn/lucit_ubdcc_dcn/RestEndpoints.py
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
from unicorn_binance_local_depth_cache import DepthCacheOutOfSync


class RestEndpoints(RestEndpointsBase):
    def __init__(self, app=None):
        super().__init__(app=app)

    def register(self):
        super().register()

        @self.fastapi.get("/get_asks")
        async def get_asks(request: Request):
            return await self.get_asks(request=request)

        @self.fastapi.get("/get_bids")
        async def get_bids(request: Request):
            return await self.get_bids(request=request)

    async def get_asks(self, request: Request):
        event = "GET_ASKS"
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        limit_count = request.query_params.get("limit_count")
        threshold_volume = request.query_params.get("threshold_volume")
        if limit_count is None or limit_count == "None":
            limit_count = None
        else:
            limit_count = int(limit_count)
        if threshold_volume is None or threshold_volume == "None":
            threshold_volume = None
        else:
            threshold_volume = float(threshold_volume)
        for dc in self.app.data['local_depthcaches']:
            if dc['exchange'] == exchange and dc['market'] == market:
                try:
                    asks = self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].get_asks(market=dc['market'],
                                                                                                                 limit_count=limit_count,
                                                                                                                 threshold_volume=threshold_volume)
                except DepthCacheOutOfSync:
                    return self.get_error_response(event=event, error_id="#1026",
                                                   message=f"DepthCache with market '{market}' for '{exchange}' not "
                                                           f"found!")
                return self.get_ok_response(event=event, params={"asks": asks})
        return self.get_error_response(event=event, error_id="#7000", message=f"DepthCache '{market}' for '{exchange}'"
                                                                              f" not found!")

    async def get_bids(self, request: Request):
        event = "GET_BIDS"
        exchange = request.query_params.get("exchange")
        market = request.query_params.get("market")
        limit_count = request.query_params.get("limit_count")
        threshold_volume = request.query_params.get("threshold_volume")
        if limit_count is None or limit_count == "None":
            limit_count = None
        else:
            limit_count = int(limit_count)
        if threshold_volume is None or threshold_volume == "None":
            threshold_volume = None
        else:
            threshold_volume = float(threshold_volume)
        for dc in self.app.data['local_depthcaches']:
            if dc['exchange'] == exchange and dc['market'] == market:
                try:
                    bids = self.app.data['depthcache_instances'][dc['exchange']][dc['update_interval']].get_bids(market=dc['market'],
                                                                                                                 limit_count=limit_count,
                                                                                                                 threshold_volume=threshold_volume)
                except DepthCacheOutOfSync:
                    return self.get_error_response(event=event, error_id="#1026",
                                                   message=f"DepthCache with market '{market}' for '{exchange}' not "
                                                           f"found!")
                return self.get_ok_response(event=event, params={"bids": bids})
        return self.get_error_response(event=event, error_id="#7000", message=f"DepthCache '{market}' for '{exchange}'"
                                                                              f" not found!")

