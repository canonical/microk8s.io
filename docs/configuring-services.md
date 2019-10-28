---
layout: docs
title: "MicroK8s command reference"
permalink: /docs/configuring-services
---

# Configuring MicroK8s services

MicroK8s brings up Kubernetes as a number of different services run through
`sytemd`. The configuration of these services is read from files stored
in the $SNAP_DATA directory, which normally points to
`/var/snap/microk8s/current`.

To reconfigure a service you will need to edit the corresponding file and then
restart the respective daemon. For example, to add `debug` level logging to
containerd:

```bash
echo '-l=debug' | sudo tee -a /var/snap/microk8s/current/args/containerd
sudo systemctl restart snap.microk8s.daemon-containerd.service
```

The following systemd services will be run by MicroK8s:


### snap.microk8s.daemon-apiserver

The Kubernetes API server validates and configures data for the API objects
which include pods, services, replication controllers, and others. The API
Server services REST operations and provides the frontend to the cluster’s
shared state through which all other components interact.

The service configuration is described in full in the upstream  
[kube-apiserver documentation][kube-apiserver].

**Default configuration**:

```yaml
--cert-dir=${SNAP_DATA}/certs
--service-cluster-ip-range=10.152.183.0/24
--authorization-mode=AlwaysAllow
--basic-auth-file=${SNAP_DATA}/credentials/basic_auth.csv
--service-account-key-file=${SNAP_DATA}/certs/serviceaccount.key
--client-ca-file=${SNAP_DATA}/certs/ca.crt
--tls-cert-file=${SNAP_DATA}/certs/server.crt
--tls-private-key-file=${SNAP_DATA}/certs/server.key
--kubelet-client-certificate=${SNAP_DATA}/certs/server.crt
--kubelet-client-key=${SNAP_DATA}/certs/server.key
--secure-port=16443
--token-auth-file=${SNAP_DATA}/credentials/known_tokens.csv
--token-auth-file=${SNAP_DATA}/credentials/known_tokens.csv
--etcd-servers='https://127.0.0.1:12379'
--etcd-cafile=${SNAP_DATA}/certs/ca.crt
--etcd-certfile=${SNAP_DATA}/certs/server.crt
--etcd-keyfile=${SNAP_DATA}/certs/server.key
--insecure-port=0

# Enable the aggregation layer
--requestheader-client-ca-file=${SNAP_DATA}/certs/front-proxy-ca.crt
--requestheader-allowed-names=front-proxy-client
--requestheader-extra-headers-prefix=X-Remote-Extra-
--requestheader-group-headers=X-Remote-Group
--requestheader-username-headers=X-Remote-User
--proxy-client-cert-file=${SNAP_DATA}/certs/front-proxy-client.crt
--proxy-client-key-file=${SNAP_DATA}/certs/front-proxy-client.key
#~Enable the aggregation layer
```

### snap.microk8s.daemon-containerd

[Containerd](https://containerd.io/) is the container runtime used by MicroK8s
to manage images and execute containers.

The containerd daemon started using the configuration in
`${SNAP_DATA}/args/containerd` and `${SNAP_DATA}/args/containerd-template.toml`.

**Defaults:**

${SNAP_DATA}/args/containerd:

```yaml
--config ${SNAP_DATA}/args/containerd.toml
--root ${SNAP_COMMON}/var/lib/containerd
--state ${SNAP_COMMON}/run/containerd
--address ${SNAP_COMMON}/run/containerd.sock
```

### snap.microk8s.daemon-controller-manager

The Kubernetes controller manager is a daemon that embeds the core control
loops shipped with Kubernetes. In Kubernetes, a controller is a control loop
which watches the shared state of the cluster through the apiserver and makes
changes attempting to move the current state towards the desired state.

The kube-controller-manager daemon is started using the arguments in
`${SNAP_DATA}/args/kube-controller-manager`. For more detail on these
arguments, see the upstream
[kube-controller-manager documentation][kube-controller-manager].

### snap.microk8s.daemon-etcd

Etcd is a key/value datastore used to support the components of Kubernetes.

The etcd daemon is started using the arguments in `${SNAP_DATA}/args/etcd`. For
more information on the configuration, see the [etcd documentation][etcd]. Note
that different channels of MicroK8s may use different versions of etcd.


**Defaults:**

```ỳaml
--data-dir=${SNAP_COMMON}/var/run/etcd
--advertise-client-urls=https://${DEFAULT_INTERFACE_IP_ADDR}:12379
--listen-client-urls=https://0.0.0.0:12379
--client-cert-auth
--trusted-ca-file=${SNAP_DATA}/certs/ca.crt
--cert-file=${SNAP_DATA}/certs/server.crt
--key-file=${SNAP_DATA}/certs/server.key
```

### snap.microk8s.daemon-kubelet

The kubelet is the primary “node agent” that runs on each node. The kubelet
takes a set of PodSpecs(a YAML or JSON object that describes a pod) that are
provided and ensures that the containers described in those PodSpecs are
running and healthy. The kubelet doesn’t manage containers which were not
created by Kubernetes.

The kubelet daemon is started using the arguments in
`${SNAP_DATA}/args/kubelet`. These are fully documented in the upstream
[kubelet documentation][kubelet].

### snap.microk8s.daemon-proxy

The Kubernetes network proxy runs on each node. This reflects services as
defined in the Kubernetes API on each node and can do simple TCP, UDP, and SCTP
stream forwarding or round robin TCP, UDP, and SCTP forwarding across a set of
backends.

The kube-proxy daemon is started using the arguments in
`${SNAP_DATA}/args/kube-proxy`. For more details see the upstream
[kube-proxy documentation][kube-proxy].

### snap.microk8s.daemon-scheduler

The Kubernetes scheduler is a workload-specific function which takes into
account individual and collective resource requirements, quality of service
requirements, hardware/software/policy constraints, affinity and anti-affinity
specifications, data locality, inter-workload interference, deadlines, and so
on. Workload-specific requirements will be exposed through the API as
necessary.

The kube-scheduler daemon started using the arguments in
`${SNAP_DATA}/args/kube-scheduler`. These are explained fully in the
upstream [kube-scheduler documentation][kube-scheduler].


To reconfigure a service you will need to edit the corresponding file and then restart the respective daemon. For example:



<!-- LINKS -->

[kube-apiserver]: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/
[kube-scheduler]: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/
[kube-controller-manager]: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/
[kube-proxy]: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/
[etcd]: https://etcd.io/docs/v3.4.0/op-guide/configuration/
[kubelet]: https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/
