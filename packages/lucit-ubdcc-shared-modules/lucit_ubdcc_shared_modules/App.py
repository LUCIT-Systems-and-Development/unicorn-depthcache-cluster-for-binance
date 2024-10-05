#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/App.py
#
# Project website: https://www.lucit.tech/unicorn-binance-depthcache-cluster.html
# Github: https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster
# Documentation: https://unicorn-binance-depthcache-cluster.docs.lucit.tech
# PyPI: https://pypi.org/project/lucit-ubdcc-shared-modules
# LUCIT Online Shop: https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance
#
# License: LSOSL - LUCIT Synergetic Open Source License
# https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/LICENSE
#
# Author: LUCIT Systems and Development
#
# Copyright (c) 2024-2024, LUCIT Systems and Development (https://www.lucit.tech)
# All rights reserved.

import asyncio
import cython
import logging
import json
import os
import signal as sys_signal
import socket
import random
import requests
import string
import sys
import kubernetes
import time
import traceback
from fastapi import FastAPI


K8S_SERVICE_PORT_MGMT: int = 4280
REST_SERVER_PORT: int = 8080
REST_SERVER_PORT_DEV_DCN: int = 42082
REST_SERVER_PORT_DEV_MGMT: int = 42080
REST_SERVER_PORT_DEV_RESTAPI: int = 42081
VERSION: str = "0.0.56"


