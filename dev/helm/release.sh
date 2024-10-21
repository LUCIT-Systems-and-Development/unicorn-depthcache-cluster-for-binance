cd ./docs/helm
helm package ../../dev/helm/lucit-ubdcc/
helm repo index . --url https://unicorn-binance-depth-cache-cluster.docs.lucit.tech/helm
