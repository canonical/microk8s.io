---
layout: docs
title: "MicroK8s Addons"
permalink: /docs/addons
---

# MicroK8s Addons

To be as lightweight as possible, MicroK8s only installs the basics of a usable
Kubernetes install:

 - api-server
 - controller-manager
 - scheduler
 - kubelet
 - cni
 - kube-proxy

While this does deliver a pure Kubernetes experience with the smallest of
resource footprints, there are situations where you may require additional
services. MicroK8s caters for this with the concept of "Addons" - extra
services which can easily be added to MicroK8s. These addons can be enabled
and disabled at any time, and most are pre-configured to 'just work' without
any further set up.

For example, to enable the CoreDNS addon:

```bash
microk8s enable dns
```

These add-ons can be disabled at anytime using the `disable` command:

```bash
microk8s disable dns
```

... and you can check the list of available and installed addons at any time
by running:

```bash
microk8s status
```

<a id="list"> </a>
## Current MicroK8s Addons

[**dashboard**](addon-dashboard): The standard Kubernetes Dashboard.

[**dns**](addon-dns): Deploys CoreDNS. This add-on may be required by others - it is
recommended you always enable it. In restricted environments you may need to
update the upstream DNS servers.

**cilium**: Deploys [Cilium][cilium-doc] to support Kubernetes network policies using eBPF.

**[fluentd](addon-fluentd)**: Deploy the [Elasticsearch-Fluentd-Kibana][kibana-docs] logging and
monitoring solution.

[**gpu**](addon-gpu):  Enable support for GPU accelerated workloads using the NVIDIA runtime.

**helm**:  Enable [Helm 2](https://v2.helm.sh/docs/) package manager for Kubernates.

**helm3**:  Enable package manager [Helm 3](https://v3.helm.sh/docs/).

**ingress**: A simple ingress controller for external access.

**istio**: Adds the core [Istio][istio-docs] services.

**jaeger**: Deploy the [Jaeger Operator][jaeger-docs] in the “simplest”
configuration.

**juju**: Enables a [juju][] client to work with MicroK8s.

**knative**: Adds the [Knative][knative-docs] middleware to your cluster.

**kubeflow**: Adds [KubeFlow][] using the [kubeflow juju bundle][kubeflow-bundle].

**[linkerd](/docs/addon-linkerd)**: Deploys the [linkerd][linkerd-docs] service mesh.

**metrics-server**: Adds the [Kubernetes Metrics Server][metrics-design-doc]
for API access to service metrics.

**prometheus**: Deploys the [Prometheus Operator][prometheus-docs].

**rbac**: Enable Role Based Access Control for authorisation. Note that this is
incompatible with some other add-ons.

**registry**: Deploy a private image registry and expose it on localhost:32000.
The storage add-on will be enabled as part of this add-on. See the registry
documentation for more details.

**storage**: Create a default storage class which allocates storage from a
host directory.

**metallb**: Deploys the [MetalLB Loadbalancer][metallb].  Note that currently this does not
work under multipass on macOS, due to filtering that macOS applies to network traffic.


<!-- LINKS -->

[cilium-doc]: http://docs.cilium.io/en/stable/intro/
[efk-upstream]: https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/
[Helm 2]: https://helm.sh
[istio-woe]: https://istio.io/docs/concepts/what-is-istio/
[istio-docs]: https://istio.io/docs/
[jaeger-docs]: https://github.com/jaegertracing/jaeger-operator
[juju]: https://jaas.ai/docs/what-is-juju
[linkerd-docs]: https://linkerd.io/2/overview/
[kibana-docs]: https://www.elastic.co/guide/en/kibana/current/discover.html
[KubeFlow]: https://www.kubeflow.org/
[kubeflow-bundle]: https://github.com/juju-solutions/bundle-kubeflow/blob/master/README.md
[metrics-design-doc]:https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/metrics-server.md
[knative-docs]: https://knative.dev/
[prometheus-docs]: https://prometheus.io/docs/
[metallb]: https://metallb.universe.tf/

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/addons.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
