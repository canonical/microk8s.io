---
layout: docs
title: "MicroK8s command reference"
permalink: /docs/commands
---

# Command Reference

MicroK8s adds a number of commands, grouped together with a 'microk8s.' prefix
for convenience.

-   [microk8s.add-node](#microk8s.add-node)
-   [microk8s.config](#microk8s.config)
-   [microk8s.ctr](#microk8s.ctr)
-   [microk8s.disable](#microk8s.disable)
-   [microk8s.enable](#microk8s.enable)
-   [microk8s.inspect](#microk8s.inspect)
-   [microk8s.join](#microk8s.join)
-   [microk8s.kubectl](#microk8s.kubectl)
-   [microk8s.leave](#microk8s.leave)
-   [microk8s.remove-node](#microk8s.remove-node)  
-   [microk8s.reset](#microk8s.reset)
-   [microk8s.start](#microk8s.start)
-   [microk8s.status](#microk8s.status)
-   [microk8s.stop](#microk8s.stop)

## Addon helper commands

Some commands are specific to particular addons (e.g.
`microk8s.cilium`) and may not do anything useful if the respective addon is
not currently enabled. For more information on these commands, see the
[Addon documentation](addons).

-   `microk8s.cilium`
-   `microk8s.helm`
-   `microk8s.istioctl`
-   `microk8s.linkerd`

---
<a id="microk8s.add-node"> </a>
### microk8s.add-node

**Usage:** `microk8s.add-node`

**Options:**

**Description:**
Running this command will generate a connection string and output a list of
suggested `microk8s.join` commands to add an additional MicroK8s node to
the current cluster.

**Examples:**

`microk8s.add-node`

...will result in output similar to:

```no-highlight
Join node with: microk8s.join 192.168.0.2:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl

If the node you are adding is not reachable through the default interface you can
use one of the following:
 microk8s.join 192.168.0.2:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 192.168.250.1:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 10.57.200.1:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 10.128.63.1:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 172.17.0.1:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 10.1.37.68:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
 microk8s.join 192.168.122.1:25000/eLCTbltkDzxOnSKAkmVMbOPYgSrAieEl
```

---

<a id="microk8s.config"> </a>
### microk8s.config

**Usage:** `microk8s.config [-l]`

**Options:**

-   `-l, --use-loopback` : Report the cluster address using the loopback
     address (127.0.0.1) rather than the default interface address.

**Description:**
Retrieves and outputs the current config information from MicroK8s (similar
to that returned by `kubectl`).

**Examples:**

`microk8s.config`

...will result in output similar to:

```no-highlight
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURCRENDQWV5Z0F3SUJBZ0lKQVBQMGhoaFduTTR0TUEwR0NTcUdTSWIzRFFFQkN3VUFNQmN4RlRBVEJnTlYKQkFNTURERXdMakUxTWk0eE9ETXVNVEFlRncweE9URXdNVFl3T1RRNE5UaGFGdzAwTnpBek1ETXdPVFE0TlRoYQpNQmN4RlRBVEJnTlZCQU1NRERFd0xqRTFNaTR4T0RNdU1UQ0NBU0l3RFFZSktvWklodmNOQVFFQkJRQURnZ0VQCkFEQ0NBUW9DZ2dFQkFQbWpiZ3F6NWxTL3FlTldlcDduVE9NUS94NXp6MUI5bGR3dTJkZkVxbEtIRXVWT3RZYU0KeVJMb0xtYmZBbUxTd2ZDSXIycWhyZ1UxTlFTd096WUVCeXpNZ01WaWtzejZlVjJ3Um10b3RxbXpXLzZHQTh1SQpmM1MvTURERHh2ZmQva1hrb2lpeTE5WCtPVENDTHFUTmJZRG45RkdRTjJWSVVzVWV5Z255LzJjbkpDb0xLTGtBCm04NHVTUXBLYUJ1T3hzeFZBU3J6cURINk1uczN5Y0pyWXRqSG9BaDBTcWxFdHhKblpGOGJpTGx2Q2lRVkMyNE4KQ2IyMkpRMHVyQWFRUlBIRmRsaGtKU1RBL2Y0VFp1VDN2N2tpaU9QZWpGT252M0lXYld3UXZRYU5ad0JmM0NQQwozK0dIRXNSU1NPYkQ5Z2FGODhVTXNScEM1TFBaVm12eFFVc0NBd0VBQWFOVE1GRXdIUVlEVlIwT0JCWUVGUElKCmp6ZWhaYW1nS0xPSkQyVitiU3VMaHFjU01COEdBMVVkSXdRWU1CYUFGUElKanplaFphbWdLTE9KRDJWK2JTdUwKaHFjU01BOEdBMVVkRXdFQi93UUZNQU1CQWY4d0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dFQkFIOVlPaGRMT3RXKwpxbkhnajRYMjcwSWRFNDNlc3JRRENEUnY4UGpRVmVwYytNUEdrMU10cFNsckgvTkNnc2puMzZ2RmpFeUJzcXFJCkh4QmhPdi9wR3NIUHdUa2p3bXNSYkdwWkliQTdRcGNKSTZlaEM4aFUwSmI2b3ZwSU9zZnR6SFF6SVA4NWRhOEsKWGptbVY2UzNLQnZtZlpKMU1WZzFuUFBGYnpBdVhoaXI0RmFvZ3AzL2lwNkVFdWtYNUYydnQvVDdSaC9XODFDNQphUFhpTDdSMTUxQm9aU3U2Y2ZUdGx2Y092cW9DSDFvaXlvWlJIV2dSeElPVTU2dXVuRXlUdVNoMjJnbGVSSlAyCk8xWk9rNEVBS3VNMEsra05SeEVvcXNmeFliYlZicENvbGVJRXlLUVhhNzJJU0RrdlVWRmhRMkxGZTJ1bmtvRDgKY2JZbVAxVU1tZ009Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    server: https://192.168.0.2:16443
  name: microk8s-cluster
contexts:
- context:
    cluster: microk8s-cluster
    user: admin
  name: microk8s
current-context: microk8s
kind: Config
preferences: {}
users:
- name: admin
  user:
    username: admin
    password: S05BcnhqaWpCNzlRaWtDZEIzNHEzVU5qKzZCaERUbWxjQ2d6VTFmcjkrQT0K

```
---
<a id="microk8s.ctr"> </a>
### microk8s.ctr

**Usage:** `microk8s.ctr [command]`

**Options:**

-   any ctr command: see below

**Description:**
This command provides access to the containerd CLI command `ctr`. It is
provided as a convenience, for more information on
using `ctr`, please see the relevant manpage with `man ctr` or run the built-in
help with `microk8s.ctr`.

**Examples:**

`microk8s.ctr version`

...will result in output similar to:

```no-highlight
Client:
  Version:  v1.2.5
  Revision: bb71b10fd8f58240ca47fbb579b9d1028eea7c84
```

---

<a id="microk8s.disable"> </a>
### microk8s.disable

**Usage:** `microk8s.disable addon [addon ...]`

**Options:**

-   *addon* : The name of the addon to disable.

**Description:**
MicroK8s addons can be enabled or disabled at any time. This command accepts
the name of an addon and then proceeds to make the necessary changes to remove
it from the current node. Note that some services and applications may not
continue to work properly if addons are removed.

**Examples:**

`microk8s.disable dns`

...will usually result in output detailing what has been done. In this case,
the ouput will be similar to:

```no-highlight
Disabling DNS
Reconfiguring kubelet
Removing DNS manifest
serviceaccount "coredns" deleted
configmap "coredns" deleted
deployment.apps "coredns" deleted
service "kube-dns" deleted
clusterrole.rbac.authorization.k8s.io "coredns" deleted
clusterrolebinding.rbac.authorization.k8s.io "coredns" deleted

```

---

<a id="microk8s.enable"> </a>
### microk8s.enable

**Usage:** `microk8s.enable addon [addon ... ]`

**Options:**

-   *addon* : The name of the addon to enable.

**Description:**
MicroK8s addons can be enabled or disabled at any time. This command accepts
the name of an addon and then proceeds to make the necessary changes to
MicroK8s to enable it. For more details, see the documentation for the
specific addon in question in the [addons documentation](addons).

For a list of the current available addons, and whether or not they are
enabled, run `microk8s.status`.

**Examples:**

`microk8s.enable storage`

...will result in output similar to:

```no-highlight
Enabling default storage class
deployment.apps/hostpath-provisioner created
storageclass.storage.k8s.io/microk8s-hostpath created
serviceaccount/microk8s-hostpath created
clusterrole.rbac.authorization.k8s.io/microk8s-hostpath created
clusterrolebinding.rbac.authorization.k8s.io/microk8s-hostpath created
Storage will be available soon
```

---

<a id="microk8s.inspect"> </a>
### microk8s.inspect

**Usage:** `microk8s.inspect`

**Options:**


**Description:**
This command creates a detailed profile of the current state of the running
MicroK8s. This is primarily useful for troubleshooting and reporting bugs.

**Examples:**

`microk8s.inspect`

...will result in output similar to:

```no-highlight
Inspecting services
  Service snap.microk8s.daemon-cluster-agent is running
  Service snap.microk8s.daemon-flanneld is running
  Service snap.microk8s.daemon-containerd is running
  Service snap.microk8s.daemon-apiserver is running
  Service snap.microk8s.daemon-apiserver-kicker is running
  Service snap.microk8s.daemon-proxy is running
  Service snap.microk8s.daemon-kubelet is running
  Service snap.microk8s.daemon-scheduler is running
  Service snap.microk8s.daemon-controller-manager is running
  Service snap.microk8s.daemon-etcd is running
  Copy service arguments to the final report tarball
Inspecting AppArmor configuration
Gathering system information
  Copy processes list to the final report tarball
  Copy snap list to the final report tarball
  Copy VM name (or none) to the final report tarball
  Copy disk usage information to the final report tarball
  Copy memory usage information to the final report tarball
  Copy server uptime to the final report tarball
  Copy current linux distribution to the final report tarball
  Copy openSSL information to the final report tarball
  Copy network configuration to the final report tarball
Inspecting kubernetes cluster
  Inspect kubernetes cluster

Building the report tarball
  Report tarball is at /var/snap/microk8s/982/inspection-report-20191017_180222.tar.gz

```

---

<a id="microk8s.join"> </a>
### microk8s.join

**Usage:** `microk8s.join <master>:<port>/<token>`

**Options:**

**Description:**
Used to join the local MicroK8s node in to a remote cluster. An 'invitation' in
the form of a token is required, which is issued by running the
`microk8s.add-node` command on the master MicroK8s node.

Running `microk8s.add-node` will output a number of different commands which can
be used from the node wishing to join, taking into account different
network addressing. The `microk8s.join` command will need the address and port
number of the master node, as well as the token, in order for this command to
be successful.

**Examples:**

`microk8s.join 10.128.63.163:25000/JGoShFJfHtbieSOsMhmkgsOHrwtxDKRH`

---

<a id="microk8s.kubectl"> </a>
### microk8s.kubectl

**Usage:** `microk8s.kubectl [command]`

**Options:**

-   any `kubectl` command : See description.

**Description:**
This command runs the standard Kubernetes `kubectl` which ships with MicroK8s.

**Examples:**

`microk8s.kubectl get all`

...will result in output similar to:

```no-highlight
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.152.183.1   <none>        443/TCP   108m

```

---

<a id="microk8s.leave"> </a>
### microk8s.leave

**Usage:** `microk8s.leave`

**Options:**

**Description:**
When run on a node which has previously joined a cluster with `microk8s.join`,
this command will remove the current node from the cluster and return it to
single node operation.

**Examples:**

`microk8s.leave`

---

<a id="microk8s.remove-node"> </a>
### microk8s.remove-node

**Usage:** `microk8s.remove-node address`

**Options:**

-   address : The address of the node to be removed

**Description:**
Removes a specified node from the current cluster. The node should be
identified by hostname/IP address by which it is known to the cluster. To
retrieve this information you can run:

`microk8s.kubectl get nodes`

This command only works on the master node of the cluster. To remove the local
node from a remote cluster, see [`microk8s.leave`](#microk8s.leave).

**Examples:**

`microk8s.remove-node 10.128.63.163`

---

<a id="microk8s.reset"> </a>
### microk8s.reset

**Usage:** `microk8s.reset [--destroy-storage]`

**Options:**

-   `--destroy-storage` : Also deletes any files which may have been created by the storage addon.


**Description:**
This command is used to return the MicroK8s node to the default initial state.
This process may take some time and will remove any resources, authentication,
running services, pods and optionally, storage. All addons will be disabled and
the configuration will be reinitialised.

This commands makes it easy to revert your MicroK8s to an 'install fresh' state
wihout having to reinstall anything.

**Examples:**

`microk8s.reset`

...will result in output similar to:

```no-highlight
Calling clean_cluster
Cleaning resources in namespace default
No resources found
endpoints "kubernetes" deleted
secret "default-token-5lqdh" deleted
serviceaccount "default" deleted
service "kubernetes" deleted
...

```

---

<a id="microk8s.start"> </a>
### microk8s.start

**Usage:** `microk8s.start`

**Options:**

**Description:**
Will start MicroK8s, if the MicorK8s node has previously been halted
with `microk8s.stop`.

**Examples:**

`microk8s.start`

...will result in output similar to:

```no-highlight
Started.
Enabling pod scheduling
node/ubuntu1804 already uncordoned
```

---

<a id="microk8s.status"> </a>
### microk8s.status

**Usage:** `microk8s.status`

**Options:**

**Description:**
This command outputs some useful status information, including the current state
of the MicroK8s node, and a list of all the available extensions, indicating
which ones are enabled/disabled.

**Examples:**

`microk8s.status`

...will result in output similar to:

```no-highlight
microk8s is running
addons:
cilium: disabled
linkerd: disabled
jaeger: disabled
rbac: disabled
prometheus: disabled
dns: disabled
fluentd: disabled
storage: disabled
gpu: disabled
registry: disabled
knative: disabled
dashboard: disabled
ingress: disabled
metrics-server: disabled
istio: disabled
```

---

<a id="microk8s.stop"> </a>
### microk8s.stop

**Usage:** `microk8s.stop`

**Options:**

**Description:**
Halts the current MicroK8s node.

**Examples:**

`microk8s.stop`

...will result in output describing the shutdown process.

---



<!-- LINKS-->

[kubectl-docs]: https://kubernetes.io/docs/reference/kubectl/kubectl/
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/commands.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
