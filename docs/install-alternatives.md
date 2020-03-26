---
layout: docs
title: "Alternative Install"
permalink: /docs/install-alternatives
---

# Alternative install methods

MicroK8s is spectacularly easy to install and use on Ubuntu or any Linux which
supports snaps. For other platforms or less common scenarios, see the relevant
notes below.

<a id="windows"> </a>
## Windows 10

From 1.18, MicroK8s now has an official Windows installer, which is the
recommended way to install MicroK8s

1.  **Download the installer**

    The Windows installer is available on the MicroK8s GitHub page.
    [Download it here](https://github.com/ubuntu/microk8s/releases/download/installer-v1.0.0/microk8s-installer.exe)

1.  **Run the installer**

    Once the installer is downloaded, run it to begin installation.

    You will be asked a few questions as usual when installing software. Some
    things to note:

    ![](https://assets.ubuntu.com/v1/141d9f8b-winmk8s-01.png)

    We recommend installing for 'All users'

    ![](https://assets.ubuntu.com/v1/c7d0a5a7-winmk8s-03.png)

    The installer also requires the Ubuntu VM system, [Multipass][], to be
    installed. This will be done automatically when you click 'Yes' here.

1.  **Open the command line:**

    Use PowerShell or the standard Windows 'cmd' to open a commandline.

    ![](https://assets.ubuntu.com/v1/a5fe14a5-winmk8s-04.png)

1.  **Check MicroK8s is running**

    Run the command:

    ```
    microk8s status --wait-ready
    ```

1.  **Explore what you can do!**

    Congrats! MicroK8s is now running on your Windows machine and is ready
    for you to explore and use Kubernetes. See the
    [main install](/docs/index#rejoin) page for your next steps!

<a id="macos"> </a>
## macOS

The recommended way to install MicroK8s on MacOS is with Homebrew

1.  **Install Homebrew**

    Open a terminal and run the installer:

    ```
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```

1.  **Install MicroK8s**

    Run the command:

    ```
    brew install ubuntu/microk8s/microk8s
    ```

    [![asciicast](https://asciinema.org/a/IWhwnidik9xaC2YHfjBUIsLin.svg)](https://asciinema.org/a/IWhwnidik9xaC2YHfjBUIsLin)

1.  **Wait for MicroK8s to start**

    ```
    microk8s status --wait-ready
    ```

1.  **Congrats!**

    MicroK8s is now running! Continue to explore by following the
    _Getting Started_ instructions [here](/docs/index#rejoin)


<a id="multipass"> </a>
## multipass

With multipass installed, you can now create a VM to run MicroK8s. At least 4
Gigabytes of RAM and 40G of storage is recommended -- we can pass these
requirements when we launch the VM:

```bash
multipass launch --name microk8s-vm --mem 4G --disk 40G
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

To work within the VM environment more easily, you can run a shell:

```bash
multipass shell microk8s-vm
```

Then install the  MicroK8s snap and configure the network:

```bash
sudo snap install microk8s --classic --channel=1.17/stable
sudo iptables -P FORWARD ACCEPT
```

From within the VM shell, you can now follow along the rest of the
[quick start instructions](index#status)

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

<a id="arm"> </a>
## Raspberry Pi/ARM

Running MicroK8s on some ARM hardware may run into difficulties because cgroups
(required!) are not enabled by default. This can be remedied on the Rasberry Pi
by editing the boot parameters:

```bash
sudo vi /boot/firmware/nobtcmd.txt
```

<div class="p-notification--positive"><p markdown="1" class="p-notification__response">
<span class="p-notification__status">Note:</span> In older Raspberry Pi versions
the boot parameters are in `/boot/firmware/cmdline.txt`.</p></div>

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
    microk8s stop
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
    microk8s start
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
