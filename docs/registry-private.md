---
layout: docs
title: "Using a private registry"
permalink: /docs/registry-private
---

# Working with a private registry

Often organisations have their own private registry to assist collaboration and
accelerate development. Kubernetes (and thus MicroK8s) need to be aware of the
registry endpoints before being able to pull container images.

## Insecure registry

Let's assume the private insecure registry is at `10.141.241.175` on port
`32000`. The images we build need to be tagged with the registry endpoint:

```bash
docker build . -t 10.141.241.175:32000/mynginx:registry
```

Pushing  the `mynginx` image at this point will fail because the local Docker
does not trust the private insecure registry. The docker daemon used for
building images should be configured to trust the private insecure registry.
This is done by marking the registry endpoint in `/etc/docker/daemon.json`:

```json
{
  "insecure-registries" : ["10.141.241.175:32000"]
}
```

Restart the Docker daemon on the host to load the new configuration:

```
sudo systemctl restart docker
```

Now  running
```bash
docker push  10.141.241.175:32000/mynginx
```
...should succeed in uploading the image to the registry.

Attempting to pull an image in MicroK8s at this point will result in an error
like this:

```no-highlight
  Warning  Failed             1s (x2 over 16s)  kubelet, jackal-vgn-fz11m  Failed to pull image "10.141.241.175:32000/mynginx:registry": rpc error: code = Unknown desc = failed to resolve image "10.141.241.175:32000/mynginx:registry": no available registry endpoint: failed to do request: Head https://10.141.241.175:32000/v2/mynginx/manifests/registry: http: server gave HTTP response to HTTPS client
```

We need to edit `/var/snap/microk8s/current/args/containerd-template.toml` and
add the following under `[plugins] -> [plugins.cri.registry] ->
[plugins.cri.registry.mirrors]`:

```
        [plugins.cri.registry.mirrors."10.141.241.175:32000"]
          endpoint = ["http://10.141.241.175:32000"]
```

See the full file [here](containerd-template.toml).

Restart MicroK8s to have the new configuration loaded:

```bash
microk8s stop
```

Allow a few seconds for the service to close fully before starting again:

```bash
microk8s start
```

The image can now be deployed with:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: 10.141.241.175:32000/mynginx:registry
        ports:
        - containerPort: 80
```

Note that the image is referenced with `10.141.241.175:32000/mynginx:registry`.

## Secure registry

There are a lot of ways to setup a private secure registry that may slightly
change the way you interact with it. Instead of diving into the specifics of
each setup we provide here two pointers on how you can approach the integration
with Kubernetes.

-   In the [official Kubernetes documentation][kubernetes-docs] a method is
    described for creating a secret from the Docker login credentials and using
    this to access the secure registry. To achieve this, `imagePullSecrets` is
    used as part of the container spec.

-   MicroK8s v1.14 and onwards uses **containerd**. [As described
    here](https://github.com/containerd/cri/blob/master/docs/registry.md),
    users should be aware of the secure registry and the credentials needed to
    access it. As shown above, configuring containerd involves editing
    `/var/snap/microk8s/current/args/containerd-template.toml` and reloading
    the new configuration via a `microk8s stop`, `microk8s start` cycle.

<!-- LINKS -->

[kubernetes-docs]: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/registry-private.md" class="p-notification__action">edit this page</a> 
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
