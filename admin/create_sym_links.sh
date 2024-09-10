#!/usr/bin/env bash

cd container/ubdcc-mgmt/
ln -s ../../packages/ubdcc-mgmt/ubdcc_mgmt .
ln -s ../../packages/ubdcc-shared-modules/ubdcc_shared_modules .

cd ../../packages/ubdcc-mgmt/
ln -s ../ubdcc-shared-modules/ubdcc_shared_modules .