---
layout: docs
title: "Release notes"
permalink: /docs/release-notes
---

# Release notes

## Microk8s 1.16 - 26 September 2019

**MicroK8s** is a Kubernetes<sup>&reg;</sup> cluster delivered as a single snap
package - it can be installed on any Linux distribution which supports
[snaps][]. MicroK8s is small and simple to install and is a great way to stand
up a cluster quickly for development and testing. Try it on your laptop!

```bash
snap install microk8s --classic --channel=1.16/stable
```

Most important updates since the last release:

-   Clustering - MicroK8s nodes can be joined to create a multi-node cluster,
    see [these docs](clustering) if you want to try it.
-   New **Cilium** addon courtesy of [@joestringer][]. Try it with `microk8s.enable cilium`.
-   New **Helm** addon courtesy of [@joestringer][]. Try it with `microk8s.enable helm`.
-   **RBAC** rules for **CoreDNS** and storage add ons, courtesy of [@wichert][].
-   **Istio** upgraded to v1.2.2 and now includes kiali.
-   **Knative** upgraded to v0.9.0.
-   Enabling of aggregation layer and fix on metrics server **RBAC** rules,
    thank you [@giner][].
-   **microk8s.reset** has now an option to free the disk space reserved by
    storage volumes. Thank you [@rzr][].
-   **Ingress** updated to v0.25.1, thank you [@balchua][].
-   Improvements in the inspection script, thanks [@giorgos-apo][].
-   **Dashboard** upgraded to 2.0.0 beta4.

For more information on MicroK8s consult the official [docs][], and to
contribute to the project, check out the repo at
[https://github.com/ubuntu/microk8s][repo], or chat with us on the [Kubernetes
Slack][slack], in the #microk8s channel!

## Microk8s 1.15 - 21 June 2019

### Changelog

-   **RBAC** support via a simple `microk8s.enable rbac`, courtesy of [@magne][].
-   Update of the **Dashboard** to 1.10.1 and fixes for RBAC. Thank you [@balchua][].
-   **Knative** addon, try it with `microk8s.enable knative`. Thank you [@olatheander][] for your contribution.
-   **CoreDNS** is now the default. Thanks [@richardcase][] for driving this.
-   **Ingress** updated to 0.24.1 by [@JorritSalverda][], thank you.
-   Fix on socat failing on Fedora by [@JimPatterson][], thanks.
-   Modifiable CSR server certificate, courtesy of [@balchua][].
-   Use of iptables kubeproxy mode by default.
-   User guide moved out of GitHub to microk8s.io .
-   Instructions on how to run **Cilium** on MicroK8s by [@joestringer][].


## MicroK8s 1.14 - 25 March 2019

#### Changelog

-   **Containerd** replaced dockerd. Thanks to [@waquidvp][] for keeping up
    with the containerd and runc updates.
-   The **Ingress** controller got updated to v0.22.0 (thanks to [@khteh][]) and is now using:
    -   the correct ConfigMap (thanks [@keshavdv][]).
    -   the ClusterFirstWithHostNet dnsPolicy (thanks [@klarose][]).
    -   the right targetport (thanks [@davefinster][]).
-   **Istio** addon now deploys Istio v1.0.5.
-   `microk8s.reset` now deletes CRDs. Thank you [@miguelgarcia][].
-   Improved security of exposed ports and services.
-   Three new addons are available since the last release anouncement:
    -   **Jaeger**, available with: `microk8s.enable jaeger`.
    -   **Fluentd**, try it with: `microk8s.enable fluentd`.
    -   **Prometheus**, enable it with: `microk8s.enable prometheus`.
-   Installation on Arch Linux now correctly detects the machine architecture.
-   kubectl now uses a secure kubeconfig found in a configurable location.


## MicroK8s 1.13 - 14 February 2019

#### Changelog

-   New website! Check it out at [https://microk8s.io](https://microk8s.io).
-   **ARM64 support!**
-   `microk8s.start` and `microk8s.stop` commands allow you to easily enable and disable MicroK8s.
-   `microk8s.status` gives you an overview of the current status.
-   We now detect host IP changes. You can now use MicroK8s on your laptop without the need to restart it whenever you switch networks.
-   MicroK8s is now a **CNCF certified Kubernetes**. Certification was for v1.12; v1.13 will follow shortly.
-   Enable **digitalSignature key** usage for CA (thanks [@lhotari][]).
-   Pod eviction limit due to memory shortage decreased to 100MB.


## MicroK8s 1.12 - 13 November 2018

#### Changelog

-   Stable releases of 1.10, 1.11, 1.12.
-   Private **registry** addon (`microk8s.enable registry`).
-   **GPU** addon (`microk8s.enable gpu`).
-   **Istio** v1.0.0 addon (`microk8s.enable istio`).
-   **Metrics server** (`microk8s.enable metrics-server`).
-   Inspect command for deployment troubleshooting (`microk8s.inspect`).
-   **CNI** updated to v0.7.1.
-   Bug fix: Ship socat in the snap.
-   Bug fix: Metrics for pods are now available in the grafana dashboard addon.
-   Bug fix: ZFS utilities are now shipped with the snap.
-   Bug fix: microk8s.reset will now remove all resources.

## MicroK8s 1.11 - 10 July 2018

#### Changelog

-   New **ingress controller** addon - `microk8s.enable ingress` - creates an ingress controller.
-   New **storage** addon - `microk8s.enable storage` - creates a default storage class using hostpath-provisioner and a directory on the host.
-   New command: `microk8s.reset` - stops all running pods, deployments, services, and daemons.
-   New command: `microk8s.config` - outputs the config used by `microk8s.kubectl`.
-   Bug fix: Clean up snap removal.
-   Bug fix: Add Ubuntu Trusty (14.04) support.

<!-- LINKS -->

[docs]: https://microk8s.io/docs/
[snaps]: https://snapcraft.io/
[slack]: http://slack.kubernetes.io/
[repo]: https://github.com/ubuntu/microk8s

<!-- people -->

[@balchua]: https://github.com/balchua
[@davefinster]: https://github.com/davefinster
[@giner]: https://github.com/giner
[@giorgos-apo]: https://github.com/giorgos-apo
[@JimPatterson]: https://github.com/JimPatterson
[@joestringer]: https://github.com/joestringer
[@JorritSalverda]: https://github.com/JorritSalverda
[@keshavdv]: https://github.com/keshavdv
[@khteh]: https://github.com/khteh
[@klarose]: https://github.com/klarose
[@lhotari]: https://github.com/lhotari
[@magne]: https://github.com/magne
[@miguelgarcia]: https://github.com/miguelgarcia
[@olatheander]: https://github.com/olatheander
[@richardcase]: https://github.com/richardcase
[@rzr]: https://github.com/rzr
[@waquidvp]: https://github.com/waquidvp
[@wichert]: https://github.com/wichert
