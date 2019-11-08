---
layout: docs
title: "Troubleshooting"
permalink: /docs/troubleshooting
---
# Troubleshooting

It is important to recognise that things _can_ go wrong. But MicroK8s gives
you tools to help work out _what_ has gone wrong, as detailed below. Be sure to
check out the [common issues](#common-issues) section for help resolving the
most frequently encountered problems.  

### Checking logs

If a pod is not behaving as expected, the first port of call should be the
logs.

First determine the resource identifier for the pod:

```bash
microk8s.kubectl get pods
```
This will list the currently available pods, for example:

```no-highlight
NAME                                 READY   STATUS             RESTARTS   AGE
mk8s-redis-7647889b6d-vjwqm          1/1     Running            0          2m24s
```

You can then use `kubectl` to view the log. For example, for the simple redis
pod above:

```bash
microk8s.kubectl logs mk8s-redis-7647889b6d-vjwqm
```

### Examining the configuration

If the problem you are experiencing indicates a problem with the configuration
of the Kubernetes components themselves, it could be helpful to examine the
arguments used to run these components. These are available in the directory
`${SNAP_DATA}/args`, which on Ubuntu should point to `/var/snap/microk8s/current`.
Note that the `$SNAP_DATA` environment variable itself is only available to the
running snap. For more information on the snap environment, check the
[snap documentation][snap-docs].

<a id="inspect"> </a>
### Using the built-in inspection tool

MicroK8s ships with a script to compile a complete report on MicroK8s and the
system which it is running on. This is essential for bug reports, but is also
a useful way of confirming the system is (or isn't) working and collecting all
the relevant data in one place.

To run the inspection tool, enter the command (admin privilege is required
to collect all the data):

```bash
sudo microk8s.inspect
```

You should see output similar to the following:

```bash
Inspecting services
  Service snap.microk8s.daemon-cluster-agent is running
  Service snap.microk8s.daemon-flanneld is running
  Service snap.microk8s.daemon-containerd is running
  Service snap.microk8s.daemon-apiserver is running
  Service snap.microk8s.daemon-apiserver-kicker is running
  Service snap.microk8s.daemon-proxy is running
  Service snap.microk8s.daemon-kubelet is running
  Service snap.microk8s.daemon-scheduler is running
  Service snap.microk8s.daemon-controller-manager is running
  Service snap.microk8s.daemon-etcd is running
  Copy service arguments to the final report tarball
Inspecting AppArmor configuration
Gathering system information
  Copy processes list to the final report tarball
  Copy snap list to the final report tarball
  Copy VM name (or none) to the final report tarball
  Copy disk usage information to the final report tarball
  Copy memory usage information to the final report tarball
  Copy server uptime to the final report tarball
  Copy current linux distribution to the final report tarball
  Copy openSSL information to the final report tarball
  Copy network configuration to the final report tarball
Inspecting kubernetes cluster
  Inspect kubernetes cluster

Building the report tarball
  Report tarball is at /var/snap/microk8s/1031/inspection-report-20191104_153950.tar.gz
```

This confirms the services that are running, and the resultant report file
can be viewed to get a detailed look at every aspect of the system.


<a id="common-issues"> </a>
## Common issues (and their solutions!)

<details>
    <summary><strong>My dns and dashboard pods are CrashLooping...</strong></summary>
    <p>The cni network plugin used by MicroK8s creates a <code>cni0</code>
    interface (<code>cbr0</code> on pre v1.16 releases) when the first pod is
    created.</p>
    <p>If you have <code>ufw</code> enabled, you'll need to allow traffic on
    this interface:</p>
    <pre><code>sudo ufw allow in on cni0 && sudo ufw allow out on cni0</code></pre>
</details>

<details>
   <summary><strong>My pods can't reach the internet or each other (but my MicroK8s host machine can)...</strong></summary>

   <p>Make sure packets to/from the pod network interface can be forwarded
      to/from the default interface on the host via the <code class="highlighter-rouge">iptables</code> tool.
      Such changes can be made persistent by installing the <code class="highlighter-rouge">iptables-persistent</code> package:</p>

   <div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>   sudo iptables -P FORWARD ACCEPT
      sudo apt-get install iptables-persistent
   </code></pre></div></div>

   <p>or, if using <code class="highlighter-rouge">ufw</code>:</p>

   <div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>   sudo ufw default allow routed
   </code></pre></div></div>

   <p>The MicroK8s inspect command can be used to check the firewall configuration:</p>

   <div class="highlighter-rouge"><div class="highlight"><pre class="highlight"><code>   microk8s.inspect
   </code></pre></div></div>

   <p>A warning will be shown if the firewall is not forwarding traffic.</p>
</details>

<details>
   <summary><strong>My log collector is not collecting any logs...</strong></summary>

   <p>By default container logs are located in <code class="highlighter-rouge">/var/log/pods/{id}</code>. You have to mount this location in your log collector for that to work. Following is an example diff for <a href="https://raw.githubusercontent.com/fluent/fluent-bit-kubernetes-logging/master/output/elasticsearch/fluent-bit-ds.yaml">fluent-bit</a>:</p>

   <div class="language-diff highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gu">@@ -36,6 +36,9 @@
   </span>         - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
   <span class="gi">+        - name: varlibdockercontainers
   +          mountPath: /var/snap/microk8s/common/var/lib/containerd/
   +          readOnly: true
   </span>         - name: fluent-bit-config
              mountPath: /fluent-bit/etc/
          terminationGracePeriodSeconds: 10
   <span class="gu">@@ -45,7 +48,7 @@
   </span>           path: /var/log
          - name: varlibdockercontainers
            hostPath:
   <span class="gd">-          path: /var/lib/docker/containers
   </span><span class="gi">+          mountPath: /var/snap/microk8s/common/var/lib/containerd/
   </span>       - name: fluent-bit-config
            configMap:
              name: fluent-bit-config
   </code></pre></div></div>
</details>

<a id="report-bug"> </a>
## Reporting a bug

If you cannot solve your issue and believe the fault may lie in MicroK8s,
please [file an issue on the project repository][bugs].

To help us deal effectively with issues, it is incredibly useful to include
the report obtained from [`microk8s.inspect`](#inspect), as well as any
additional logs, and a summary of the issue.

<!--LINKS-->
[bugs]: https://github.com/ubuntu/microk8s/issues/
[snap-docs]: https://snapcraft.io/docs/environment-variables
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/troubleshooting.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
