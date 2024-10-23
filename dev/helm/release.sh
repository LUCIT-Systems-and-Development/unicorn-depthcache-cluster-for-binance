cd ./docs/helm
helm package ../../dev/helm/lucit-ubdcc/
helm repo index . --url https://unicorn-depthcache-cluster-for-binance.docs.lucit.tech/helm
