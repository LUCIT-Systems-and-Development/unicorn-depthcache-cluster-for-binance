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

        @self.fastapi.get("/ubdcc_get_responsible_dcn_addresses")
        async def ubdcc_get_responsible_dcn_addresses(request: Request):
            return await self.ubdcc_get_responsible_dcn_addresses(request=request)

        @self.fastapi.get("/ubdcc_node_cancellation")
        async def ubdcc_node_cancellation(request: Request):
            return await self.ubdcc_node_cancellation(request=request)

        @self.fastapi.get("/ubdcc_node_registration")
        async def ubdcc_node_registration(request: Request):
            return await self.ubdcc_node_registration(request=request)

        @self.fastapi.get("/ubdcc_node_sync")
        async def ubdcc_node_sync(request: Request):
            return await self.ubdcc_node_sync(request=request)

        @self.fastapi.get("/ubdcc_update_depthcache_distribution")
        async def ubdcc_update_depthcache_distribution(request: Request):
            return await self.ubdcc_update_depthcache_distribution(request=request)

    async def create_depthcache(self, request: Request):
        event = "CREATE_DEPTHCACHE"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange", None)
        market = request.query_params.get("market", None)
        desired_quantity = request.query_params.get("desired_quantity", None)
        update_interval = request.query_params.get("update_interval", None)
        refresh_interval = request.query_params.get("refresh_interval", None)
        if market == "None":
            exchange = None
        if market == "None":
            exchange = None
        if desired_quantity is None or desired_quantity == "None":
            desired_quantity = 1
        else:
            desired_quantity = int(desired_quantity)
        if update_interval is None or update_interval == "None":
            update_interval = None
        else:
            update_interval = int(update_interval)
        if refresh_interval is None or refresh_interval == "None":
            refresh_interval = None
        else:
            refresh_interval = int(refresh_interval)
        if exchange is None or market is None:
            return self.get_error_response(event=event, error_id="#1016",
                                           message="Missing required parameter: exchange, market")
        if self.db.exists_depthcache(exchange=exchange, market=market):
            return self.get_error_response(event=event, error_id="#1024",
                                           message=f"DepthCache '{market}' for '{exchange}' already exists!")
        try:
            result = self.db.add_depthcache(exchange=exchange, market=market, update_interval=update_interval,
                                            refresh_interval=refresh_interval, desired_quantity=desired_quantity)
        except ValueError as error_msg:
            return self.get_error_response(event=event, error_id="#1017", message=str(error_msg))
        if result is True:
            used_dcn = []
            for _ in range(0, desired_quantity):
                best_dcn = self.db.get_best_dcn(excluded_pods=used_dcn)
                if best_dcn is not None:
                    self.db.add_depthcache_distribution(exchange=exchange, market=market, pod_uid=best_dcn)
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

    async def get_depthcache_list(self, request: Request):
        event = "GET_DEPTHCACHE_LIST"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        response = self.create_depthcache_list_response()
        return self.get_ok_response(event=event, params=response)

    async def get_depthcache_info(self, request: Request):
        event = "GET_DEPTHCACHE_INFO"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange", None)
        market = request.query_params.get("market", None)
        if market == "None":
            exchange = None
        if market == "None":
            exchange = None
        if exchange is None or market is None:
            return self.get_error_response(event=event, error_id="#1006",
                                           message="Missing required parameter: exchange, market")
        response = self.create_depthcache_info_response(exchange=exchange, market=market)
        if not response['depthcache_info']:
            return self.get_error_response(event=event, error_id="#7000", message=f"DepthCache '{market}' for "
                                                                                  f"'{exchange}' not found!")
        return self.get_ok_response(event=event, params=response)

    async def stop_depthcache(self, request: Request):
        event = "STOP_DEPTHCACHE"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange", None)
        market = request.query_params.get("market", None)
        if market == "None":
            exchange = None
        if market == "None":
            exchange = None
        if exchange is None or market is None:
            return self.get_error_response(event=event, error_id="#1019",
                                           message="Missing required parameter: exchange, market")
        if not self.db.exists_depthcache(exchange=exchange, market=market):
            return self.get_error_response(event=event, error_id="#7000", message=f"DepthCache '{market}' for "
                                                                                  f"'{exchange}' not found!")
        try:
            result = self.db.delete_depthcache(exchange=exchange, market=market)
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
        api_secret = request.query_params.get("api_secret", None)
        license_token = request.query_params.get("license_token", None)
        if api_secret == "None":
            api_secret = None
        if license_token == "None":
            license_token = None
        if api_secret is None or license_token is None:
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

    async def ubdcc_get_responsible_dcn_addresses(self, request: Request):
        event = "UBDCC_GET_RESPONSIBLE_DCN_ADDRESSES"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange", None)
        market = request.query_params.get("market", None)
        if market == "None":
            exchange = None
        if market == "None":
            exchange = None
        if exchange is None or market is None:
            return self.get_error_response(event=event, error_id="#1012",
                                           message="Missing required parameter: exchange, market")
        result = self.db.get_responsible_dcn_addresses(exchange=exchange, market=market)
        if result is True:
            return self.get_ok_response(event=event, params={"addresses": result})
        else:
            return self.get_error_response(event=event, error_id="#1013",
                                           message=f"No addresses of responsible DCN for '{market}' from '{exchange}' "
                                                   f"found!")

    async def ubdcc_node_cancellation(self, request: Request):
        event = "UBDCC_NODE_CANCELLATION"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        uid = request.query_params.get("uid")
        if uid == "None":
            uid = None
        if uid is None:
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
        name = request.query_params.get("name", None)
        uid = request.query_params.get("uid", None)
        node = request.query_params.get("node", None)
        role = request.query_params.get("role", None)
        api_port_rest = request.query_params.get("api_port_rest", None)
        status = request.query_params.get("status", None)
        version = request.query_params.get("version", None)
        if name == "None":
            name = None
        if uid == "None":
            uid = None
        if node == "None":
            node = None
        if role == "None":
            role = None
        if api_port_rest == "None":
            api_port_rest = None
        if status == "None":
            status = None
        if version == "None":
            version = None
        if name is None or uid is None or node is None or role is None or api_port_rest is None or status is None:
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
            await self.app.send_backup_to_node(host=request.client.host, port=api_port_rest)
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1009", message="An unknown error has occurred!")

    async def ubdcc_node_sync(self, request: Request):
        event = "UBDCC_NODE_SYNC"
        uid = request.query_params.get("uid", None)
        node = request.query_params.get("node", None)
        api_port_rest = request.query_params.get("api_port_rest", None)
        status = request.query_params.get("status", None)
        if uid == "None":
            uid = None
        if node == "None":
            node = None
        if api_port_rest == "None":
            api_port_rest = None
        if status == "None":
            status = None
        if uid is None or api_port_rest is None:
            return self.get_error_response(event=event, error_id="#1000",
                                           message="Missing required parameter: uid, api_port_rest")
        if not self.db.exists_pod(uid=uid) and self.db.is_empty() is True:
            backup = await self.app.get_backup_from_node(host=request.client.host, port=api_port_rest)
            if backup is not None:
                source_ip = request.client.host
                source_port = api_port_rest
                source_uid = uid
                timestamp_limit = float(backup['timestamp'])
                pods = []
                for pod in backup['pods']:
                    pods.append(backup['pods'][pod]['UID'])
                    timestamp = await self.app.get_backup_timestamp_from_node(host=backup['pods'][pod]['IP'],
                                                                              port=backup['pods'][pod]['API_PORT_REST'])
                    if timestamp is not None:
                        if timestamp_limit < timestamp:
                            source_ip = pod['IP']
                            source_port = pod['API_PORT_REST']
                            source_uid = pod['UID']
                            timestamp_limit = timestamp
                self.app.stdout_msg(f"Found pods: {pods}", log="info")
                if source_uid != uid:
                    backup = await self.app.get_backup_from_node(host=source_ip, port=source_port)
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
            await self.app.send_backup_to_node(host=request.client.host, port=pod['API_PORT_REST'])
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1010",
                                           message="An unknown error has occurred!")

    async def ubdcc_update_depthcache_distribution(self, request: Request):
        event = "UBDCC_UPDATE_DEPTHCACHE_DISTRIBUTION"
        ready_check = self.throw_error_if_mgmt_not_ready(request=request, event=event)
        if ready_check is not None:
            return ready_check
        exchange = request.query_params.get("exchange", None)
        market = request.query_params.get("market", None)
        pod_uid = request.query_params.get("pod_uid", None)
        last_restart_time = request.query_params.get("last_restart_time", None)
        status = request.query_params.get("status", None)
        if exchange == "None":
            exchange = None
        if market == "None":
            market = None
        if pod_uid == "None":
            pod_uid = None
        if last_restart_time == "None":
            last_restart_time = None
        if status == "None":
            status = None
        if exchange is None or market is None or pod_uid is None:
            return self.get_error_response(event=event, error_id="#1015",
                                           message="Missing required parameter: exchange, market, pod_uid")
        if last_restart_time is None and status is None:
            return self.get_error_response(event=event, error_id="#1022",
                                           message="Nothing to update! Missing parameter: last_restart_time, status")
        result = self.db.update_depthcache_distribution(exchange=exchange, market=market,
                                                        pod_uid=pod_uid, status=status)
        if result is True:
            return self.get_ok_response(event=event)
        else:
            return self.get_error_response(event=event, error_id="#1023", message=f"An unknown error has occurred!")
