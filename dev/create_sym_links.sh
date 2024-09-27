#!/usr/bin/env bash

cd container/generic_loader/
ln -s ../../packages/lucit-ubdcc-mgmt/lucit_ubdcc_mgmt .
ln -s ../../packages/lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules .

cd ../../packages/lucit-ubdcc-mgmt/
ln -s ../lucit-ubdcc-shared-modules/lucit_ubdcc_shared_modules .
cd lucit_ubdcc_mgmt
ln -s ../lucit_ubdcc_shared_modules .
