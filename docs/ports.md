---
layout: docs
title: "Services exposed - Authorization and authentication"
permalink: /docs/ports
---
# Services exposed and ports used

Services can be placed in two groups based on the network interface they bind to. Services binding to the `localhost`
interface are only available from within the host. Services binding to the
default host interface are available from outside the host and thus are subject to access restrictions.


### Services binding to the default Host interface

Port   | Service         | Access Restrictions
------ | --------------- | ---
16443  | API server      | SSL encrypted. Clients need to present a valid password from a [Static Password File](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authentication-strategies).
10250  | kubelet         | Anonymous authentication is disabled. [X509 client certificate](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet-authentication-authorization/) is required.
10255  | kubelet         | Read only port for the Kubelet.
25000  | cluster-agent   | Proper token required to authorise actions.
12379  | etcd            | SSL encrypted. Client certificates required to connect.
10257  | kube-controller | Serve HTTPS with authentication and authorization.
10259  | kube-scheduler  | Serve HTTPS with authentication and authorization.


### Services binding to the localhost interface

Port  | Service           | Description
------| ----------------- | -----------
10248 | kubelet           | Localhost healthz endpoint.
10249 | kube-proxy        | Port for the metrics server to serve on.
10251 | kube-schedule     | Port on which to serve HTTP insecurely.
10252 | kube-controller   | Port on which to serve HTTP insecurely.
10256 | kube-proxy        | Port to bind the health check server.
2380  | etcd              | Used for peer connections.
1338  | containerd        | Metrics port


### Containerd and etcd

Both these services are exposed through unix sockets.

Service     | Socket
----------- | ---
containerd  | unix:///var/snap/microk8s/common/run/containerd.sock


## Authentication and authorization

Upon deployment MicroK8s creates a CA, a signed server certificate and a service account key file. These files are stored under `/var/snap/microk8s/current/certs/`. Kubelet and the API server are aware of the same CA and so the signed server certificate is used by the API server to authenticate with kubelet (`--kubelet-client-certificate`). Clients talking to the secure port of the API server (`16443`) have to also be aware of the CA (`certificate-authority-data` in user kubeconfig).

The authentication [strategies](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authentication-strategies)
 enabled by default are:
 - Static Password File, with password tokens and usernames stored in `/var/snap/microk8s/current/credentials/basic_token.csv`
 - Static Token File with tokens in `/var/snap/microk8s/current/credentials/known_tokens.csv`, and
 - X509 Client Certs with the client CA file set to `/var/snap/microk8s/current/certs/ca.crt`.
 Under `/var/snap/microk8s/current/credentials/` you can find the `client.config` kubeconfig file
 used by `microk8s.kubectl`.

By default all authenticated requests are authorized as the api-server runs with
`--authorization-mode=AlwaysAllow`. Turning on [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) is done through `microk8s.enable rbac`.


## References

 - [Authentication strategies](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#authentication-strategies)
 - [Role-based access control (RBAC)](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
 - [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)
 - [kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
 - [kube-scheduler](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-scheduler/)
 - [kube-controller-manager](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/)
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/ports.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
