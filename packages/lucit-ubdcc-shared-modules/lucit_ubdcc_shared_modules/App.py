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
import os
import signal as sys_signal
import socket
import sys
import kubernetes
import time
from fastapi import FastAPI

REST_SERVER_PORT = 8080
VERSION = "0.0.42"


class App:
    def __init__(self, app_name=None, cwd=None, logger=None, service_call=None, stop_call=None):
        self.app_name = app_name
        self.app_version = VERSION
        self.cwd = cwd
        self.fastapi = FastAPI(docs_url=None, redoc_url=None)
        self.info = None
        self.k8s_client = None
        self.k8s_metrics_client = None
        self.logger = logger
        self.pod_info = None
        self.rest_server_port = REST_SERVER_PORT
        self.service_call = service_call
        self.sigterm = False
        self.stop_call = stop_call
        self.status = "starting"
        self.data: dict = {}

    def get_fastapi_instance(self) -> FastAPI:
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
                metrics = self.k8s_metrics_client.get_cluster_custom_object(
                    group="metrics.k8s.io", version="v1beta1", plural="nodes", name=node_name
                )
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

    @staticmethod
    def get_timestamp():
        return time.time()

    @staticmethod
    def get_version() -> str:
        return VERSION

    @staticmethod
    def is_compiled() -> bool:
        return cython.compiled

    def is_shutdown(self) -> bool:
        return self.sigterm

    def register_graceful_shutdown(self) -> None:
        sys_signal.signal(sys_signal.SIGINT, self.sigterm_handler)
        sys_signal.signal(sys_signal.SIGTERM, self.sigterm_handler)

    def sigterm_handler(self, signal, frame) -> None:
        self.sigterm = True
        self.stdout_msg(f"Processing SIGTERM - signal: {signal} - frame: {frame}", log="debug", stdout=False)
        self.stdout_msg(f"Received SIGTERM, performing graceful shutdown ...", log="warn")

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

    async def sleep(self, seconds: int = None) -> bool:
        if seconds is None:
            raise ValueError("Parameter 'seconds' is mandatory!")
        internal_sleep_time = 3
        time_start = time.time()
        time_limit = time_start + seconds
        for i in range(int(seconds/internal_sleep_time)):
            if time.time() < time_limit and self.is_shutdown() is False:
                await asyncio.sleep(internal_sleep_time)
            else:
                break
        return True

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

        # App Identity
        self.info = {'name': self.app_name,
                     'version': self.get_version(),
                     'author': "LUCIT Systems and Development"}
        build_type = "compiled" if self.is_compiled() else "source"
        info = f"Starting {self.info['name']}_{self.info['version']}_{build_type} by {self.info['author']} ..."
        self.stdout_msg(info, log="info")

        # Catch Termination Signals
        self.register_graceful_shutdown()

        # Runtime Information
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
            self.pod_info = "not available"
        except kubernetes.config.config_exception.ConfigException as error_msg:
            self.stdout_msg(f"WARNING: K8s - {error_msg}", log="warn")
            self.k8s_client = None
            self.pod_info = "not available"

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
