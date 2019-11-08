---
layout: docs
title: "Alternative Install"
permalink: /docs/install-alternatives
---

# Alternative install methods

MicroK8s is spectacularly easy to install and use on Ubuntu or any Linux which
supports snaps. For other platforms or less common scenarios, see the relevant
notes below.

## Windows 10

Although Windows 10 now has some very useful features, such as the ability to
install [Ubuntu as an app][ubuntu-app], the integration of WSL2 still
doesn't provide all the Ubuntu functionality required to make MicroK8s run
smoothly out-of-the-box.

If you wish to experiment with running MicroK8s semi-natively, take a look at
this [discourse post on WSL2][windows-post].

For now, the best way to run MicroK8s on Windows is with virtualisation.
MicroK8s will install without problems on Ubuntu running on number of different
VMs, including [VirtulBox](https://www.virtualbox.org/).

The recommended way to run MicroK8s in a VM on Windows 10 is to use
[multipass][]. The Windows installer is available for
[download here][multipass-install], and the notes for installing MicroK8s on
multipass [here](#multipass).

## macOS

As with Windows, the recommended way to run MicroK8s on macOS is to use
[multipass][], although it is possible to run under other VMs.

There is an installer for multipass available on the
[multipass site][multipass-install]. See the notes for running MicroK8s on
multipass below.


<a id="multipass"> </a>
## multipass

With multipass installed, you can now create a VM to run MicroK8s. At least 4
Gigabytes of RAM and 40G of storage is recommended -- we can pass these
requirements when we launch the VM:

```bash
multipass launch --name microk8s-vm --mem 4G --disk 40G
```

To install the MicroK8s snap and configure the network:

```bash
multipass exec microk8s-vm -- sudo snap install microk8s --classic
multipass exec microk8s-vm -- sudo iptables -P FORWARD ACCEPT
```

We can now find the IP address which has been allocated. Running:

```bash
multipass list
```

... will return something like:

```no-highlight
Name                    State             IPv4             Release
microk8s-vm             RUNNING           10.72.145.216    Ubuntu 18.04 LTS
```

Take a note of this IP as services will become available there when accessed
from the host machine.

#### Useful multipass commands

-   Get a shell inside the VM:

    ```bash
    multipass shell microk8s-vm
    ```

-   Shutdown the VM:

    ```bash
    multipass stop microk8s-vm
    ```

-   Delete and cleanup the VM:

    ```bash
    multipass delete microk8s-vm
    multipass purge
    ```

## Raspberry Pi/ARM

Running MicroK8s on some ARM hardware may run into difficulties because cgroups
(required!) are not enabled by default. This can be remedied on the Rasberry Pi
by editing the boot parameters:

```bash
sudo vi /boot/firmware/cmdline.txt
```

And adding the following:

```no-highlight
cgroup_enable=memory cgroup_memory=1
```

## Systems using ZFS

There is currently an issue surrounding using MicroK8s on a ZFS filesystem due
to the way containerd is configured. If you have installed MicroK8s on ZFS
you can fix this:

1.  Stop microk8s:

    ```
    microk8s.stop
    ```

1.  Remove old state of containerd:

    ```
    sudo rm -rf /var/snap/microk8s/common/var/lib/containerd
    ```

1.  Configure containerd to use ZFS:
    Edit  the file `/var/snap/microk8s/current/args/containerd-template.toml`
    replacing `snapshotter = "overlayfs"`  with `snapshotter = "zfs"`

1.  Create new zfs dataset for containerd to use:

    ```
    zfs create -o mountpoint=/var/snap/microk8s/common/var/lib/containerd/io.containerd.snapshotter.v1.zfs $POOL/containerd
    ```
1.  Restart microk8s:

    ```
    microk8s.start
    ```

## Offline deployment

There are situations where it is necessary or desirable to run MicroK8s on a
machine not connected to the internet. This is possible, but there are a few
extra things to be aware of.

#### Downloading a snap

If the machine you are intending to install MicroK8s to has no connectivity at
all, it is possible to download the snap from a machine which does have
access to the internet.

```bash
snap download microk8s
```

this will retrieve *two* files to the local directory:

-   microk8s_xxx.snap: The snap package with a versioned suffix.
-   microk8s_xxx.assert: The assertion file (effectively a signature validating the package).

When the files are transferred to the offline machine, MicroK8s can then be
installed with the following commands:

```bash
sudo snap ack microk8s_993.assert
sudo snap install microk8s_993.snap
```

In an offline environment, the snap will not be able to contact the store for
any updates.

#### Simulating a network

In some environments, as well as being offline, there is no network capability
at all (e.g. no NIC hardware). In such cases the Kubernetes apiserver will not
be able to work. This can be solved by simulating hardware (e.g. in a VM) or
adding a virtual address.

For an example, see this [answer on askubuntu][askubuntu].

<!-- LINKS -->

[ubuntu-app]: https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6
[windows-post]: https://discourse.ubuntu.com/t/using-snapd-in-wsl2/12113
[multipass]: https://multipass.run/
[multipass-install]: https://multipass.run/#install
[askubuntu]: https://askubuntu.com/questions/993139/how-to-create-a-virtual-network-interface-in-ubuntu
[profile]: https://github.com/ubuntu/microk8s/tree/master/tests/lxc
<!-- FEEDBACK -->
<div class="p-notification--information">
  <p class="p-notification__response">
    We appreciate your feedback on the docs. You can 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/install-alternatives.md" class="p-notification__action">edit this page</a> 
    or 
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
