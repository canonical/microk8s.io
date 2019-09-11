---
layout: docs
title: "Muli-node Clusters"
---
# Muli-node Clusters


Forming a cluster out of two or more already running MicroK8s instances is done through
the `microk8s.add-node` command. The MicroK8s instace on which this command is
run will be the master of the cluster and will host the kubernetes control plane:
```
> microk8s.add-node 
Join node with: microk8s.join ip-172-31-20-243:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf

If the node you are adding is not reachable through the default interface you can use one of the following:
 microk8s.join 10.1.84.0:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
 microk8s.join 10.22.254.77:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
```

As shown, `add-node` produces a random, single use token ("DDOkUupkmaBezNnMheTBqFYHLWINGDbf" in this example)
and displays a message on how a node is to be added to the cluster.
On the MicroK8s instance that we want to turn into a node we have to:
```
> microk8s.join ip-172-31-20-243:25000/DDOkUupkmaBezNnMheTBqFYHLWINGDbf
```

Joining a node to the cluster should only take a few seconds. Afterwards you should be able
to see the node with:
```
> microk8s.kubectl get no
NAME               STATUS   ROLES    AGE   VERSION
10.22.254.79       Ready    <none>   27s   v1.15.3
ip-172-31-20-243   Ready    <none>   53s   v1.15.3
```

To remove a node from the cluster we call the `microk8s.remove` command
and provide the name of the node we want to remove:
```
> microk8s.remove 10.22.254.79
```

On the removed node we can call `microk8s.leave` so that MicroK8s starts
its own control plane and start acting as a full single node cluster:
```
> microk8s.leave
```
