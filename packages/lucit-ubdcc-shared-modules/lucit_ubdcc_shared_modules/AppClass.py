#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules/AppClass.py
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

import cython
import logging
import fastapi
import os
import signal
import socket
import sys
import kubernetes


VERSION = "0.0.14"


class AppClass:
    def __init__(self, app_name=None, cwd=None, logger=None, service_call=None):
        self.app = None
        self.app_name = app_name
        self.cwd = cwd
        self.cython = None
        self.fastapi = None
        self.k8_client = None
        self.logger = logger
        self.pod_info = None
        self.service_call = service_call
        self.sigterm = False

    @staticmethod
    def get_version() -> str:
        return VERSION

    def is_compiled(self) -> bool:
        return self.cython.compiled

    def is_shutdown(self) -> bool:
        return self.sigterm

    def register_graceful_shutdown(self) -> None:
        signal.signal(signal.SIGINT, self.sigterm_handler)
        signal.signal(signal.SIGTERM, self.sigterm_handler)

    def sigterm_handler(self, signal, frame) -> None:
        self.sigterm = True
        print("Received SIGTERM, performing graceful shutdown ...")
        self.logger.warning(f"Received SIGTERM, performing graceful shutdown ... - {signal} - {frame}")

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
            print(msg)
        return True

    def start(self) -> None:
        # App Identity
        self.app = {'name': self.app_name,
                    'version': self.get_version(),
                    'author': "LUCIT Systems and Development"}
        print(f"App Info: {self.app}")

        # Start Message
        info = f"Init {self.app['name']} Service {self.app['version']} ..."
        print(info)

        # Working Directory
        if self.cwd:
            os.chdir(self.cwd)

        # Logging
        print(f"Configure Logging ...")
        if self.logger is None:
            self.logger = logging.getLogger("unicorn_binance_depthcache_cluster")
            logging.basicConfig(level=logging.DEBUG,
                                filename=f"{socket.gethostname()}.log",
                                format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                                style="{")
            self.logger.info(info)
            info = "Logging is ready!"
            self.stdout_msg(info, log="info")

        # Catch Termination Signals
        self.register_graceful_shutdown()

        # Modules
        self.cython = cython
        self.fastapi = fastapi

        # Runtime Information
        try:
            kubernetes.config.load_incluster_config()
            with open("/etc/hostname", "r") as f:
                pod_name = f.read().strip()
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
                namespace = f.read().strip()
            self.k8_client = kubernetes.client.CoreV1Api()
            self.pod_info = self.k8_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            print(f"Pod Name: {self.pod_info.metadata.name}")
            print(f"Pod UID: {self.pod_info.metadata.uid}")
            print(f"Pod Namespace: {self.pod_info.metadata.namespace}")
            print(f"Node Name: {self.pod_info.spec.node_name}")
            print(f"Pod Labels: {self.pod_info.metadata.labels}")
        except kubernetes.client.exceptions.ApiException as error_msg:
            print(f"K8 error_msg: {error_msg}")
            self.pod_info = "not available"
        except kubernetes.config.config_exception.ConfigException as error_msg:
            print(f"K8 error_msg: {error_msg}")
            self.pod_info = "not available"

        self.stdout_msg(f"Compiled: {self.is_compiled()}", log="info")

        google_ip = socket.gethostbyname("google.com")
        self.stdout_msg(f"DNS test (resolving 'google.com'): {google_ip}", log="info")

        # Running the core app
        try:
            self.service_call()
        except Exception as error_msg:
            self.stdout_msg(f"ERROR: {error_msg}", log="critical")
            sys.exit(1)

        # Shutdown
        self.stdout_msg(f"Gracefully shutdown finished! Thank you and good bye ...", log="info")
