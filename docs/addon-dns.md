---
layout: docs
title: "dns addon"
permalink: /docs/addon-dns
---

# DNS addon


This deploys CoreDNS to supply address resolution services to
Kubernetes.

This service is commonly required by other addons, so it is
recommended that you enable it.

```bash
microk8s.enable dns
```

By default it points to Google's `8.8.8.8` and `8.8.4.4` servers for resolving
addresses. This can be changed by running the command:

```bash
microk8s.kubectl -n kube-system edit configmap/coredns
```

This will invoke the `vim` editor so that you can alter the configuration.

The addon can be disabled at any time:

```bash
microk8s.disable dns
```

...but bear in mind this could have implications for services and pods which
may be relying on it.
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-dns.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
