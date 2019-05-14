---
layout: docs
title: "Release channels and upgrades"
---
# Release channels and upgrades

Microk8s is a snap deploying Kubernetes. Upstream Kubernetes ships a new release about every three months, while old releases get periodic updates. At the time of this writing the latest release series is `v1.14` with `v1.14.1` being the latest release. On the `v1.13` series, `v1.13.6` is the latest release. It is important to remember that upstream Kubernetes is committed to maintain backwards compatibility only within a release series. That means that your Kubernetes will not break when you upgrade from `v1.14.x` to `v1.14.y` but may break if you upgrade from `v1.13.x` to `v1.14.z`.


## Choosing the right channel

When installing MicroK8s you can select your desired upstream Kubernetes series with the corresponding snap channel. All channels are shown with `snap info microk8s` and at the time of writing we have:

```
channels:
  stable:         v1.14.1         2019-04-18 (522) 214MB classic
  candidate:      v1.14.1         2019-04-15 (522) 214MB classic
  beta:           v1.14.1         2019-04-15 (522) 214MB classic
  edge:           v1.14.1         2019-05-10 (587) 217MB classic
  1.15/stable:    –
  1.15/candidate: –
  1.15/beta:      –
  1.15/edge:      v1.15.0-alpha.3 2019-05-08 (578) 215MB classic
  1.14/stable:    v1.14.1         2019-04-18 (521) 214MB classic
  1.14/candidate: v1.14.1         2019-04-15 (521) 214MB classic
  1.14/beta:      v1.14.1         2019-04-15 (521) 214MB classic
  1.14/edge:      v1.14.1         2019-05-11 (590) 217MB classic
  1.13/stable:    v1.13.5         2019-04-22 (526) 237MB classic
  1.13/candidate: v1.13.6         2019-05-09 (581) 237MB classic
  1.13/beta:      v1.13.6         2019-05-09 (581) 237MB classic
  1.13/edge:      v1.13.6         2019-05-08 (581) 237MB classic
  1.12/stable:    v1.12.8         2019-05-02 (547) 259MB classic
  1.12/candidate: v1.12.8         2019-05-01 (547) 259MB classic
  1.12/beta:      v1.12.8         2019-05-01 (547) 259MB classic
  1.12/edge:      v1.12.8         2019-04-24 (547) 259MB classic
  1.11/stable:    v1.11.10        2019-05-10 (557) 258MB classic
  1.11/candidate: v1.11.10        2019-05-02 (557) 258MB classic
  1.11/beta:      v1.11.10        2019-05-02 (557) 258MB classic
  1.11/edge:      v1.11.10        2019-05-01 (557) 258MB classic
  1.10/stable:    v1.10.13        2019-04-22 (546) 222MB classic
  1.10/candidate: v1.10.13        2019-04-22 (546) 222MB classic
  1.10/beta:      v1.10.13        2019-04-22 (546) 222MB classic
  1.10/edge:      v1.10.13        2019-04-22 (546) 222MB classic
```

To install MicroK8s and let it follow the `v1.14` release series you:

```
snap install microk8s --classic --channel=1.14/stable
```

If you omit the `--channel` argument MicroK8s will follow the latest stable upstream Kubernetes. This means that your deployment will eventually upgrade to a new release series. For example, at the time of writing you will get `v1.14.1` with:

```
snap install microk8s --classic
```

Since no `--channel` is specified such deployment will eventually upgrade to `v1.15.0`.


## Tracks with stable releases

The `*/stable` channels serve the latest stable upstream Kubernetes release of the respective release series. Upstream releases are propagated to the MicroK8s snap in about a week. This means your MicroK8s will upgrade to the latest upstream release in your selected channel roughly one week after the upstream release.

The `*/candidate` and `*/beta` channels get updated within hours of an upstream release. Getting a MicroK8s deployment pointing to `1.14/beta` is as simple as:

```
snap install microk8s --classic --channel=1.14/beta
```

The `*/edge` channels get updated on each MicroK8s patch or upstream Kubernetes patch release.

Keep in mind that edge and beta are snap constructs and do not relate to Kubernetes release names.


## Tracks with pre-stable releases

On tracks where no stable Kubernetes release is available, MicroK8s ships pre-stable releases under the following scheme. 

- The `*/edge` channel (eg `1.15/edge`) holds the alpha upstream releases. 
- The `*/beta` channel (eg `1.15/beta`) holds the beta upstream releases.
- The `*/candidate` channel (eg `1.15/candidate`) holds the release candidate of upstream releases.

Pre-stable releases will be available the same day they are released upstream. 

For example, assuming `v1.14` is the latest stable release, to test your work against the alpha `v1.15` release simply do:

```
sudo snap install microk8s --classic --channel=1.5/edge
```

Beware however that pre-stable releases may require you to configure the K8s services on your own.


## I am confused. Which channel is right for me?

The single question you need to focus on is what channel should be used below:

```
sudo snap install microk8s --classic --channel=<which_channel?>
```

Here is the channel you have to select based on your needs:

 - I want to always be on the latest stable Kubernetes.

   -- Use `--channel=latest`

 - I want to always be on the latest release in a specific upstream K8s release.

   -- Use `--channel=<release>/stable`, eg `--channel=1.14/stable`. 

 - I want to test-drive a pre-stable release.

   -- Use `--channel=<next_release>/edge` for alpha releases.

   -- Use `--channel=<next_release>/beta` for beta releases.

   -- Use `--channel=<next_release>/candidate` for candidate releases.

 - I am waiting for a bug fix on MicroK8s:

   -- Use `--channel=<release>/edge`.

 - I am waiting for a bug fix on upstream Kubernetes:

   -- Use `--channel=<release>/candidate`.
