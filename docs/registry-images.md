---
layout: docs
title: "Using images"
permalink: /docs/registry-images
---

# MicroK8s images

Kubernetes manages containerised applications based on images. These images can
be created locally, or more commonly are fetched from a remote image registry.
The following documentation explains how to use MicroK8s with local images, or
images fetched from public or private registries.

A familiarity with building, pushing and tagging container images will be
helpful. These examples use Docker but you can use your preferred
container tool chain.

To install Docker on Ubuntu 18.04:

```
sudo apt-get install docker.io
```

Add the user to the `docker` group:

```bash
sudo usermod -aG docker ${USER}
```

Open a new shell for the user, with updated group membership:

```bash
su - ${USER}
```

The Dockerfile we will be using is:

```
FROM nginx
```

To build the image tagged with `mynginx:local`, navigate to the directory where
`Dockerfile` is and run:

```bash
docker build . -t mynginx:local
```

This will generate a new local image tagged `mynginx:local`.

## Working with locally built images without a registry

When an image is built it is cached on the Docker daemon used during the build.
Having run the `docker build . -t mynginx:local` command, you can see the newly
built image by running:

```bash
docker images
```

This will list the images currently known to Docker, for example:

```no-highlight
REPOSITORY          TAG                 IMAGE ID            SIZE
mynginx             local               1fe3d8f47868        16.1MB
```

The image we created is known to Docker. However, Kubernetes is not aware of
the newly built image. This is because your local  Docker daemon is not part of
the MicroK8s Kubernetes cluster. We can export the built image from the local
Docker daemon and "inject" it into the  MicroK8s image cache like this:

```bash
docker save mynginx > myimage.tar
microk8s.ctr -n k8s.io image import myimage.tar
```

Note that when we import the image to MicroK8s we do so under the `k8s.io`
namespace (the `-n k8s.io` argument).

Now we can list the images present in MicroK8s:

```bash
microk8s.ctr -n k8s.io images ls
```

At this point we are ready to `microk8s.kubectl apply -f` a deployment with
this image:

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
        image: mynginx:local
        imagePullPolicy: Never
        ports:
        - containerPort: 80
```

We reference the image with `image: mynginx:local`. Kubernetes will behave as
though there is an image in docker.io (the Dockerhub registry) for which it
already has a cached copy. This process can be repeated any time changes are
made to the image. Note that containerd will not cache images with the `latest`
tag so make sure you avoid it.
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/registry-images.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
