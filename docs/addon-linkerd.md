---
layout: docs
title: "Linkerd addon"
permalink: /docs/addon-linkerd
---

# linkerd

Enabling this addon will deploy the necessary services and proxies for the
linkerd service mesh.

```bash
microk8s.enable linkerd
```

Linkerd includes a command line utility. For convenience, MicroK8s ships
with this utility. You can verify that the utility and linkerd are
configured and working by running:

```bash
microk8s.linkerd check
```

For more on linkerd, see the
[linkerd documentation][linkerd-docs].

<!-- LINKS -->

[linkerd-docs]: https://linkerd.io/2/overview/

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-linkerd.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
