# Metrics Server

# Run without certificate

Find   
name: metrics-server

namespace: kube-system

then add " - --kubelet-insecure-tls" into spec.container.arg
