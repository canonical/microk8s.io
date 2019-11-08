---
layout: docs
title: "gpu addon"
permalink: /docs/addon-gpu
---

# GPU addon

This addon enables NVIDIA GPU support for MicroK8s.

```bash
microk8s.enable gpu
```

Note that this is obviously dependent on the host system having suitable
NVIDIA GPU hardware _and_ the relevant drivers.

With the GPU addon enabled, workloads can request the GPU using a limit
setting, `nvidia.com/gpu: 1 `. For example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vector-add
spec:
  restartPolicy: OnFailure
  containers:
    - name: cuda-vector-add
      image: "k8s.gcr.io/cuda-vector-add:v0.1"
      resources:
        limits:
          nvidia.com/gpu: 1
```
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addon-gpu.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
