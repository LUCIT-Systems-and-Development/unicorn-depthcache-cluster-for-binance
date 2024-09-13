export LUCIT_UBDCC_DEV_MODE=TRUE

docker run -d \
  --name etcd \
  -p 2379:2379 \
  -p 2380:2380 \
  --env ALLOW_NONE_AUTHENTICATION=yes \
  --env ETCD_ENABLE_V2=false \
  bitnami/etcd:latest
