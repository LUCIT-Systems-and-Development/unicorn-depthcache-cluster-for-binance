#!/usr/bin/env bash

set -e

VERSION="0.0.57"

echo Deploying UBDCC DepthCacheCluster $VERSION to https://i018oau9.c1.de1.container-registry.ovh.net/harbor/projects/3/repositories

docker build -f container/generic_loader/Dockerfile.lucit-ubdcc-dcn -t lucit-ubdcc-dcn .
docker login i018oau9.c1.de1.container-registry.ovh.net
docker tag lucit-ubdcc-dcn:latest i018oau9.c1.de1.container-registry.ovh.net/library/lucit-ubdcc-dcn:$VERSION
docker push i018oau9.c1.de1.container-registry.ovh.net/library/lucit-ubdcc-dcn:$VERSION
