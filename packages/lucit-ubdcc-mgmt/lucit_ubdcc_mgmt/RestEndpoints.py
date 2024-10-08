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

from lucit_ubdcc_shared_modules.Database import Database
from lucit_ubdcc_shared_modules.RestEndpointsBase import RestEndpointsBase, Request


class RestEndpoints(RestEndpointsBase):
    def __init__(self, app=None):
        super().__init__(app=app)
        self.db: Database = self.app.data['db']

    def register(self):
        super().register()

        @self.fastapi.get("/create_depthcache")
        async def create_depthcache(request: Request):
            return await self.create_depthcache(request=request)

        @self.fastapi.get("/get_cluster_info")
        async def get_cluster_info(request: Request):
            return await self.get_cluster_info(request=request)

        @self.fastapi.get("/stop_depthcache")
        async def stop_depthcache(request: Request):
            return await self.stop_depthcache(request=request)

        @self.fastapi.get("/submit_license")
        async def submit_license(request: Request):
            return await self.submit_license(request=request)

        @self.fastapi.get("/ubdcc_node_cancellation")
        async def ubdcc_node_cancellation(request: Request):
            return await self.ubdcc_node_cancellation(request=request)

        @self.fastapi.get("/ubdcc_node_registration")
        async def ubdcc_node_registration(request: Request):
            return await self.ubdcc_node_registration(request=request)

        @self.fastapi.get("/ubdcc_node_sync")
        async def ubdcc_node_sync(request: Request):
            return await self.ubdcc_node_sync(request=request)

    async def create_depthcache(self, request: Request):
        event = "CREATE_DEPTHCACHE"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange")
        symbol = request.query_params.get("symbol")
        desired_quantity = request.query_params.get("desired_quantity")
        update_interval = request.query_params.get("update_interval")
        if desired_quantity is None or desired_quantity == "None":
            desired_quantity = 1
        else:
            desired_quantity = int(desired_quantity)
        if update_interval is None or update_interval == "None":
            update_interval = None
        else:
            update_interval = int(update_interval)
        if not exchange or not symbol:
            return self.get_error_response(event=event, error_id="#1016",
                                           message="Missing required parameter: exchange, symbol")
        if self.db.exists_depthcache(exchange=exchange, symbol=symbol):
            return self.get_error_response(event=event, error_id="#1024",
                                           message=f"A DepthCache for exchange '{exchange}' and symbol '{symbol}' "
                                                   f"already exists!")
        try:
            result = self.db.add_depthcache(exchange=exchange, symbol=symbol, update_interval=update_interval,
                                            desired_quantity=desired_quantity)
        except ValueError as error_msg:
            return self.get_error_response(event=event, error_id="#1017", message=str(error_msg))
        if result is True:
            used_dcn = []
            for _ in range(0, desired_quantity):
                best_dcn = self.db.get_best_dcn(excluded_pods=used_dcn)
                if best_dcn is not None:
                    self.db.add_depthcache_distribution(exchange=exchange, symbol=symbol, pod_uid=best_dcn)
                    used_dcn.append(best_dcn)
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1018", message="An unknown error has occurred!")

    async def get_cluster_info(self, request: Request):
        event = "GET_CLUSTER_INFO"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        response = self.create_cluster_info_response()
        return self.get_ok_response(event=event, params=response)

    async def stop_depthcache(self, request: Request):
        event = "STOP_DEPTHCACHE"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange")
        symbol = request.query_params.get("symbol")
        if not exchange or not symbol:
            return self.get_error_response(event=event, error_id="#1019",
                                           message="Missing required parameter: exchange, symbol")
        try:
            result = self.db.delete_depthcache(exchange=exchange, symbol=symbol)
        except ValueError as error_msg:
            return self.get_error_response(event=event, error_id="#1020", message=str(error_msg))
        if result is True:
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1021", message="An unknown error has occurred!")

    async def submit_license(self, request: Request):
        event = "SUBMIT_LICENSE"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        api_secret = request.query_params.get("api_secret")
        license_token = request.query_params.get("license_token")
        if not api_secret or not license_token:
            return self.get_error_response(event=event, error_id="#1007",
                                           message="Missing required parameter: api_secret, license_token")
        self.db.submit_license(api_secret=api_secret, license_token=license_token)
        if self.db.get_license_status() == "VALID":
            self.app.llm.close()
        if self.app.start_licensing_manager():
            return self.get_ok_response(event=event,
                                        params={"message": "The license has been successfully validated and UBDCC "
                                                           "is now ready for operation! Have fun! ;)"})
        return self.get_error_response(event=event, error_id="#1011", message="The license is invalid!")

    async def ubdcc_node_cancellation(self, request: Request):
        event = "UBDCC_NODE_CANCELLATION"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        uid = request.query_params.get("uid")
        if not uid:
            return self.get_error_response(event=event, error_id="#1004", message="Missing required parameter: uid")
        if not self.db.exists_pod(uid=uid):
            return self.get_error_response(event=event, error_id="#1005",
                                           message=f"A pod with the uid '{uid}' does not exist!")
        result = self.db.delete_pod(uid=uid)
        if result is True:
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1008", message="An unknown error has occurred!")

    async def ubdcc_node_registration(self, request: Request):
        event = "UBDCC_NODE_REGISTRATION"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        name = request.query_params.get("name")
        uid = request.query_params.get("uid")
        node = request.query_params.get("node")
        role = request.query_params.get("role")
        api_port_rest = request.query_params.get("api_port_rest")
        status = request.query_params.get("status")
        version = request.query_params.get("version")
        if not name or not uid or not node or not role or not api_port_rest or not status:
            return self.get_error_response(event=event, error_id="#1002",
                                           message="Missing required parameter: name, uid, node, role, api_port_rest, "
                                                   "status")
        if self.db.exists_pod(uid=uid):
            return self.get_error_response(event=event, error_id="#1003",
                                           message=f"A pod with the uid '{uid}' already exists!")
        result = self.db.add_pod(name=name,
                                 uid=uid,
                                 node=node,
                                 role=role,
                                 ip=request.client.host,
                                 api_port_rest=int(api_port_rest),
                                 status=status,
                                 version=version)
        if result is True:
            self.app.send_backup_to_node(host=request.client.host, port=api_port_rest)
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1009", message="An unknown error has occurred!")

    async def ubdcc_node_sync(self, request: Request):
        event = "UBDCC_NODE_SYNC"
        uid = request.query_params.get("uid")
        node = request.query_params.get("node")
        api_port_rest = request.query_params.get("api_port_rest")
        status = request.query_params.get("status")
        if not uid or not api_port_rest:
            return self.get_error_response(event=event, error_id="#1000",
                                           message="Missing required parameter: uid, api_port_rest")
        if not self.db.exists_pod(uid=uid) and self.db.is_empty() is True:
            backup = self.app.get_backup_from_node(host=request.client.host, port=api_port_rest)
            if backup is not None:
                source_ip = request.client.host
                source_port = api_port_rest
                source_uid = uid
                timestamp_limit = float(backup['timestamp'])
                pods = []
                for pod in backup['pods']:
                    pods.append(backup['pods'][pod]['UID'])
                    timestamp = self.app.get_backup_timestamp_from_node(host=backup['pods'][pod]['IP'],
                                                                        port=backup['pods'][pod]['API_PORT_REST'])
                    if timestamp is not None:
                        if timestamp_limit < timestamp:
                            source_ip = pod['IP']
                            source_port = pod['API_PORT_REST']
                            source_uid = pod['UID']
                            timestamp_limit = timestamp
                self.app.stdout_msg(f"Found pods: {pods}", log="info")
                if source_uid != uid:
                    backup = self.app.get_backup_from_node(host=source_ip, port=source_port)
                if backup is not None:
                    self.db.replace_data(data=backup)
                    if self.db.get_license_status() == "VALID":
                        if self.app.start_licensing_manager() is False:
                            self.db.set_license_status(status="INVALID")
                    self.app.data['is_ready'] = True
                    self.app.stdout_msg(f"Loaded database from pod '{source_uid}'!", log="info")
        if not self.db.exists_pod(uid=uid):
            return self.get_error_response(event=event, error_id="#1001",
                                           message=f"Registration for pod '{uid}' not found!")

        result = self.db.update_pod(uid=uid,
                                    node=node,
                                    ip=request.client.host,
                                    status=status)
        pod = self.db.get_pod_by_uid(uid=uid)
        if result is True:
            self.app.send_backup_to_node(host=request.client.host, port=pod['API_PORT_REST'])
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1010",
                                           message="An unknown error has occurred!")
