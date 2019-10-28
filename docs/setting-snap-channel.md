---
layout: docs
title: "Selecting a snap channel"
permalink: /docs/setting-snap-channel
---

# Snap channel overview

Microk8s is a snap deploying Kubernetes. The MicroK8s snap closely follow upstream
Kubernetes, so understanding a bit about the Kubernetes release cycle is helpful
for more insight into MicroK8s releases.

Upstream Kubernetes ships a new release series (e.g. 1.16.x) approximately
every three months. Prior release series may get periodic bugfix releases: for
example, the latest 1.15 release is 1.15.5.

It is important to remember that upstream Kubernetes is committed to maintain
backwards compatibility **only within a release series**. That means that your
Kubernetes should not break when you upgrade from `v1.16.x` to `v1.16.y`, but
there is no such guarantee when upgrading from `v1.15.x` to `v1.16.x`.

## Choosing the right channel

When installing MicroK8s you can select your desired upstream Kubernetes series
by choosing the corresponding snap channel.

All the currently available channels are shown if you run `snap info microk8s`:

```
stable:         v1.16.2  2019-10-22 (993) 187MB classic
candidate:      v1.16.2  2019-10-22 (993) 187MB classic
beta:           v1.16.2  2019-10-22 (993) 187MB classic
edge:           v1.16.2  2019-10-23 (998) 187MB classic
1.16/stable:    v1.16.2  2019-10-22 (989) 187MB classic
1.16/candidate: v1.16.2  2019-10-22 (989) 187MB classic
1.16/beta:      v1.16.2  2019-10-22 (989) 187MB classic
1.16/edge:      v1.16.2  2019-10-23 (999) 187MB classic
1.15/stable:    v1.15.4  2019-09-30 (876) 171MB classic
1.15/candidate: v1.15.5  2019-10-22 (984) 171MB classic
1.15/beta:      v1.15.5  2019-10-22 (984) 171MB classic
1.15/edge:      v1.15.5  2019-10-16 (984) 171MB classic
1.14/stable:    v1.14.8  2019-10-24 (979) 217MB classic
1.14/candidate: v1.14.8  2019-10-16 (979) 217MB classic
1.14/beta:      v1.14.8  2019-10-16 (979) 217MB classic
1.14/edge:      v1.14.8  2019-10-22 (997) 217MB classic
1.13/stable:    v1.13.6  2019-06-06 (581) 237MB classic
1.13/candidate: v1.13.6  2019-05-09 (581) 237MB classic
1.13/beta:      v1.13.6  2019-05-09 (581) 237MB classic
1.13/edge:      v1.13.7  2019-06-06 (625) 244MB classic
1.12/stable:    v1.12.9  2019-06-06 (612) 259MB classic
1.12/candidate: v1.12.9  2019-06-04 (612) 259MB classic
1.12/beta:      v1.12.9  2019-06-04 (612) 259MB classic
1.12/edge:      v1.12.9  2019-05-28 (612) 259MB classic
1.11/stable:    v1.11.10 2019-05-10 (557) 258MB classic
1.11/candidate: v1.11.10 2019-05-02 (557) 258MB classic
1.11/beta:      v1.11.10 2019-05-02 (557) 258MB classic
1.11/edge:      v1.11.10 2019-05-01 (557) 258MB classic
1.10/stable:    v1.10.13 2019-04-22 (546) 222MB classic
1.10/candidate: v1.10.13 2019-04-22 (546) 222MB classic
1.10/beta:      v1.10.13 2019-04-22 (546) 222MB classic
1.10/edge:      v1.10.13 2019-04-22 (546) 222MB classic
installed:        v1.16.2             (993) 187MB classic
```

To install the latest stable version, simply run:

```bash
snap install microk8s --classic
```

In this case you will get periodic snap updates to the latest stable release.
Bear in mind that this could include a new Kubernetes series, and therefore is
not guaranteed to continue running. For anything more than an ephemeral
Kubernetes install, you are strongly advised to select a series.

For example, to install MicroK8s and let it follow the `v1.16` stable release
series you can run:

```
snap install microk8s --classic --channel=1.16/stable
```

In this case you will only receive updates for the 1.16 release of Kubernetes,
and MicroK8s will never upgrade to 1.17, unless you explicitly
[refresh the snap](#refresh)


## Stable, candidate, beta and edge releases

The `*/stable` channels serve the latest stable upstream Kubernetes release of
the respective release series. Upstream releases are propagated to the MicroK8s
snap in about a week. This means your MicroK8s will upgrade to the latest
upstream release in your selected channel roughly one week after the upstream
release.

The `*/candidate` and `*/beta` channels get updated within hours of an upstream
release. Getting a MicroK8s deployment pointing to `1.16/beta` is as simple as:

```
snap install microk8s --classic --channel=1.16/beta
```

The `*/edge` channels get updated on each MicroK8s patch or upstream
Kubernetes patch release.

Keep in mind that edge and beta are snap constructs and do not relate to
specific Kubernetes release names.


## Tracks with pre-stable releases

On tracks where no stable Kubernetes release is available, MicroK8s ships
pre-release versions under the following scheme:

-   The `*/edge` channel (eg `1.16/edge`) holds the alpha upstream releases. 
-   The `*/beta` channel (eg `1.16/beta`) holds the beta upstream releases.
-   The `*/candidate` channel (eg `1.16/candidate`) holds the release candidate
    of upstream releases.

Pre-release versions will be available the same day they are released upstream. 

For example, to test your work against the alpha `v1.16` release simply run:

```
sudo snap install microk8s --classic --channel=1.16/edge
```

However, be aware that pre-release versions may require you to configure the
Kubernetes services on your own.


## I am confused. Which channel is right for me?

The single question you need to focus on is what channel should be used below:

```
sudo snap install microk8s --classic --channel=<which_channel?>
```

Here are some suggestions for the channel to use based on your needs:

-   I want to always be on the latest stable Kubernetes.

     -- Use `--channel=latest`

-   I want to always be on the latest release in a specific upstream K8s release.

     -- Use `--channel=<release>/stable`, eg `--channel=1.14/stable`. 

-   I want to test-drive a pre-stable release.

     -- Use `--channel=<next_release>/edge` for alpha releases.

     -- Use `--channel=<next_release>/beta` for beta releases.

     -- Use `--channel=<next_release>/candidate` for candidate releases.

-   I am waiting for a bug fix on MicroK8s:

     -- Use `--channel=<release>/edge`.

-   I am waiting for a bug fix on upstream Kubernetes:

     -- Use `--channel=<release>/candidate`.


<a id="refresh"> </a>
## Changing channels

If you have installed MicroK8s already, and then decide you wish to change
to a particular channel, you can use the `snap refresh` command to switch to a
different channel. For example, to switch to the latest alpha release for
the 1.16 series:

```bash
sudo snap refresh microk8s --channel=1.16/edge
```

## Changing the refresh schedule

By default, snaps are set to check for updates and automatically refresh to the
latest version (for your selected channel) four times per day. There are some
scenarios however where it may be inconvenient or difficult to refresh the
current snap so often.

There are some controls available to set the ***global*** refresh schedule for
all snaps on the system. These are outlined in the
[Snap documentation][snap-docs].



<!-- LINKS -->
[snap-docs]: https://snapcraft.io/docs/system-options
