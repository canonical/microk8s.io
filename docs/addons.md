# Addons

By default, MicroK8s installs the bare minimum of Kubernetes.  This means only
the api-server, controller-manager, scheduler, kubelet, cni and kube-proxy are
installed and run. This keeps the requirements as low as possible, but may
leave you lacking some functionality depending on your use-case.

To provide additional services and funcionality, Microk8s uses a system of
*addons* - extra components which may be useful for you.

These addons can be enabled and disabled at any time, and most are
pre-configured to 'just work' without any further set up.

For example, to enable the CoreDNS addon:

```bash
microk8s.enable dns
```

You can check which addons are currently enabled with the command:

```bash
microk8s.status
```

This also conveniently lists all the known addons, cutting down on trips to
these docs! The addons currently available are listed below, and explained in
more detail in the sections following.

**[dashboard][]**: The standard Kubernetes Dashboard.

**[dns][]**: Deploys CoreDNS. This add-on may be required by others - it is
recommended you always enable it. In restricted environments you may need to
update the upstream DNS servers ([see below][dns]).

**[fluentd][]**: Deploy the Elasticsearch-Fluentd-Kibana logging and monitoring
solution.

**[gpu][]**:  Enable support for GPU accelerated workloads using the nVidia runtime.

**[ingress][]**: A simple ingress controller for external access.

**[istio][]**: Adds the core [Istio][istio-docs] services.

**[jaeger][]**: Deploy the [Jaeger Operator][jaeger-docs] in the “simplest” configuration.

**[knative][]**: Adss the [Knative][knative-docs] middleware to your cluster.

**[linkerd][]**:Deploys the linkerd service mesh. [See below](#linkerd) for configuration.

**[metrics-server][]**: Adds the Kubernetes Metrics Server for API access to service metrics.

**[prometheus]()**: Deploys the [Prometheus Operator][prometheus-docs].

**[rbac]()**: Enable Role Based Access Control for authorisation. Note that this is incompatible with some other add-ons ([See notes](#rbac))

**[registry][]**: Deploy a private image registry and expose it on localhost:32000. The storage add-on will be enabled as part of this add-on. See the registry documentation for more details.

**[storage][]**: Create a default storage class which allocates storage from a host directory.


### dns

As noted above, this deploys CoreDNS to supply address resolution services to Kubernetes. This service is commonly required by other addons, so it is recommended that you enable it.

By default it points to Google's 8.8.8.8, 8.8.4.4 servers for resolving
addresses. This can be changed by running the command:

```bash
microk8s.kubectl -n kube-system edit configmap/coredns
```

This will invoke the `vim` editor so you can alter the configuration.

### dashboard

The standard Kubernetes Dashboard is a convenient way to keep track of the
activity and resource use of microk8s

### fluentd



### gpu

### ingress

### istio

### jaeger

### knative

### linkerd

### metrics-server

### prometheus

### rbac

### registry

### storage

This storage class makes use of the hostpath-provisioner pointing to a directory on the host. Persistent volumes are created under ${SNAP_COMMON}/default-storage. Upon disabling this add-on you will be asked if you want to delete the persistent volumes created.

[efk-upstream]: https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/
[istio-docs]: https://istio.io/docs/concepts/what-is-istio/
[jaeger-docs]: https://github.com/jaegertracing/jaeger-operator
[linkerd-docs]: https://linkerd.io/2/overview/
