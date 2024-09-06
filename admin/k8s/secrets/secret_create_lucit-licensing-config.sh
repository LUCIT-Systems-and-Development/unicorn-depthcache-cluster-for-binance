#!/usr/bin/env bash

set -e

SECRET_STRING=$(python3 ./admin/k8s/tools/converter_configini_to_json.py)
kubectl delete secret lucit-ubdcc -n lucit-ubdcc
kubectl create secret generic lucit-ubdcc -n lucit-ubdcc --from-literal=config.json="$SECRET_STRING"
