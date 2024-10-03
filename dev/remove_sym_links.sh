#!/usr/bin/env bash

rm -f ./container/generic_loader/lucit_ubdcc_dcn
rm -f ./container/generic_loader/lucit_ubdcc_mgmt
rm -f ./container/generic_loader/lucit_ubdcc_restapi
rm -f ./container/generic_loader/lucit_ubdcc_shared_modules

rm -f ./packages/lucit-ubdcc-dcn/lucit_ubdcc_shared_modules
rm -f ./packages/lucit-ubdcc-dcn/lucit_ubdcc_dcn/lucit_ubdcc_shared_modules

rm -f ./packages/lucit-ubdcc-mgmt/lucit_ubdcc_shared_modules
rm -f ./packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt/lucit_ubdcc_shared_modules

rm -f ./packages/lucit-ubdcc-restapi/lucit_ubdcc_shared_modules
rm -f ./packages/lucit-ubdcc-restapi/lucit_ubdcc_restapi/lucit_ubdcc_shared_modules