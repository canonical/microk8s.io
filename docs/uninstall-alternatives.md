---
layout: docs
title: "Alternative Uninstall"
permalink: /docs/uninstall-alternatives
---

# Alternative uninstall methods

## Windows 10

Uninstall MicroK8s via [Apps & features](https://support.microsoft.com/en-us/help/4028054/windows-10-repair-or-remove-programs).  When uninstalling MicroK8s, the VM will also be removed but Multipass will not.  This can also be removed from [Apps & features](https://support.microsoft.com/en-us/help/4028054/windows-10-repair-or-remove-programs).

## MacOS

Uninstall MicroK8s with the following command:

```bash
brew remove microk8s
```

This will *not* remove the VM.  To also remove the VM:

```bash
multipass delete -p MicroK8sVM
```

If you'd also like to remove Multipass:

```bash
multipass cask zap multipass
```

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
    <a href="https://github.com/canonical-web-and-design/microk8s.io/edit/master/docs/uninstall-alternatives.md" class="p-notification__action">edit this page</a>
    or
    <a href="https://github.com/canonical-web-and-design/microk8s.io/issues/new" class="p-notification__action">file a bug here</a>.
  </p>
</div>
