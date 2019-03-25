---
layout: docs
title: "Private registry add-on"
---
# Private registry add-on

Having a private registry can significantly improve your productivity by reducing the time spent in uploading and downloading docker images. The registry shipped with MicroK8s is hosted within the kubernetes cluster and is exposed as a NodePort service on port `32000` of the `localhost`. Note that this is an insecure registry and you may need to take extra steps to limit access to it.


## Installation and usage

You can install the registry with:
```
microk8s.enable registry
```

As you can see in the applied [manifest](https://github.com/ubuntu/microk8s/blob/master/microk8s-resources/actions/registry.yaml) a `20Gi` persistent volume is claimed for storing images. To satisfy this claim the storage add-on is also enabled along with the registry.

The containerd daemon used by MicroK8s is [configured to trust](https://github.com/ubuntu/microk8s/blob/master/microk8s-resources/default-args/containerd-template.toml) this insecure registry. The easiest way to upload images to the registry is by using the Docker client:

```
docker pull busybox
docker tag busybox localhost:32000/my-busybox
docker push localhost:32000/my-busybox
```

To consume an image from the local registry we need to reference it in our YAML manifests:
```
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
  - name: busybox
    image: localhost:32000/my-busybox
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
  restartPolicy: Always
```


## References
 - Containerd registry: https://github.com/containerd/cri/blob/master/docs/registry.md
