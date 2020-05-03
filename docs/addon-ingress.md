---
layout: docs
title: "ingress addon"
permalink: /docs/addon-ingress
---

# Ingress addon

This addon enables NGINX Ingress Controller for MicroK8s.

```bash
microk8s enable ingress
```

With the Ingress addon enabled, a HTTP/HTTPS ingress rule can be created with
an Ingress resource. For example:

```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: http-ingress
spec:
  rules:
  - http:
      paths:
      - path: /
        backend:
          serviceName: some-service
          servicePort: 80
```

Additionally, the Ingress addon can be configured to expose TCP and UDP
services by editing the `nginx-ingress-tcp-microk8s-conf` and
`nginx-ingress-udp-microk8s-conf` ConfigMaps respectively, and then exposing
the port in the Ingress controller. For example, here a Redis service is exposed
via TCP:

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-ingress-tcp-microk8s-conf
  namespace: ingress
data:
  6379: "default/redis:6379"
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: nginx-ingress-microk8s-controller
  namespace: ingress
spec:
  template:
    spec:
      containers:
      - name: nginx-ingress-microk8s
        ports:
        - containerPort: 80
        - containerPort: 443
        - name: proxied-tcp-6379
          containerPort: 6379
          hostPort: 6379
          protocol: TCP
```
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-ingress.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
microk8s
