# Module 0 · Session 1 — Tooling Reference

## The Virtual Lab: VirtualBox, the Course Machines, and SSH

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session used each of these tools for exactly one job.
> **This is the fuller treatment**, so that when you need one of them for something the session did not cover, you are reading a reference rather than searching.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Every command below is one you run on your own lab machines.

---

# VirtualBox

## The GUI and the command line do the same things

Everything in the VirtualBox Manager is also available from `VBoxManage`, which ships with VirtualBox and is on your `PATH` after installation.
The GUI is quicker to learn.
The command line is the one you can script, paste into a guide, and check the output of, which is why this course shows both.

```bash
VBoxManage --version           # which VirtualBox you are actually running
VBoxManage list vms            # every machine registered, with its UUID
VBoxManage list runningvms     # just the ones powered on
VBoxManage list natnets        # the NAT Networks, their prefixes and DHCP state
VBoxManage list hostonlyifs    # host-only adapters, if you ever use one
```

## Networks

```bash
# create the lab network
VBoxManage natnetwork add --netname CyberLab --network "10.0.2.0/24" --enable --dhcp on

# change one later
VBoxManage natnetwork modify --netname CyberLab --dhcp off

# remove one
VBoxManage natnetwork remove --netname CyberLab
```

**Port forwarding** is how something outside reaches a machine on a NAT Network deliberately.
It is the exception that proves the rule: inbound traffic is dropped **unless you open a specific door**.

```bash
VBoxManage natnetwork modify --netname CyberLab \
  --port-forward-4 "ssh-to-ubuntu:tcp:[]:2222:[10.0.2.6]:22"
```

That reads as: *name this rule `ssh-to-ubuntu`, and send TCP arriving on host port 2222 to 10.0.2.6 port 22.*
You will not need it in this session.
You will need it the first time you want to reach a lab machine from the host itself.

Remove it by name:

```bash
VBoxManage natnetwork modify --netname CyberLab --port-forward-4 delete ssh-to-ubuntu
```

> [!warning] The listing will not show you the rule
> `VBoxManage list natnets` prints the name, prefix, gateway and DHCP state and **says nothing about port forwarding**, so the command that adds a rule succeeds silently and the command you would check it with does not mention it.
> To see the rules, open **Tools**, then **Network**, then the **NAT Networks** tab, select the network, and look at **Port Forwarding**.
> (Verified on VirtualBox 7.0.16.)

## Machines

```bash
VBoxManage startvm "Ubuntu" --type headless   # boot with no window at all
VBoxManage controlvm "Ubuntu" acpipowerbutton # ask it to shut down cleanly
VBoxManage controlvm "Ubuntu" poweroff        # pull the plug, for when it is stuck
VBoxManage modifyvm "Ubuntu" --memory 2048    # RAM in MB, machine must be off
VBoxManage modifyvm "Ubuntu" --cpus 2
VBoxManage modifyvm "Ubuntu" --nic1 natnetwork --nat-network1 CyberLab
VBoxManage showvminfo "Ubuntu"                # every setting, more than you want
```

**`--type headless` is worth knowing early.**
The Ubuntu machine has no desktop, so its window shows a text console you are not going to use.
Started headless it takes no screen space at all, and you reach it over SSH exactly as before.

## Snapshots

```bash
VBoxManage snapshot "Ubuntu" take "clean install" --description "first working state"
VBoxManage snapshot "Ubuntu" list
VBoxManage snapshot "Ubuntu" restore "clean install"
VBoxManage snapshot "Ubuntu" delete "clean install"
```

**Deleting a snapshot does not roll anything back.**
It merges that point into the disk and frees the space it was holding.
Restoring is what rolls back.
These two get confused, and one of them is destructive in a way the other is not.

> [!warning] Restore is whole-machine
> `restore` puts the disk back to the snapshot.
> Everything written since is gone, not just the thing you regret.
> Copy off anything you want to keep first.

## The network modes, beyond the one this course uses

| Mode | Machines see each other | Machine reaches host | Host reaches machine | Reaches internet | Internet reaches it |
| --- | --- | --- | --- | --- | --- |
| **Internal Network** | yes | no | no | no | no |
| **Host-only** | yes | yes | yes | no | no |
| **NAT** | **no** | yes | port forward | yes | port forward |
| **NAT Network** | yes | yes | port forward | yes | port forward |
| **Bridged** | yes | yes | yes | yes | yes, it is a peer of your real network |