class App:
    def __init__(self, app_name=None, cwd=None, logger=None, service_call=None, stop_call=None):
        self.app_name = app_name
        self.app_version = VERSION
        self.api_port_rest: int = 0
        self.cwd = cwd
        self.ubdcc_mgmt_url = None
        self.dev_mode = False
        self.fastapi = None
        self.info: dict = {}
        self.k8s_client = None
        self.k8s_metrics_client = None
        self.logger = logger
        self.pod_info = None
        self.k8s_service_port_mgmt = K8S_SERVICE_PORT_MGMT
        self.rest_server_port = REST_SERVER_PORT
        self.rest_server_port_dev_dcn = REST_SERVER_PORT_DEV_DCN
        self.rest_server_port_dev_mgmt = REST_SERVER_PORT_DEV_MGMT
        self.rest_server_port_dev_restapi = REST_SERVER_PORT_DEV_RESTAPI
        self.service_call = service_call
        self.sigterm = False
        self.stop_call = stop_call
        self.status = "starting"
        self.ubdcc_mgmt_backup: str = ""
        self.data: dict = {}
        self.id: dict = {}

    def get_backup_from_node(self, host, port) -> dict:
        data = self.request(f"http://{host}:{port}/ubdcc_mgmt_backup", method="get")
        data = json.loads(data['db'])
        return data

    def get_fastapi_instance(self) -> FastAPI:
        if self.fastapi:
            return self.fastapi
        else:
            if self.dev_mode:
                # DEV MODE!!!
                self.stdout_msg("Starting REST Server in DEV MODE!!!", log="info")
                self.fastapi = FastAPI()
            else:
                # PRODUCTIVE MODE!!!
                self.stdout_msg("Starting REST Server in PRODUCTIVE MODE!!!", log="info")
                self.fastapi = FastAPI(docs_url=None, redoc_url=None)
            return self.fastapi

    def get_k8s_nodes(self) -> dict:
        if self.status != "running":
            raise RuntimeError(f"Instance is not running!")
        if self.k8s_client is not None:
            k8s_nodes = self.k8s_client.list_node()
            result_nodes = {}
            for node in k8s_nodes.items:
                node_name = node.metadata.name
                node_uid = node.metadata.uid
                try:
                    metrics = self.k8s_metrics_client.get_cluster_custom_object(
                        group="metrics.k8s.io", version="v1beta1", plural="nodes", name=node_name
                    )
                except kubernetes.client.exceptions.ApiException as error_msg:
                    self.stdout_msg(f"Error when querying the K8s nodes: {error_msg}", log="error")
                    return {}
                cpu_usage = metrics['usage']['cpu']
                memory_usage = metrics['usage']['memory']
                cpu_capacity = node.status.capacity['cpu']
                memory_capacity = node.status.capacity['memory']
                if cpu_usage.endswith('m'):
                    cpu_usage_milli = int(cpu_usage[:-1])
                elif cpu_usage.endswith('n'):
                    cpu_usage_milli = int(cpu_usage[:-1]) / 1_000_000
                else:
                    cpu_usage_milli = int(cpu_usage) * 1000
                cpu_capacity_milli = int(cpu_capacity) * 1000
                cpu_percentage = (cpu_usage_milli / cpu_capacity_milli) * 100
                memory_usage_bytes = int(memory_usage[:-2]) * 1024
                memory_capacity_bytes = int(memory_capacity[:-2]) * 1024
                memory_percentage = (memory_usage_bytes / memory_capacity_bytes) * 100
                result_nodes[node_uid] = {"NAME": node_name,
                                          "UID": node_uid,
                                          "USAGE_CPU_PERCENT": f"{cpu_percentage:.2f}",
                                          "USAGE_MEMORY_PERCENT": f"{memory_percentage:.2f}"}
            return result_nodes
        return {}

    def get_k8s_runtime_information(self):
        try:
            kubernetes.config.load_incluster_config()
            with open("/etc/hostname", "r") as f:
                pod_name = f.read().strip()
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
                namespace = f.read().strip()
            self.k8s_client = kubernetes.client.CoreV1Api()
            self.k8s_metrics_client = kubernetes.client.CustomObjectsApi()
            self.pod_info = self.k8s_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            self.stdout_msg(f"Pod Name: {self.pod_info.metadata.name}", log="info")
            self.stdout_msg(f"Pod UID: {self.pod_info.metadata.uid}", log="info")
            self.stdout_msg(f"Pod Namespace: {self.pod_info.metadata.namespace}", log="info")
            self.stdout_msg(f"Node Name: {self.pod_info.spec.node_name}", log="info")
            self.stdout_msg(f"Pod Labels: {self.pod_info.metadata.labels}", log="info")
        except kubernetes.client.exceptions.ApiException as error_msg:
            self.stdout_msg(f"WARNING: K8s - {error_msg}", log="warn")
            self.k8s_client = None
            self.pod_info = None
            self.dev_mode = True
        except kubernetes.config.config_exception.ConfigException as error_msg:
            self.stdout_msg(f"WARNING: K8s - {error_msg}", log="warn")
            self.k8s_client = None
            self.pod_info = None
            self.dev_mode = True

        self.id['name'] = self.generate_string(random.randint(10, 15)) if self.dev_mode else self.pod_info.metadata.name
        self.id['uid'] = self.generate_string(random.randint(20, 20)) if self.dev_mode else self.pod_info.metadata.uid
        self.id['node'] = self.generate_string(random.randint(15, 15)) if self.dev_mode else (
                                                                                        self.pod_info.spec.node_name)

    def get_cluster_mgmt_address(self):
        if self.dev_mode:
            # DEV MODE!!!
            url = f"http://localhost:{self.rest_server_port_dev_mgmt}"
        else:
            # PRODUCTIVE MODE!!!
            url = f"http://lucit-ubdcc-mgmt.lucit-ubdcc.svc.cluster.local:{self.k8s_service_port_mgmt}"
        return url

    @staticmethod
    def generate_string(length):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def get_unix_timestamp():
        return time.time()

    @staticmethod
    def get_version() -> str:
        return VERSION

    @staticmethod
    def is_compiled() -> bool:
        return cython.compiled

    def is_shutdown(self) -> bool:
        return self.sigterm

    def register_or_restart(self):
        if self.ubdcc_node_registration() is False:
            self.shutdown(message="Node registration failed!")

    def register_graceful_shutdown(self) -> None:
        sys_signal.signal(sys_signal.SIGINT, self.sigterm_handler)
        sys_signal.signal(sys_signal.SIGTERM, self.sigterm_handler)

    @staticmethod
    def request(url, method, params=None, headers=None, timeout=10) -> dict:
        try:
            if method == "get":
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "post":
                response = requests.post(url, json=json.dumps(params),
                                         headers={"Content-Type": "application/json"})
            else:
                raise ValueError("Allowed 'method' values: get, post")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error_msg:
            print(f"An error occurred: {error_msg}")
            return {"error": error_msg}

    def send_backup_to_node(self, host, port) -> dict:
        return self.request(f"http://{host}:{port}/ubdcc_mgmt_backup", method="post",
                            params=self.data['db'].get_backup_string())

    def set_api_rest_port(self):
        if self.dev_mode:
            # DEV MODE!!!
            if self.info['name'] == "lucit-ubdcc-dcn":
                self.api_port_rest = self.rest_server_port_dev_dcn
            elif self.info['name'] == "lucit-ubdcc-mgmt":
                self.api_port_rest = self.rest_server_port_dev_mgmt
            elif self.info['name'] == "lucit-ubdcc-restapi":
                self.api_port_rest = self.rest_server_port_dev_restapi
            else:
                raise ValueError(f"Not able to choose the right rest server port for app '{self.info['name']}'")
        else:
            # PRODUCTIVE MODE!!!
            self.api_port_rest = self.rest_server_port

    def set_status_running(self) -> bool:
        self.status = "running"
        return True

    def shutdown(self, message=None) -> None:
        self.sigterm = True
        self.stdout_msg(f"Shutdown is performed: {message}", log="warn")

    def sigterm_handler(self, signal, frame) -> None:
        self.sigterm = True
        self.stdout_msg(f"Processing SIGTERM - signal: {signal} - frame: {frame}", log="debug", stdout=False)
        self.stdout_msg(f"Received SIGTERM, performing graceful shutdown ...", log="warn")

    async def sleep(self, seconds: int = 10) -> bool:
        internal_sleep_time = 3
        time_start = self.get_unix_timestamp()
        time_limit = time_start + seconds
        for i in range(int(seconds/internal_sleep_time)):
            if self.get_unix_timestamp() < time_limit and self.is_shutdown() is False:
                await asyncio.sleep(internal_sleep_time)
            else:
                break
        return True

    @staticmethod
    def sort_dict(input_dict: dict, reverse: bool = False) -> dict:
        sorted_items = sorted(input_dict.items(), key=lambda item: item[0], reverse=reverse)
        return dict(sorted_items)

    def start(self) -> None:
        # Working Directory
        if self.cwd:
            os.chdir(self.cwd)

        # Logging
        if self.logger is None:
            self.logger = logging.getLogger("unicorn_binance_depthcache_cluster")
            logging.basicConfig(level=logging.DEBUG,
                                filename=f"{socket.gethostname()}.log",
                                format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                                style="{")

        # App Info
        self.info = {'name': self.app_name,
                     'version': self.get_version(),
                     'author': "LUCIT Systems and Development",
                     'build_type': "compiled" if self.is_compiled() else "source"}
        info = (f"Starting {self.info['name']}_{self.info['version']}_{self.info['build_type']} by "
                f"{self.info['author']} ...")
        self.stdout_msg(info, log="info")

        # Catch Termination Signals
        self.register_graceful_shutdown()

        # Runtime Information
        self.get_k8s_runtime_information()

        # Define and set the rest server port
        self.set_api_rest_port()

        # Running the core app
        exception_shutdown = False
        exception_shutdown_error = None
        self.status = "running"
        try:
            self.service_call()
        except KeyboardInterrupt:
            self.stdout_msg(f"Keyboard interrupt was caught!", log="warn")
        except Exception as error_msg:
            exception_shutdown = True
            exception_shutdown_error = error_msg
            print("Exception occurred:")
            traceback.print_exc()
        finally:
            if exception_shutdown is True:
                if exception_shutdown_error:
                    self.stdout_msg(f"ERROR: {exception_shutdown_error}", log="critical")
                self.stop_call()
                self.stdout_msg(f"The system was gracefully shut down after a critical error was encountered.",
                                log="info")
                sys.exit(1)

        # Shutdown
        self.stop_call()
        self.stdout_msg(f"Gracefully shutdown finished! Thank you and good bye ...", log="info")
        sys.exit(0)

    def stdout_msg(self, msg=None, log=None, stdout=True) -> bool:
        if msg is None:
            return False
        if log is None and stdout is False:
            return False
        if log is not None:
            if log == "debug":
                self.logger.debug(msg)
            elif log == "info":
                self.logger.info(msg)
            elif log == "warn":
                self.logger.warn(msg)
            elif log == "error":
                self.logger.error(msg)
            elif log == "critical":
                self.logger.critical(msg)
            else:
                return False
        if stdout is True:
            print(msg, flush=True)
        return True

    def ubdcc_node_cancellation(self):
        pass

    def ubdcc_node_registration(self, retries=30) -> bool:
        self.stdout_msg(f"Starting node registration ...", log="info")
        endpoint = "/ubdcc_node_registration"
        host = self.get_cluster_mgmt_address()
        query = (f"?name={self.id['name']}&"
                 f"uid={self.id['uid']}&"
                 f"node={self.id['node']}&"
                 f"role={self.info['name']}&"
                 f"api_port_rest={self.api_port_rest}&"
                 f"status={self.status}&"
                 f"version={self.get_version()}")
        url = host + endpoint + query
        loops = 0
        result = None
        while loops < retries:
            loops += 1
            result = self.request(url=url, method="get")
            if result.get('error') is None:
                self.stdout_msg(f"Node registration succeeded!", log="info")
                return True
            time.sleep(1)
        self.stdout_msg(f"Error during node registration: {result.get('error_id')} - {result.get('error')}",
                        log="error")
        return False

    def ubdcc_node_sync(self) -> bool:
        self.stdout_msg(f"Starting node sync ...", log="info")
        endpoint = "/ubdcc_node_sync"
        host = self.get_cluster_mgmt_address()
        query = (f"?uid={self.id['uid']}&"
                 f"node={self.id['node']}&"
                 f"status={self.status}")
        url = host + endpoint + query
        result = self.request(url=url, method="get")
        if result.get('error_id') is None and result.get('error') is None:
            self.stdout_msg(f"Node sync succeeded!", log="info")
            return True
        elif result.get('error') is not None:
            self.stdout_msg(f"Error during node sync: {result.get('error')}", log="warn")
            return False
        elif result.get('error_id') == "#1001":
            self.stdout_msg(f"The node is no longer recognized by {url}.", log="warn")
            # Todo: Sync local settings with mgmt!
            return self.ubdcc_node_registration()
        else:
            self.stdout_msg(f"Error during node sync: {result.get('error_id')} - {result.get('message')}",
                            log="error")
            return False
