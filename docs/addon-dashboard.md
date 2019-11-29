---
layout: docs
title: "Dashboard addon"
permalink: /docs/addon-dashboard
---

# Dashboard addon

The standard Kubernetes Dashboard is a convenient way to keep track of the
activity and resource use of MicroK8s

```bash
microk8s.enable dashboard
```

To log in to the Dashboard, you will need the access token (unless RBAC has
also been enabled). This is generated randomly on deployment, so a few commands
are needed to retrieve it:

```bash
token=$(microk8s.kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s.kubectl -n kube-system describe secret $token
```
In an RBAC enabled setup (`microk8s.enable rbac`) you need to create a user with
restricted permissions as detailed in the
[upstream Dashboard access control documentation ][upstream-dashboard]

Next, you need to connect to the dashboard service. While the MicroK8s snap will
have an IP address on your local network (the Cluster IP of the kubernetes-dashboard service),
you can also reach the dashboard by forwarding its port to a free one on your host with:

```bash
microk8s.kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
```

You can then access the Dashboard at [https://127.0.0.1:10443]()

If you are running MicroK8s in a VM and you need to expose the Dashboard to other hosts, you
should also use the `--address [IP_address_that_your_browser's_host_has]` option. Set this option
to `--address 0.0.0.0` to make the Dashboard public. For example: 

```bash
microk8s.kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443 --address 0.0.0.0
```

Visit the [upstream dashboard documentation][upstream-access-dashboard] to find out other ways to reach the Dashboard.



![IMAGE of Dashboard](https://assets.ubuntu.com/v1/c9cec03a-ubuntu18.04-microk8s+on+QEMU-KVM_007.png)
[upstream-dashboard]: https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/README.md#admin-privileges
[upstream-access-dashboard]: https://github.com/kubernetes/dashboard/blob/master/docs/user/accessing-dashboard/1.7.x-and-above.md
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-dashboard.md" class="p-notification__action">edit this page</a>
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