**The one cell that decides this course is NAT's first one.**
NAT and NAT Network are identical everywhere else on this table, and they differ on whether the machines can see each other, which is the only thing the lab actually requires.

**Internal Network** is the right answer for something you must not let out under any circumstances.
**Host-only** is for a machine that only ever talks to your own computer.
**Bridged** puts the machine on your real network as though it were another computer plugged into it, which is occasionally what you want and is almost never what you want in a security lab.

**If you already run VMware Workstation**, its modes map onto these with one difference that matters.
LAN Segment behaves like Internal Network, Host-only (`VMnet1`) like Host-only, and Bridged (`VMnet0`) like Bridged.
VMware's NAT (`VMnet8`) is not VirtualBox's NAT: it is one private network shared by every machine attached to it, and your host sits on that network through its own virtual adapter.
So on VMware, plain NAT already lets the machines see each other, and the host reaches them directly with no port forward.
The internet still reaches them only through a port forward.
(Source: Broadcom, [Workstation Pro 17: Configuring Network Address Translation](https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-pro/configuring-network-connections/configuring-network-address-translation-1.html).)

---

# 7-Zip

The Kali image arrives as a `.7z`, which most systems do not open natively.

```bash
7z x kali-linux-*-virtualbox-amd64.7z      # extract, keeping the folder structure
7z l kali-linux-*-virtualbox-amd64.7z      # list what is inside without extracting
```

**`x` rather than `e`.**
`e` flattens everything into one directory, which separates the `.vbox` file from the disk it points at.
Use `x`.

On Windows, 7-Zip's GUI does the same thing.
On macOS, Keka or The Unarchiver.

---

# Reading a machine's network state

## `ip`, on Linux

```bash
ip a                  # every interface and its addresses, the one you will use most
ip -4 a               # IPv4 only, much shorter
ip a show eth0        # one interface
ip r                  # the routing table, including the default gateway
ip -br a              # one short line per interface, easy to read at a glance
```

`ip a | grep 10.0.2` is the quick form used in the session.
`ip -br a` is the better habit, because it shows you every interface at once rather than only the one you guessed.

> [!note] `ifconfig` is the old one
> You will see `ifconfig` in older material.
> It is deprecated and is not installed by default on modern systems.
> `ip` replaced it, and everything `ifconfig` did, `ip` does.

## `ipconfig`, on Windows

```
ipconfig              # addresses per adapter
ipconfig /all         # adds the MAC address, DHCP server, and lease times
ipconfig /release     # give up the current DHCP lease
ipconfig /renew       # ask for a new one
```

**`/release` then `/renew` is the first thing to try** when a Windows machine has no address or has an address on the wrong network after you changed its adapter.

---

# `ping`

```bash
ping -c 4 10.0.2.6         # Linux: stop after 4
ping -n 4 10.0.2.6         # Windows: the same thing, different flag
ping -c 1 -W 1 10.0.2.6    # Linux: one try, give up after one second
```

**What a reply proves:** the two machines share a network and the path between them works in both directions.
**What no reply proves: much less than people assume.**
It could be a routing problem, or a machine that is off, or a firewall that drops ICMP while the machine is perfectly reachable over every other protocol.

> [!warning] Windows does not answer pings by default
> Its firewall drops unsolicited ICMP, so a ping to a Windows machine fails on a healthy lab.
> Test that machine with an address and a login instead.
> If you want it to answer, the rule to enable is *File and Printer Sharing (Echo Request - ICMPv4-In)*, and you would be changing the machine's security posture to make a diagnostic convenient, which is a real trade rather than a free one.

---

# SSH

## What the pieces are

| Tool | What it does |
| --- | --- |
| `ssh` | opens a session on another machine, or runs one command there |
| `ssh-keygen` | makes a key pair |
| `ssh-copy-id` | installs your public key into a server's `authorized_keys` |
| `scp` | copies files over the same connection |
| `sftp` | an interactive file session over the same connection |
| `rsync` | copies only what changed, over the same connection |
| `sshd` | the **server** side, the thing the Ubuntu installer's checkbox installed |

Everything in the first six reads `~/.ssh/config`, which is why one alias serves all of them.

## Keys

```bash
ssh-keygen -t ed25519                      # the default choice today
ssh-keygen -t ed25519 -C "kali lab key"    # a comment, to tell keys apart later
ssh-keygen -t rsa -b 4096                  # when something old refuses ed25519
ssh-keygen -l -f ~/.ssh/id_ed25519.pub     # the fingerprint of a key
```

