#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/Service.py
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

import cython
import logging
import os
import socket
import sys
import time
import kubernetes
from lucit_ubdcc_shared_modules.AppClass import AppClass
from lucit_ubdcc_shared_modules.Database import Database


def start(cwd=None):
    # App Identity
    app = {'name': "lucit-ubdcc-mgmt",
           'version': AppClass.get_version(),
           'author': "LUCIT Systems and Development"}
    print(f"App Info: {app}")

    info = f"Init lucit-ubdcc-mgmt Service {app['version']} ..."
    print(info)
    print(f"Configure Logging ...")
    logger = logging.getLogger("unicorn_binance_depthcache_cluster")
    logging.basicConfig(level=logging.DEBUG,
                        filename=f"{socket.gethostname()}-{os.path.basename(__file__)}.log",
                        format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                        style="{")
    logger.info(info)
    info = "Logging is ready!"
    print(info)
    logger.info(info)

    app_class = AppClass(logger=logger)
    app_class.register_graceful_shutdown()

    # K8 Information
    try:
        kubernetes.config.load_incluster_config()
        with open("/etc/hostname", "r") as f:
            pod_name = f.read().strip()
        with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
            namespace = f.read().strip()
        k8_client = kubernetes.client.CoreV1Api()
        pod_info = k8_client.read_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"Pod Name: {pod_info.metadata.name}")
        print(f"Pod UID: {pod_info.metadata.uid}")
        print(f"Pod Namespace: {pod_info.metadata.namespace}")
        print(f"Node Name: {pod_info.spec.node_name}")
        print(f"Pod Labels: {pod_info.metadata.labels}")
    except kubernetes.client.exceptions.ApiException as error_msg:
        print(f"K8 error_msg: {error_msg}")
        pod_info = "not available"
    except kubernetes.config.config_exception.ConfigException as error_msg:
        print(f"K8 error_msg: {error_msg}")
        pod_info = "not available"



    # Working Directory
    if cwd:
        os.chdir(cwd)

    # Database
    db = Database()

    # Variables
    service_name = "lucit-ubdcc-mgmt.lucit-ubdcc.svc.cluster.local"


    app_class.stdout_msg(f"Compiled: {str(cython.compiled)}", log="info")
    google_ip = socket.gethostbyname("google.com")
    app_class.stdout_msg(f"DNS test (resolving 'google.com'): {google_ip}", log="info")

    time.sleep(10)

    try:
        while app_class.is_shutdown() is False:
            try:
                service_ip = socket.gethostbyname(service_name)
            except socket.gaierror:
                service_ip = "unknown"
            print(f"Hallo Olli @ {service_ip} {time.time()}")
            time.sleep(10)
            app_class.stdout_msg(f"Loop finished ...", log="info")
    except Exception as error_msg:
        app_class.stdout_msg(f"ERROR: {error_msg}", log="critical")
        sys.exit(1)

    app_class.stdout_msg(f"Gracefully shutdown finished! Thank you and good bye ...", log="info")
