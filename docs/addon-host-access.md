---
layout: docs
title: "Host-acces addon"
permalink: /docs/addon-host-access
---

# Host-access addon

The host-access addon enables access of services running on the host machine via a fixed IP.
This becomes useful when your machine changes IPs as you hope through different networks. 

You can install this addon with:

```bash
microk8s enable host-access
```

The local network interface created is named `lo:microk8s` and the IP assigned by default is `10.0.1.1`.

We can provide a different IP with:
```bash
microk8s enable host-access:ip=<desired-ip>
```


<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-dashboard.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
