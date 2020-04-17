---
layout: docs
title: "Using the built-in private registry"
permalink: /docs/registry-built-in
---

# Working with MicroK8s' built-in registry

Having a private Docker registry can significantly improve your productivity by
reducing the time spent in uploading and downloading Docker images. The
registry shipped with MicroK8s is hosted within the Kubernetes cluster and is
exposed as a NodePort service on port `32000` of the `localhost`. Note that
this is an insecure registry and you may need to take extra steps to limit
access to it.

You can install the registry with:

```bash
microk8s enable registry
```

The add-on registry is backed up by a `20Gi` persistent volume is claimed for
storing images. To satisfy this claim the storage add-on is also enabled along
with the registry.

The containerd daemon used by MicroK8s is configured to trust this insecure
registry. To upload images we have to tag them with
`localhost:32000/your-image` before pushing them:

We can either add proper tagging during build:

```bash
docker build . -t localhost:32000/mynginx:registry
```

Or tag an already existing image using the image ID. Obtain the ID by running:

```bash
docker images
```

The ID is listed in the output:

```no-highlight
REPOSITORY          TAG                 IMAGE ID            SIZE
mynginx             local               1fe3d8f47868        16.1MB
....
```

Then use the `tag` command:

```bash
docker tag 1fe3d8f47868 localhost:32000/mynginx:registry
```

Now that the image is tagged correctly, it can be pushed to the registry:

```bash
docker push localhost:32000/mynginx
```

Pushing to this insecure registry may fail in some versions of Docker unless
the daemon is explicitly configured to trust this registry. To address this we
need to edit `/etc/docker/daemon.json` and add:

```json
{
  "insecure-registries" : ["localhost:32000"]
}
```

The new configuration should be loaded with a Docker daemon restart:

```bash
sudo systemctl restart docker
```

At this point we are ready to `microk8s kubectl apply -f` a deployment with our
image:

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
        image: localhost:32000/mynginx:registry
        ports:
        - containerPort: 80
```

## What if MicroK8s runs inside a VM?

Often MicroK8s is placed in a VM while the development process takes place on
the host machine. In this setup pushing container images to the in-VM registry
requires some extra configuration.

Let's assume the IP of the VM running MicroK8s is `10.141.241.175`. When we are
on the host the Docker registry is not on `localhost:32000` but on
`10.141.241.175:32000`. As a result the first thing we need to do is to tag the
image we are building on the host with the right registry endpoint:

```bash
docker build . -t 10.141.241.175:32000/mynginx:registry
```

If we immediately try to push the `mynginx` image we will fail because the
local Docker does not trust the in-VM registry. Here is what happens if we try
a push:

```bash
docker push  10.141.241.175:32000/mynginx
```
```no-highlight
The push refers to repository [10.141.241.175:32000/mynginx]
Get https://10.141.241.175:32000/v2/: http: server gave HTTP response to HTTPS client
```

We need to be explicit and configure the Docker daemon running on the host to
trust the in-VM insecure registry. Add the registry endpoint in
`/etc/docker/daemon.json`:

```json
{
  "insecure-registries" : ["10.141.241.175:32000"]
}
```

Then restart the docker daemon on the host to load the new configuration:

```bash
sudo systemctl restart docker
```

We can now `docker push  10.141.241.175:32000/mynginx` and see the image
getting uploaded. During the push our Docker client instructs the in-host
Docker daemon to upload the newly built image to the `10.141.241.175:32000`
endpoint as marked by the tag on the image. The Docker daemon sees (on
`/etc/docker/daemon.json`) that it trusts the registry and proceeds with
uploading the image.

Consuming the image from inside the VM involves no changes:

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
        image: localhost:32000/mynginx:registry
        ports:
        - containerPort: 80
```

Reference the image with `localhost:32000/mynginx:registry` since the registry
runs inside the VM so it is on `localhost:32000`.

## Using the local registry from another node in a microk8s cluster

If you have joined up other machines into a cluster with the machine that has the registry, you need to change the configuration files to point to the IP of the master node:
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
        image: <IP of the master node>:32000/mynginx:registry
        ports:
        - containerPort: 80
```

And you need to manually edit the containerd TOML on the worker machines, per [the private registry instructions](https://microk8s.io/docs/registry-private) to trust the insecure registry.

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/registry-built-in.md" class="p-notification__action">edit this page</a> 
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
