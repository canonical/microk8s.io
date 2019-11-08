---
layout: docs
title: "Using a public registry"
permalink: /docs/registry-public
---

# Working with a public registry

After building an image we can push it to one of the mainstream public
registries. For this example we have created an account with
https://hub.docker.com/ with the username `kjackal`.

First we run the login command:

```bash
docker login
```

Docker will ask for a Docker ID and password to complete the login.

``` no-highlight
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: kjackal
Password: *******
```

Pushing to the registry requires that the image is tagged with
`your-hub-username/image-name:tag`. We can either add proper tagging during build:

```bash
docker build . -t kjackal/mynginx:public
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
docker tag 1fe3d8f47868 kjackal/mynginx:public
```

Now that the image is tagged correctly, it can be pushed to the registry:

```bash
docker push kjackal/mynginx
```

At this point we are ready to `microk8s.kubectl apply -f` a deployment with our
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
        image: kjackal/mynginx:public
        ports:
        - containerPort: 80
```

We refer to the image as `image: kjackal/mynginx:public`. Kubernetes will
search for the image in its default registry, `docker.io`.
