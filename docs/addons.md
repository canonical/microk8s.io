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

**[knative](#knative)**: Adds the [Knative][knative-docs] middleware to your cluster.

**[linkerd](#linkerd)**: Deploys the linkerd service mesh. [See below](#linkerd) for configuration.

**[metrics-server](#metrics-server)**: Adds the Kubernetes Metrics Server for API access to service metrics.

**[prometheus](#prometheus)**: Deploys the [Prometheus Operator][prometheus-docs].

**[rbac](#rbac)**: Enable Role Based Access Control for authorisation. Note that this is incompatible with some other add-ons ([See notes](#rbac))

**[registry][]**: Deploy a private image registry and expose it on localhost:32000. The storage add-on will be enabled as part of this add-on. See the registry documentation for more details.

**[storage][]**: Create a default storage class which allocates storage from a host directory.


### dns

As noted above, this deploys CoreDNS to supply address resolution services to
Kubernetes. This service is commonly required by other addons, so it is
recommended that you enable it.

By default it points to Google's 8.8.8.8, 8.8.4.4 servers for resolving
addresses. This can be changed by running the command:

```bash
microk8s.kubectl -n kube-system edit configmap/coredns
```

This will invoke the `vim` editor so you can alter the configuration.

### dashboard

The standard Kubernetes Dashboard is a convenient way to keep track of the
activity and resource use of MicroK8s


To log in to the Dashboard, you will need the access token. This is generated
randomly on deployment, so a few commands are needed to retrieve it:

```bash
token=$(microk8s.kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s.kubectl -n kube-system describe secret $token
```

Next, you need a connection to the API server. While the MicroK8s snap will
have an IP address on your local network, the recommended way to do this is
through the proxy service. You can initiate the proxy with the command:

```bash
microk8s.kubectl proxy --accept-hosts=.* --address=0.0.0.0 &
```

You can then access the Dashboard at the address

[http://127.0.0.1:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/]()

![IMAGE of Dashboard](#ref)


### fluentd

Enabling this addon will add Elasticsearch, Fluentd and Kibana (the EFK stack)
to MicroK8s. The components will be installed and connected together.

To access the Kibana dashboard, you should first start the kube proxy service:

```bash
microk86.kubectl proxy
```

You will now find the dashboard available at:
<http://127.0.0.1:8001/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana>

Note that you will still need to set up Kibana to track whatever you are
interested in. For more details see the [upstrem docs on EFK][efk-upstream]
and the [official Kibana documentation][kibana-docs].

![IMAGE kibana](#ref)



### gpu

This addon enables GPU support for MicroK8s. Note that this is obviously dependent on the host system having suitable Nvidia GPU hardware and
relevant drivers.

With the GPU addon enabled, workloads can request the GPU using a limit setting, `nvidia.com/gpu: 1 `. For example:

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


### ingress

### istio

Deploying the [Istio][istio-woe] service mesh will add various traffic management, tuning and security features to MicroK8s.

If you enable this addon, there is a single question to answer during the install process:

```
Enforce mutual TLS authentication (https://bit.ly/2KB4j04) between sidecars? If unsure, choose N. (y/N):
```

Istio controls routing and security - if you plan to run services which are not looked after by istio (i.e. a mixed environment) then you should answer 'N' here.


You can confirm the istio services are running with:

```bash
microk8s.kubectl get all -n istio-system
```

Istio proxy injection may be done on a service by service basis, but if you are intending to run all services through istio, it is more convenient to label the namespace to add istio to all new services:

```bash
microk8s.kubectl label namespace default istio-injection=true
```

There is more information about working with istio in the [istio documentation][istio-docs].

### jaeger

### knative

### linkerd

### metrics-server

The metrics-server addon is a complete implementation of the Kubernetes metrics
server project. Enabling the metrics-server will provide API access to
continuously updated metrics for MicroK8s.

More details on the scope and planned functionality of the metrics-server can be found in its [design documentation][metrics-design-doc].

### prometheus

Prometheus is a popular way to monitor a Kubernetes system, and one which is
easy to integrate with MicroK8s. To use Grafana to view the collected data,
it is advisable to also enable the `dashboard` addon at the same time:

```bash
microk8s.enable dashboard prometheus
```

You can verify the Grafana dashboard is available by running:

```bash
microk8s.kubectl cluster-info
```

Now, run the proxy service

```
microk8s.kubectl proxy &
```
(You may wish to run the proxy in a different shell rather than as a background process).

You can now navigate to the Grafana dashboard at the address:
<http://127.0.0.1:8001/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy>


![IMAGE Grafana](#ref)



### rbac

When enabled, the kube-apiserver `authorization-mode` will be set to `RBAC`. Kubernetes will then automatically add all the default roles and rolebindings.

When disabled, the addon will retrun the `authorization-mode` to `AlwaysAllow`.

For more information on using RBAC and the roles and bindings, see the
[upstream Kubernetes documentation][kubernetes-rbac].

### registry

The registry shipped with MicroK8s is hosted within the Kubernetes cluster and
is exposed as a NodePort service on port 32000 of the localhost. Note that this
is an insecure registry and you may need to take extra steps to limit access to
it.

For more information on using this private registry, please see the
[Working with registries documentation](#ref)


### storage

This storage class makes use of the hostpath-provisioner pointing to a
directory on the host. Persistent volumes are created under
`${SNAP_COMMON}/default-storage`. On an Ubuntu system this is commonly
`/var/snap/microk8s/common/default-storage/`.

If this addon is subsequently disabled, you will be asked if you wish to
permanently remove any storage which may have been created.



<-! LINKS ->

[efk-upstream]: https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/
[istio-woe]: https://istio.io/docs/concepts/what-is-istio/
[istio-docs]: https://istio.io/docs/
[jaeger-docs]: https://github.com/jaegertracing/jaeger-operator
[linkerd-docs]: https://linkerd.io/2/overview/
[kibana-docs]: https://www.elastic.co/guide/en/kibana/current/discover.html
[metrics-design-doc]:https://github.com/kubernetes/community/blob/master/contributors/design-proposals/instrumentation/metrics-server.md
