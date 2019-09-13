---
layout: docs
title: "Multi-node MicroK8s"
---
# Multi-node MicroK8s

## Adding a node

To create a cluster out of two or more already-running MicroK8s instances,
use the `microk8s.add-node` command. The MicroK8s instance on which this
command is
run will be the master of the cluster and will host the Kubernetes
control plane:
```
> microk8s.add-node
Join node with: microk8s.join ip-172-31-20-243:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf

If the node you are adding is not reachable through the default
interface you can use one of the following:
 microk8s.join 10.1.84.0:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
 microk8s.join 10.22.254.77:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
```

The `add-node` command prints a `microk8s.join` command which should
be executed on the MicroK8s instance that you wish to join to this
cluster:
```
> microk8s.join ip-172-31-20-243:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
```

Joining a node to the cluster should only take a few seconds. Afterwards
you should be able to see the node has joined:
```
> microk8s.kubectl get no
NAME               STATUS   ROLES    AGE   VERSION
10.22.254.79       Ready    <none>   27s   v1.15.3
ip-172-31-20-243   Ready    <none>   53s   v1.15.3
```

## Removing a node

To remove a node from the cluster, use `microk8s.remove-node`:
```
> microk8s.remove-node 10.22.254.79
```

Finally, qn the removed node, run `microk8s.leave`. MicroK8s will restart
its own control plane and resume operations as a full single node cluster:
```
> microk8s.leave
```