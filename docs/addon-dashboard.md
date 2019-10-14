---
layout: docs
title: "Dashboardaddon"
permalink: /docs/addon-dashboard
---

# Dashboard addon

The standard Kubernetes Dashboard is a convenient way to keep track of the
activity and resource use of MicroK8s

To log in to the Dashboard, you will need the access token (unless RBAC has
also been enabled). This is generated randomly on deployment, so a few commands
are needed to retrieve it:

```bash
token=$(microk8s.kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s.kubectl -n kube-system describe secret $token
```
In an RBAC enabled setup (microk8s.enable RBAC) you need to create a user with
restricted permissions as detailed in the
[upstream Dashboard wiki][upstream-dashboard]

Next, you need a connection to the API server. While the MicroK8s snap will
have an IP address on your local network, the recommended way to do this is
through the proxy service. You can initiate the proxy with the command:

```bash
microk8s.kubectl proxy --accept-hosts=.* --address=0.0.0.0 &
```

You can then access the Dashboard at the address

[http://127.0.0.1:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/]()

![IMAGE of Dashboard](#ref)

[upstream-dashboard]: https://github.com/kubernetes/dashboard/wiki/Creating-sample-user
