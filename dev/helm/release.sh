cd ./dev/helm/
helm package ./lucit-ubdcc/
helm repo index . --url https://unicorn-binance-depth-cache-cluster.docs.lucit.tech/helm
cp index.yaml ../../docs/helm/
cp *.tgz ../../docs/helm/