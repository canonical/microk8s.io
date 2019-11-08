---
layout: docs
title: "Quick start"
---

<h1 id="microk8s-documentation">MicroK8s quick start guide <img src="https://assets.ubuntu.com/v1/6731169e-certified-kubernetes-color.png?w=60" style="margin-left: 1rem; position: relative; top: -8px;" align="right"></h1>

The smallest, fastest, fully-conformant Kubernetes that tracks upstream
releases and makes clustering trivial. MicroK8s is great for offline
development, prototyping, and testing. Use it on a VM as a small, cheap,
reliable k8s for CI/CD. The best Kubernetes for appliances. Develop IoT apps
for k8s and deploy them to MicroK8s on your Linux boxes.


## What you'll need

- An Ubuntu 18.04 LTS or 16.04 LTS environment to run the commands (or another operating system which supports `snapd` - see the [snapd documentation][snapd-docs])
- At least 20G of disk space and 4G of memory are recommended
- An internet connection

<div class="p-notification--positive"><p markdown="1" class="p-notification__response">
<span class="p-notification__status">Note:</span> If you don't meet these requirements, there are additional ways of installing the <emphasis>MicroK8s</emphasis>, including additional OS support and an offline deploy. See the  <a href="/docs/install-alternatives">alternative install</a> page for details. </p></div>


<section class="p-strip--light is-bordered">
  <div class="u-fixed-width">
    <ol class="p-stepped-list--detailed">
      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title col-4"><span class="p-stepped-list__bullet">1</span>Install MicroK8s</h3>
        <div class="col-8 p-stepped-list__content" >
MicroK8s will install a minimal, lightweight Kubernetes you can run and use on practically any machine. It can be installed with a snap:
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="sudo snap install microk8s --classic --channel=1.16/stable" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
          <script id="asciicast-279765" src="https://asciinema.org/a/279765.js" async data-autoplay="true" data-rows="4"></script>
          <p>
          <a href="/docs/setting-snap-channel">More about setting the channel&nbsp;›</a>
          </p>
        </div>
      </li>

      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title"><span class="p-stepped-list__bullet">2</span>Check the status</h3>
        <div class="p-stepped-list__content">

MicroK8s has a built-in command to display its status. During installation you
can use the `--wait-ready` flag to wait for the Kubernetes services to initialise:
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.status --wait-ready" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
        </div>
      </li>

      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title"><span class="p-stepped-list__bullet">3</span>Access Kubernetes</h3>
        <div class="p-stepped-list__content">
<p>MicroK8s bundles its own version of <code>kubectl</code> for accessing Kubernetes. Use it to run
commands to monitor and control your Kubernetes. For example, to view your node:</p>
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.kubectl get nodes" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
<p>.. or to see the running services: </p>
<div class="p-code-copyable">
  <input class="p-code-copyable__input" value="microk8s.kubectl get services" readonly="readonly">
  <button class="p-code-copyable__action">Copy to clipboard</button>
</div>
        </div>

      </li>

      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title"><span class="p-stepped-list__bullet">4</span>Deploy an app</h3>
        <div class="p-stepped-list__content">
          <p>Of course, Kubernetes is meant for deploying apps and services. You can use
          the <code>kubectl</code> command to do that as with any Kuberenetes. Try
          installing a demo app:</p>
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.kubectl create deployment kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
          <p>It may take a minute or two to install, but you can check the status:</p>

          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.kubectl get pods" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
        </div>
      </li>

      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title"><span class="p-stepped-list__bullet">5</span>Use add-ons</h3>
        <div class="p-stepped-list__content">
          <p>
MicroK8s uses the minimum of components for a pure, lightweight Kubernetes. However, plenty of extra features are available with a few keystrokes using "add-ons" -- pre-packaged components that will provide extra capabilities for your Kubernetes, from simple DNS management to machine learning with Kubeflow!
</p>
<p>
To start it is recommended to add DNS management to facilitate communication between services. For applications which need storage, the 'storage' add-on provides directory space on the host. These are easy to set up:</p>
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.enable dns storage" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
          <p>
          <a href="/docs/addons">See the full list of addons&nbsp;›</a>
          </p>
        </div>

      </li>

      <li class="p-stepped-list__item">
        <h3 class="p-stepped-list__title"><span class="p-stepped-list__bullet">6</span>Starting and Stopping MicroK8s</h3>
        <div class="p-stepped-list__content">
          <p>MicroK8s will continue running until you decide to stop it. You can stop and start MicroK8s with these simple commands:</p>
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.stop" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
          <p>... will stop MicroK8s and its services. You can start again any time by running:</p>
          <div class="p-code-copyable">
            <input class="p-code-copyable__input" value="microk8s.start" readonly="readonly">
            <button class="p-code-copyable__action">Copy to clipboard</button>
          </div>
        </div>
      </li>
      </ol>
    </div>
  </section>


## Next steps

-   One node not enough? Try [setting up a MicroK8s cluster][cluster].
-   Want to experiment with alpha releases of Kubernetes? [See the documentation on setting channels][channels].
-   Need to fiddle with the Kubernetes configuration? [Find out how to configure the Kubernetes services][services].
-   Find out how to run MicroK8s on [Windows, macOS or a Raspberry Pi][alternative].
-   Having problems? Check out our [troubleshooting section][trouble].
-   Love MicroK8s? Want to contribute or suggest a feature? [Give us your feedback][feedback].


<!--LINKS-->

[cluster]: /docs/clustering
[channels]: /docs/setting-snap-channel
[services]: /docs/configuring-services
[alternative]: /docs/install-alternatives
[trouble]: /docs/troubleshooting
[feedback]: /docs/get-in-touch
[snapd-docs]: https://snapcraft.io/docs/installing-snapd

<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/index.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
