---
layout: docs
title: "Install behind a proxy"
permalink: /docs/install-proxy
---

# Install behind a proxy

To let MicroK8s use a proxy we need to enter the proxy details in 
`${SNAP_DATA}/args/containerd-env` (normally `/var/snap/microk8s/current/args/containerd-env`). The `containerd-env` file holds the environment variables containerd runs with. Setting the `HTTPS_PROXY` to your proxy endpoint enables containerd to fetch conatiner images from the web. Here is an example where `HTTPS_PROXY` is set to `https://squid.internal:3128`:

```
HTTPS_PROXY=https://squid.internal:3128
#
# Some additional environment variables
#
ulimit -n 65536 || true
ulimit -l 16384 || true
```

For the changes to take effect we need to restart MicroK8s:

```bash
microk8s.stop
microk8s.start
```

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/install-proxy.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
