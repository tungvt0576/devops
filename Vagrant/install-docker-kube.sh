#!/bin/bash

# Cai dat Docker
apt-get update
apt-get -y install ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update && apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# usermod -aG docker $(whoami)
## Create /etc/docker directory.
# mkdir /etc/docker

# Setup daemon.
# cat > /etc/docker/daemon.json <<EOF
# {
#   "exec-opts": ["native.cgroupdriver=systemd"],
#   "log-driver": "json-file",
#   "log-opts": {
#     "max-size": "100m"
#   },
#   "storage-driver": "overlay2",
#   "storage-opts": [
#     "overlay2.override_kernel_check=true"
#   ]
# }
# EOF

# mkdir -p /etc/systemd/system/docker.service.d


# # Restart Docker
# systemctl enable docker.service
# systemctl daemon-reload
# systemctl restart docker


# Tat SELinux
# setenforce 0
# sed -i --follow-symlinks 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/sysconfig/selinux

# Tat Firewall
systemctl disable ufw >/dev/null 2>&1

# sysctl
cat >>/etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system >/dev/null 2>&1

# Tat swap
sed -i '/swap/d' /etc/fstab
swapoff -a

# Add apt repo file for Kubernetes
apt-get update
apt-get install -y apt-transport-https
curl -fsSL https://dl.k8s.io/apt/doc/apt-key.gpg | gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl

# Configure NetworkManager before attempting to use Calico networking.
apt-get update
apt-get -y install network-manager

# Check if the /etc/NetworkManager/conf.d/ directory exists
if [ ! -d "/etc/NetworkManager/conf.d/" ]; then
  # Create the /etc/NetworkManager/conf.d/ directory if it doesn't exist
  mkdir -p /etc/NetworkManager/conf.d/
fi

# Append the Calico configuration to /etc/NetworkManager/conf.d/calico.conf
sh -c 'cat >>/etc/NetworkManager/conf.d/calico.conf<<EOF
[keyfile]
unmanaged-devices=interface-name:cali*;interface-name:tunl*
EOF'

# Restart the NetworkManager service to apply the changes
systemctl restart NetworkManager
