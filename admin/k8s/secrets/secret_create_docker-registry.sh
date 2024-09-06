#!/usr/bin/env bash

set -e

kubectl create secret docker-registry lucit-harbor-credentials \
  --docker-username= \
  --docker-password= \
  --docker-email= \
  --docker-server=
