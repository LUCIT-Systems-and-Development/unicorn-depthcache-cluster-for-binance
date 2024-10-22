[![Get a UNICORN DepthCache Cluster for Binance License](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/blob/master/images/logo/LUCIT-UBDCC-License-Offer.png)](https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance)

[![License](https://img.shields.io/badge/license-LSOSL-blue)](https://unicorn-binance-depthcache-cluster.docs.lucit.tech/license.html)
[![Build and Publish PyPi (lucit-ubdcc-dcn)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_dcn.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_dcn.yml)
[![Build and Publish PyPi (lucit-ubdcc-mgmt)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_mgmt.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_mgmt.yml)
[![Build and Publish PyPi (lucit-ubdcc-restapi)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_restapi.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_restapi.yml)
[![Build and Publish PyPi (lucit-ubdcc-shared-modules)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_shared_modules.yml/badge.svg)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/actions/workflows/build_wheels_lucit_ubdcc_shared_modules.yml)
[![Read the Docs](https://img.shields.io/badge/read-%20docs-yellow)](https://unicorn-binance-depth-cache-cluster.docs.lucit.tech/)
[![Github](https://img.shields.io/badge/source-github-cbc2c8)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster)
[![Telegram](https://img.shields.io/badge/community-telegram-41ab8c)](https://t.me/unicorndevs)
[![Gitter](https://img.shields.io/badge/community-gitter-41ab8c)](https://gitter.im/unicorn-trading-suite/unicorn-binance-depthcache-cluster?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Get Free Professional Support](https://img.shields.io/badge/chat-lucit%20support-004166)](https://www.lucit.tech/get-support.html)

# UNICORN Binance Depth Cache Cluster (UBDCC)

A highly scalable Kubernetes application from LUCIT to manage multiple and redundant UNICORN Binance Local Depth Cache 
Instances on a Kubernetes Cluster for high-frequency access to Binance's DepthCache data (order books). 

[Get help](https://www.lucit.tech/get-support.html)!

## Get a UNICORN DepthCache Cluster for Binance License

***Licenses will only be publicly available in the store in a few days. If you are interested, please 
[contact us via the chat](https://www.lucit.tech/get-support.html)!***

To run the *UNICORN DepthCache Cluster for Binance* you need a [valid license](https://shop.lucit.services/software/unicorn-depthcache-cluster-for-binance)!

## What is UBDCC?

The main idea is to deploy the UBDCC on a Kubernetes cluster with, for example, 4 rented servers. After transferring a 
valid license, you can create and manage DepthCaches within the cluster environment instead of on local servers and 
access them from multiple clients.

For example, when you configure the system to create 200 DepthCaches with a `desired_quantity` of 2, UBDCC will deploy 2 
DepthCaches for each symbol/market. These DepthCaches are evenly distributed across the nodes of the cluster and can 
download order book snapshots from the Binance Rest API using their own public IP addresses. On the first run, each 
server starts 50 DepthCaches, synchronizing the full set of 200 as quickly as possible. Afterward, replicas are 
initiated, with each node handling 100 DepthCaches.

[![Visual overview](https://lucid.app/publicSegments/view/7ba7d734-4bb2-467f-b7b9-74ea0d1deec2/image.png)](https://lucid.app/publicSegments/view/7ba7d734-4bb2-467f-b7b9-74ea0d1deec2/image.png)

## Key Features

- **Asynchronous Operation**: The entire cluster code is built to run asynchronously.
- **Load Balancing & Failover**: All requests for data (Asks/Bids) are handled via a load balancer with built-in 
failover, ensuring high availability and quick response times.
  - Local requests for Asks/Bids: ~0.02 seconds
  - Requests via the Internet: ~0.06 seconds
- **Flexible Data Retrieval**: You can trim the amount of transferred data at the cluster level, either by limiting to
a specific amount of top Asks/Bids or by setting a threshold.
- **HTTP Access**: DepthCache values can be retrieved through HTTP using both synchronous and asynchronous methods 
provided by 
[UBLDC](https://unicorn-binance-local-depth-cache.docs.lucit.tech/unicorn_binance_local_depth_cache.html#module-unicorn_binance_local_depth_cache.cluster).
- **Top Performance**: The entire code base is deployed in the Kubernetes cluster as a compiled C-Extention!

## Current State

The first MVP is stable and offers the most critical features for efficient DepthCache management. Future improvements 
might include switching to websockets instead of REST queries, or implementing simultaneous queries for both Asks and 
Bids. [Vote here for new features!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

For more information, check out the 
[GitHub Repository](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster) and the
[Docs](https://unicorn-binance-depth-cache-cluster.docs.lucit.tech).

## Installation

- Get a Kubernetes Cluster of your choice and connect `kubectl`. 
- Install dependencies:
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Helm Chart
- [Install Helm](https://helm.sh/docs/intro/install) 
- Prepare `helm`:

``` 
helm repo add lucit-ubdcc https://unicorn-binance-depth-cache-cluster.docs.lucit.tech/helm
helm repo update
```

- Install the UNICORN DepthCache Cluster for Binance:

``` 
helm install lucit-ubdcc lucit-ubdcc/lucit-ubdcc
```

- Get the "LoadBalancer Ingress" IP, the default Port is TCP 80:

```
kubectl describe services lucit-ubdcc-restapi
```

#### Choose an explizit version
- Find a version to choose
``` 
helm search repo lucit-ubdcc
``` 
- Then
``` 
helm install lucit-ubdcc lucit-ubdcc/lucit-ubdcc --version 0.1.3
``` 

#### Choose a namespace
``` 
helm install lucit-ubdcc lucit-ubdcc/lucit-ubdcc --namespace lucit-ubdcc
``` 

#### Choose an alternate public port
``` 
helm install lucit-ubdcc lucit-ubdcc/lucit-ubdcc --set publicPort.restapi=8080
``` 
  
### Kubernetes Deployment
- [Download the deployment files](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depth-cache-cluster/tree/master/admin/k8s)
- Apply the deployment files with `kubectl`
    ``` 
    kubectl apply -f ./setup/01_namespace_lucit-ubdcc.yaml
    kubectl apply -f ./setup/02_role_lucit-ubdcc.yaml
    kubectl apply -f ./setup/03_rolebinding_lucit-ubdcc.yaml
    kubectl apply -f ./lucit-ubdcc-dcn.yaml  
    kubectl apply -f ./lucit-ubdcc-mgmt.yaml
    kubectl apply -f ./lucit-ubdcc-mgmt_service.yaml
    kubectl apply -f ./lucit-ubdcc-restapi.yaml
    kubectl apply -f ./lucit-ubdcc-restapi_service.yaml
    ```
- Get the "LoadBalancer Ingress" IP, the default Port is TCP 80:
    ```
    kubectl describe services lucit-ubdcc-restapi
    ```
  
## Uninstallation
```
kubectl delete -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Helm Chart

```
helm uninstall lucit-ubdcc
```

### Kubernetes Deployment
- Delete the deployment with `kubectl`
    ``` 
    kubectl delete -f ./setup/01_namespace_lucit-ubdcc.yaml
    kubectl delete -f ./setup/02_role_lucit-ubdcc.yaml
    kubectl delete -f ./setup/03_rolebinding_lucit-ubdcc.yaml
    kubectl delete -f ./lucit-ubdcc-dcn.yaml  
    kubectl delete -f ./lucit-ubdcc-mgmt.yaml
    kubectl delete -f ./lucit-ubdcc-mgmt_service.yaml
    kubectl delete -f ./lucit-ubdcc-restapi.yaml
    kubectl delete -f ./lucit-ubdcc-restapi_service.yaml
    ```

## Accessing the DepthCaches

The UNICORN DepthCache Cluster for Binance is accessed with the Python module [UNICORN Binance Local Depth Cache](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache?tab=readme-ov-file#connect-to-a-unicorn-depthcache-cluster-for-binance).

Just try this [examples](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-local-depth-cache/tree/master/examples/unicorn_depthcache_cluster_for_binance)!

## How to report Bugs or suggest Improvements?
[List of planned features](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) - click ![thumbs-up](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-suite/master/images/misc/thumbup.png) if you need one of them or suggest a new feature!

Before you report a bug, [try the latest release](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster#installation-and-upgrade). If the issue still exists, provide the error trace, OS 
and Python version and explain how to reproduce the error. A demo script is appreciated.

If you don't find an issue related to your topic, please open a new [issue](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/issues)!

[Report a security bug!](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/security/policy)

## Contributing
[UNICORN Binance DepthCache Cluster](https://www.lucit.tech/unicorn-binance-depthcache-cluster.html) is an open 
source project which welcomes contributions which can be anything from simple documentation fixes and reporting dead links to new features. To 
contribute follow 
[this guide](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/blob/master/CONTRIBUTING.md).
 
### Contributors
[![Contributors](https://contributors-img.web.app/image?repo=oliver-zehentleitner/unicorn-binance-depthcache-cluster)](https://github.com/LUCIT-Systems-and-Development/unicorn-binance-depthcache-cluster/graphs/contributors)

We ![love](https://raw.githubusercontent.com/lucit-systems-and-development/unicorn-binance-suite/master/images/misc/heart.png) open source!

## Disclaimer
This project is for informational purposes only. You should not construe this information or any other material as 
legal, tax, investment, financial or other advice. Nothing contained herein constitutes a solicitation, recommendation, 
endorsement or offer by us or any third party provider to buy or sell any securities or other financial instruments in 
this or any other jurisdiction in which such solicitation or offer would be unlawful under the securities laws of such 
jurisdiction.

### If you intend to use real money, use it at your own risk!

Under no circumstances will we be responsible or liable for any claims, damages, losses, expenses, costs or liabilities 
of any kind, including but not limited to direct or indirect damages for loss of profits.

## Commercial Support

[![Get professional and fast support](https://raw.githubusercontent.com/LUCIT-Systems-and-Development/unicorn-trading-suite/master/images/support/LUCIT-get-professional-and-fast-support.png)](https://www.lucit.tech/get-support.html)

***Do you need a developer, operator or consultant?*** [Contact us](https://www.lucit.tech/contact.html) for a non-binding initial consultation!
