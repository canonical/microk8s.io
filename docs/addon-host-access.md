---
layout: docs
title: "Host-access addon"
permalink: /docs/addon-host-access
---

# Host-access addon

The host-access addon enables access of services running on the host machine via a fixed IP.
This becomes useful when your machine changes IPs as you hop through different networks.

You can install this addon with:

```bash
microk8s enable host-access
```

A new local network interface named `lo:microk8s` is created with a default IP address of `10.0.1.1`.

Alternatively, provide a different IP address when enabling the addon:
```bash
microk8s enable host-access:ip=<desired-ip>
```


<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-host-access.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
