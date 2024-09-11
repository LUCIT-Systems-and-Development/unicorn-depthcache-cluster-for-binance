#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯
#
# File: packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/RestApiEndpoints.py
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

import time
from fastapi import FastAPI, Request


class RestApiEndpoints:
    def __init__(self, app=None, app_class=None, cache_licenses=None, config=None, restapi_tools=None,
                 service_stage="production"):
        self.app = app
        self.app_class = app_class
        self.cache_licenses = cache_licenses
        self.config = config
        self.restapi_tools = restapi_tools
        self.service_stage = service_stage
        if service_stage == "development":
            # Dev Stage:
            fastapi = FastAPI()
        else:
            # Productive Stage:
            fastapi = FastAPI(docs_url=None, redoc_url=None)
        self.fastapi = fastapi

        # ENDPOINTS
        @fastapi.get("/licensing/v1/close")
        async def close(request: Request):
            """
                Verify the given license.
                Access: Private
            """
            self.restapi_tools.control_access_header(request=request)
            session = self.restapi_tools.request_validation(request=request)
            self.restapi_tools.control_private_access_api_rates(session=session)

            result = self.restapi_tools.redis_delete_quota_instance(session=session)
            if result is True:
                blacklist = self.restapi_tools.redis_blacklist_instance(session=session)
                if blacklist is True:
                    params = {"close": {"status": "SUCCESSFUL"}}
                else:
                    params = {"close": {"status": "NOT_SUCCESSFUL"}}
            else:
                params = {"close": {"status": "NOT_SUCCESSFUL"}}

            params["timestamp"] = str(time.time())
            params["signature"] = self.restapi_tools.generate_signature(
                                                            api_secret=session['license_record']['customer_api_secret'],
                                                            data=params)
            return params

        @fastapi.get("/licensing/v1/info")
        async def info(request: Request):
            """
                Return information about the given license.
                Access: Private
            """
            start_time = time.time()
            self.restapi_tools.control_access_header(request=request)
            session = self.restapi_tools.request_validation(request=request)
            self.restapi_tools.control_private_access_api_rates(session=session)

            params = {"license": {"licensed_product": "UNICORN-BINANCE-SUITE",
                                  "license_holder_name": str(session['license_record']['license_holder_name']),
                                  "license_holder_email": str(session['license_record']['license_holder_email']),
                                  "paid_till": str(session['license_record']['paid_till'])},
                      "timestamp": str(time.time())}

            params["signature"] = self.restapi_tools.generate_signature(
                                                            api_secret=session['license_record']['customer_api_secret'],
                                                            data=params)
            self.app_class.stdout_msg(msg=f"License {session['license_record']['customer_license']} for client "
                                          f"{session['request_get']['client_ip']} validated within "
                                          f"{time.time()-start_time} seconds!", log="debug", stdout=True)
            return params

        @fastapi.get("/licensing/v1/quotas")
        async def quotas(request: Request):
            """
                Get Quotas of a given license.
                Access: Private
            """
            self.restapi_tools.control_access_header(request=request)
            session = self.restapi_tools.request_validation(request=request)
            self.restapi_tools.control_private_access_api_rates(session=session)

            instances_available = session['quota']['instances']
            instances_used = self.restapi_tools.get_quota_instances_used(session['license_record']['customer_license'])

            ips_available = session['quota']['ips']
            ips_used = self.restapi_tools.get_quota_ips_used(session['license_record']['customer_license'])

            resets_available = self.restapi_tools.reset_quota_value
            resets_used = self.restapi_tools.get_quota_resets_used(session['license_record']['customer_license'])

            params = {"quotas": {"ips": {"available": ips_available,
                                         "used": ips_used,
                                         "free": (ips_available - ips_used)},
                                 "instances": {"available": instances_available,
                                               "used": instances_used,
                                               "free": (instances_available - instances_used)},
                                 "resets": {"available": resets_available,
                                            "used": resets_used,
                                            "free": (resets_available - resets_used)}},
                      "timestamp": str(time.time())}

            params["signature"] = self.restapi_tools.generate_signature(
                                                            api_secret=session['license_record']['customer_api_secret'],
                                                            data=params)
            return params

        @fastapi.get("/licensing/v1/reset")
        async def reset(request: Request):
            """
                Release the occupied slots of your quota. Please note, this will stop ALL active instances.
                Access: Private
            """
            start_time = time.time()
            self.restapi_tools.control_access_header(request=request)
            session = self.restapi_tools.request_validation(request=request)
            self.restapi_tools.control_private_access_api_rates(session=session)

            result = self.restapi_tools.redis_release_quotas(session=session)
            if result is True:
                params = {"reset": {"status": "SUCCESSFUL"}}
            else:
                params = {"reset": {"status": "NOT_SUCCESSFUL"}}

            params["timestamp"] = str(time.time())
            params["signature"] = self.restapi_tools.generate_signature(
                                                            api_secret=session['license_record']['customer_api_secret'],
                                                            data=params)
            self.app_class.stdout_msg(msg=f"License {session['license_record']['customer_license']} for client "
                                          f"{session['request_get']['client_ip']} validated within "
                                          f"{time.time()-start_time} seconds!", log="debug", stdout=True)
            return params

        @fastapi.get("/licensing/v1/test")
        async def test(request: Request):
            """
                Just a test to proof if the backend is reachable (no request validation)
                Access: Public
            """
            self.restapi_tools.control_access_header(request=request)
            self.restapi_tools.control_public_access_api_rates(request=request)
            return {"message": "Hello World!"}

        @fastapi.get("/licensing/v1/timestamp")
        async def timestamp(request: Request):
            """
                Just a test to proof if the backend is reachable (no request validation)
                Access: Public
            """
            self.restapi_tools.control_access_header(request=request)
            self.restapi_tools.control_public_access_api_rates(request=request)
            return {"timestamp": str(time.time())}

        @fastapi.get("/licensing/v1/verify")
        async def verify(request: Request):
            """
                Verify the given license and occupy used quotas
                Access: Private
            """
            start_time = time.time()
            self.restapi_tools.control_access_header(request=request)
            session = self.restapi_tools.request_validation(request=request)
            if session['license_record']['product_id'] == self.restapi_tools.lucit_licenses.PRODUCT_ID_UBS_TEST:
                self.restapi_tools.prevent_test_license_abuse(session=session)
            self.restapi_tools.control_private_access_api_rates(session=session)
            if self.restapi_tools.redis_is_instance_blacklisted(session=session):
                license_status = "INSTANCE_CLOSED"
            else:
                self.restapi_tools.control_private_access_quotas(session=session)
                license_status = "VALID"

            params = {"license": {"licensed_product": "UNICORN-BINANCE-SUITE",
                                  "license_holder_name": str(session['license_record']['license_holder_name']),
                                  "license_holder_email": str(session['license_record']['license_holder_email']),
                                  "paid_till": str(session['license_record']['paid_till']),
                                  "request_interval": str(self.config.restapi_client_request_interval_minutes),
                                  "status": license_status},
                      "timestamp": str(time.time())}

            params["signature"] = self.restapi_tools.generate_signature(
                                                            api_secret=session['license_record']['customer_api_secret'],
                                                            data=params)
            self.app_class.stdout_msg(msg=f"License {session['license_record']['customer_license']} for client "
                                          f"{session['request_get']['client_ip']} validated within "
                                          f"{time.time()-start_time} seconds!", log="debug", stdout=True)
            return params

        @fastapi.get("/licensing/v1/version")
        async def version(request: Request):
            """
                Get the API version number
                Access: Public
            """
            self.restapi_tools.control_access_header(request=request)
            self.restapi_tools.control_public_access_api_rates(request=request)
            return {"version_api": self.app['version']}

    def get_fastapi_instance(self):
        return self.fastapi
