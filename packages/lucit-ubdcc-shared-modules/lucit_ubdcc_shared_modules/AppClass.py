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
import os
import signal as sys_signal
import socket
import sys
import kubernetes
from fastapi import FastAPI


VERSION = "0.0.20"


class AppClass:
    def __init__(self, app_name=None, cwd=None, logger=None, service_call=None, stop_call=None):
        self.app = None
        self.app_name = app_name
        self.cwd = cwd
        self.fastapi = FastAPI(docs_url=None, redoc_url=None)
        self.k8_client = None
        self.logger = logger
        self.pod_info = None
        self.service_call = service_call
        self.sigterm = False
        self.stop_call = stop_call

    def get_fastapi_instance(self):
        return self.fastapi

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
        print("# Received SIGTERM, performing graceful shutdown ...")
        self.logger.warning(f"# Received SIGTERM, performing graceful shutdown ... - {signal} - {frame}")

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
        self.app = {'name': self.app_name,
                    'version': self.get_version(),
                    'author': "LUCIT Systems and Development"}
        build_type = "compiled" if self.is_compiled() else "source"
        info = f"# Starting {self.app['name']}_{self.app['version']}_{build_type} by {self.app['author']} ..."
        print(info)
        self.logger.info(info)

        # Catch Termination Signals
        self.register_graceful_shutdown()

        # Runtime Information
        try:
            kubernetes.config.load_incluster_config()
            with open("/etc/hostname", "r") as f:
                pod_name = f.read().strip()
            with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
                namespace = f.read().strip()
            self.k8_client = kubernetes.client.CoreV1Api()
            self.pod_info = self.k8_client.read_namespaced_pod(name=pod_name, namespace=namespace)
            self.stdout_msg(f"# Pod Name: {self.pod_info.metadata.name}", log="info")
            self.stdout_msg(f"# Pod UID: {self.pod_info.metadata.uid}", log="info")
            self.stdout_msg(f"# Pod Namespace: {self.pod_info.metadata.namespace}", log="info")
            self.stdout_msg(f"# Node Name: {self.pod_info.spec.node_name}", log="info")
            self.stdout_msg(f"# Pod Labels: {self.pod_info.metadata.labels}", log="info")
        except kubernetes.client.exceptions.ApiException as error_msg:
            self.stdout_msg(f"# K8 error_msg: {error_msg}", log="warn")
            self.pod_info = "not available"
        except kubernetes.config.config_exception.ConfigException as error_msg:
            self.stdout_msg(f"# K8 error_msg: {error_msg}", log="warn")
            self.pod_info = "not available"

        # Running the core app
        exception_shutdown = False
        exception_shutdown_error = None
        try:
            self.service_call()
        except KeyboardInterrupt:
            print(f"Keyboard interrupt was caught!")
        except Exception as error_msg:
            exception_shutdown = True
            exception_shutdown_error = error_msg
        finally:
            if exception_shutdown is True:
                if exception_shutdown_error:
                    self.stdout_msg(f"# ERROR: {exception_shutdown_error}", log="critical")
                self.stop_call()
                self.stdout_msg(f"# The system was gracefully shut down after a critical error was encountered.",
                                log="info")
                sys.exit(1)

        # Shutdown
        self.stop_call()
        self.stdout_msg(f"# Gracefully shutdown finished! Thank you and good bye ...", log="info")
        sys.exit(0)
