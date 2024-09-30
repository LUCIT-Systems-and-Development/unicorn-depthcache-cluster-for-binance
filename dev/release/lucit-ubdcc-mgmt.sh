#!/usr/bin/env bash

set -e

VERSION="0.0.22"

echo Deploying UBDCC Mgmt $VERSION to https://i018oau9.c1.de1.container-registry.ovh.net/harbor/projects/3/repositories

docker build -f container/generic_loader/Dockerfile.lucit-ubdcc-mgmt -t lucit-ubdcc-mgmt .
docker login i018oau9.c1.de1.container-registry.ovh.net
docker tag lucit-ubdcc-mgmt:latest i018oau9.c1.de1.container-registry.ovh.net/library/lucit-ubdcc-mgmt:$VERSION
docker push i018oau9.c1.de1.container-registry.ovh.net/library/lucit-ubdcc-mgmt:$VERSION