**`ed25519` rather than RSA**, unless you meet a server too old to accept it.
Shorter keys, faster, and no key-size decision to get wrong.

**The passphrase is a second lock, on the key file itself.**
Without one, anybody who gets the file gets the key.
With one, they need the file *and* the passphrase.
`ssh-agent` means you type it once per session rather than once per connection:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

## The files, and what each one is

| Path | Side | What it holds |
| --- | --- | --- |
| `~/.ssh/id_ed25519` | client | **your private key. Never copy this anywhere.** |
| `~/.ssh/id_ed25519.pub` | client | the public half, safe to hand out |
| `~/.ssh/authorized_keys` | **server** | public keys allowed to log in as this account |
| `~/.ssh/known_hosts` | client | server identities you have already accepted |
| `~/.ssh/config` | client | your aliases and their settings |

**Permissions matter and SSH enforces them.**
If `~/.ssh` is not `700`, or a private key is not `600`, SSH refuses to use them rather than warning you.
`chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/id_ed25519` fix the usual cases.

## The client config

```
Host lab
    HostName 10.0.2.6
    User student
    IdentityFile ~/.ssh/id_ed25519

Host lab-*
    User student
    IdentityFile ~/.ssh/id_ed25519
```

Useful options beyond the four the session used:

| Option | What it does |
| --- | --- |
| `Port` | when the server does not listen on 22 |
| `ServerAliveInterval 60` | keeps an idle session from being dropped |
| `ForwardAgent yes` | lets a session use your local keys to reach a third machine. Convenient, and it trusts that server with your agent |
| `StrictHostKeyChecking` | leave it alone. Turning it off disables the check that detects an impostor server |

**Patterns work**, as the `lab-*` block shows, so settings shared by a group of machines are written once.

## Running things without a session

```bash
ssh lab uptime                        # run one command and come back
ssh lab "systemctl is-active ssh.socket"   # quote anything with spaces or arguments
ssh lab < script.sh                   # feed a local script to the remote shell
```

## Copying files

```bash
scp notes.txt lab:                    # to the server's home directory
scp notes.txt lab:/tmp/               # to somewhere specific
scp lab:remote.txt .                  # back again
scp -r folder lab:                    # a whole directory
rsync -av folder/ lab:folder/         # only what changed, and much faster on a second run
```

## Host keys

The first connection to a machine prints a fingerprint and asks you to accept it.
That is the client recording the server's identity in `known_hosts`.

**If it ever asks again for a machine you already accepted, stop and find out why.**
The benign cause is that the server was rebuilt, which happens constantly in a lab.
The other cause is that something is impersonating it.
After a deliberate rebuild:

```bash
ssh-keygen -R 10.0.2.6      # forget that host's old key
```

---

# Small things worth knowing

## `passwd`

```bash
passwd            # change your own password
sudo passwd student   # change another account's, as an administrator
```

The Kali image ships with a **published** default of `kali` / `kali`.
Published means it is not a secret from anybody, which is why it is changed on first login.

## `systemctl`

```bash
systemctl status ssh          # is it running, and what did it last say
sudo systemctl stop ssh       # stop it now
sudo systemctl start ssh      # start it now
sudo systemctl restart ssh    # after changing its configuration
sudo systemctl enable ssh     # start it automatically at boot
sudo systemctl disable ssh    # do not start it at boot
```

> [!warning] On Ubuntu, SSH is started by a socket
> Current Ubuntu does not keep the SSH server running.
> **systemd holds port 22 itself**, through `ssh.socket`, and starts the server when a connection arrives.
> Two consequences are worth remembering.
> `systemctl status ssh` can read `inactive` on a machine that accepts logins perfectly well, so ask about both units with `systemctl is-active ssh.socket ssh.service`.
> And stopping SSH means answering the listener rather than the service, with `sudo systemctl stop ssh.socket`, which stops the service along with it.

**`stop` and `disable` are different**, and mixing them up wastes an evening.
`stop` affects the running system and nothing else, so a reboot brings the service back.
`disable` affects boot and nothing else, so a running service keeps running.

## Checking virtualization support

```bash
grep -c -E 'vmx|svm' /proc/cpuinfo     # Linux: any number above zero means it is on
```

On Windows: **Task Manager**, **Performance**, **CPU**, look for *Virtualization: Enabled*.
On Apple silicon there is nothing to enable.

**This reports what the firmware is exposing**, so a zero means the setting is off in firmware, not that the processor cannot do it.
Almost every 64-bit processor of the last decade can.
