---
layout: docs
title: "Install behind a proxy"
permalink: /docs/install-proxy
---

# Install behind a proxy

To let MicroK8s use a proxy enter the proxy details in 
`${SNAP_DATA}/args/containerd-env` (normally `/var/snap/microk8s/current/args/containerd-env`) and restart with:

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
