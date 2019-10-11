---
layout: docs
title: "Fluentd addon"
permalink: /docs/addon-fluentd
---

# Fluentd addon

Enabling this addon will add Elasticsearch, Fluentd and Kibana (the EFK stack)
to MicroK8s. The components will be installed and connected together.

To enable the addon:

```bash
microk8s enable fluentd
```

To access the Kibana dashboard, you should first start the kube proxy service:

```bash
microk86.kubectl proxy
```

You will now find the dashboard available at:
<http://127.0.0.1:8001/api/v1/namespaces/kube-system/services/kibana-logging/proxy/app/kibana>

Note that you will still need to set up Kibana to track whatever you are
interested in. For more details see the [upstream docs on EFK][efk-upstream]
and the [official Kibana documentation][kibana-docs].

The addon can be disabled at any time with the command:

```bash
microk8s.disable fluentd
```


<!-- LINKS -->
[efk-upstream]: https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/
[kibana-docs]: https://www.elastic.co/guide/en/kibana/current/discover.html
