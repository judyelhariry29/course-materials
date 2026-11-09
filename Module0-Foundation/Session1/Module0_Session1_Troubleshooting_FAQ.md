# Module 0 · Session 1 — Troubleshooting & FAQ

## The Virtual Lab: VirtualBox, the Course Machines, and SSH

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the sentence you would say out loud**, not the step you were on.
> The headings are written the way the problem sounds, because you arrive here mid-failure and you already know what you typed.
> Each entry gives the **cause** before the **fix**, so you learn what happened rather than only what to click.
>
> If nothing here matches, note **the exact step and the exact error** and bring both.

## Contents

- [Before anything boots](#before-anything-boots)
- [Building the machines](#building-the-machines)
- [The network](#the-network)
- [SSH](#ssh)
- [Windows](#windows)
- [Snapshots and disk space](#snapshots-and-disk-space)

---

# Before anything boots

### The machine won't start and says something about VT-x or AMD-V

**Cause.**
Hardware virtualization is turned off in your computer's firmware.
VirtualBox cannot run a 64-bit guest without it, and **this cannot be fixed from inside your operating system.**

**Fix.**
Restart, enter the firmware settings (usually `F2`, `F10`, `Del` or `Esc` during startup), and enable **Intel VT-x**, **Intel Virtualization Technology**, **AMD-V**, or **SVM Mode**.
Save and reboot.
Confirm it:

- **Windows:** Task Manager, Performance, CPU, look for *Virtualization: Enabled*
- **Linux:** `grep -c -E 'vmx|svm' /proc/cpuinfo`, and any number above zero means it is on

### There's no 64-bit option when I create a machine

**Cause.**
The same one.
This is the other face of it: rather than failing at start, VirtualBox hides every 64-bit guest type from the creation wizard, so the setting looks like it is missing rather than disabled.

**Fix.**
As above.
When virtualization is on, the 64-bit versions reappear in the list.

### Everything is painfully slow, and I'm on Windows

**Cause.**
**Hyper-V or WSL2 is enabled.**
Both take ownership of the processor's virtualization features, and VirtualBox is left running your machines in a much slower software mode.
Some combinations refuse to start at all.

**Fix.**
Turn Hyper-V off and reboot.
In **Turn Windows features on or off**, clear **Hyper-V**, **Virtual Machine Platform** and **Windows Hypervisor Platform**.
You lose nothing for this course: everything it does with containers runs **inside Kali**, not on your own machine.

---

# Building the machines

### VirtualBox won't import the Kali file. The dialog doesn't even list it

**Cause.**
You are in **File, then Import Appliance**, which only opens `.ova` files.
The Kali download is a `.7z` containing a **`.vbox`**, which is a machine that already exists rather than an appliance to import.

**Fix.**
Use **Machine**, then **Add**, and select the extracted `.vbox` file.
This is the single most common place to get stuck on this machine.

### I extracted Kali, and now VirtualBox says it can't find the hard disk

**Cause.**
The archive was extracted with `7z e`, which **flattens everything into one directory** and separates the `.vbox` file from the `.vdi` disk it points at.
The machine registers and then cannot find its own disk.

**Fix.**
Delete what you extracted and do it again with `7z x`, which keeps the folder structure.
Then add the `.vbox` again.
If the machine is already registered, remove it first, choosing **Remove only** so the files are left alone.

### The Ubuntu installer never got an address

**Cause.**
The machine's Adapter 1 was not attached to CyberLab before you started the install, so there was no network for DHCP to answer on.

**Fix.**
Power the machine off.
In **Settings**, then **Network**, then **Adapter 1**, set **Attached to: NAT Network** and **Name: CyberLab**.
Start the installer again.
The network step should show a `10.0.2.x` address before you go any further, and that is worth waiting to see.

### I moved the machine's folder and now it won't start

**Cause.**
The `.vbox` file records the path to its disk.
Moving the folder breaks that path.

**Fix.**
Remove the machine from VirtualBox with **Remove only**, then **Machine**, then **Add** the `.vbox` from its new location.
Nothing is lost.
Keep the folder somewhere you will leave alone.

---

# The network

### Both machines reach the internet, but they can't see each other

**Cause.**
One of them is on plain **NAT** rather than the **NAT Network**.
Plain NAT gives each machine a **private network of its own**, so outbound traffic works perfectly and the machines are invisible to one another.
This is the one difference between the two modes that matters.

**Fix.**
Power the machine off.
**Settings**, then **Network**, then **Adapter 1**: **Attached to: NAT Network**, **Name: CyberLab**.
Start it and run `ip a` again.

> [!note] Why the address looked fine
> Plain NAT hands out addresses on `10.0.2.x` too, so `ip a` looks completely normal and the first check passes.
> It is the **ping** that fails.
> That is exactly why the three checks run in order.

### My machine has no IP address at all

**Cause.**
Either the adapter is not attached to anything, or **DHCP is off** on the CyberLab network.

**Fix.**
Check the network first, because it affects every machine:

```bash
VBoxManage list natnets
```

You want `CyberLab`, `Network: 10.0.2.0/24`, `Gateway: 10.0.2.1`, `DHCP Server: Yes`.
If DHCP is off:

```bash
VBoxManage natnetwork modify --netname CyberLab --dhcp on
```

Then check the machine's own Adapter 1 is attached to **NAT Network / CyberLab**.

### I changed the adapter and the address didn't change

**Cause.**
The machine is still holding its old DHCP lease.

**Fix.**
On Linux, reboot the machine, which is the quickest reliable answer.
On Windows:

```
ipconfig /release
ipconfig /renew
```

### The addresses in the guide don't match mine

**Cause.**
Nothing is wrong.
**Addresses come from DHCP**, so the host part is assigned to whoever asks first.
Every address written in the course material is a worked example.

**Fix.**
Use your own, from `ip a` on Linux or `ipconfig` on Windows.
That is why the first verification check is the one that reports your addresses.

---

# SSH

### `Connection refused`

**Cause.**
You reached the machine and **nothing is listening on port 22**.
Almost always this means the **OpenSSH server was not installed** during the Ubuntu install, which is one checkbox on the SSH Setup step.
Occasionally it means the service is stopped.

**Fix.**
At the Ubuntu machine's own console:

```bash
systemctl is-active ssh.socket ssh.service    # is anything listening
sudo apt install openssh-server               # if the server was never installed
sudo systemctl enable --now ssh.socket        # start it, and start it at every boot
```

**`ssh.service` reading `inactive` is normal**, and on its own it is not the fault.
Current Ubuntu keeps port 22 open through `ssh.socket` and starts the server only when a connection arrives, so the socket is the unit to ask about and the unit to start.

### `No route to host`, or `Network is unreachable`

**Cause.**
Different from *refused*.
This one means you never reached the machine at all, so the two machines are **not on the same network**.
Refused means you arrived and were turned away.

**Fix.**
Go back to the network section above.
Check Adapter 1 on both machines.

### It still asks for my password after `ssh-copy-id`

**Cause.**
Usually **file permissions on the server**.
SSH refuses to use `~/.ssh` or `authorized_keys` if they are readable by anyone else, and it **fails silently back to the password** rather than telling you why.
The other cause is copying the key to a different account than the one you log in as.

**Fix.**
On the server:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Then confirm the account matches the `User` line in your `~/.ssh/config`.
To see what is actually happening, ask the client:

```bash
ssh -v lab
```

### `Permissions 0644 for 'id_ed25519' are too open`

**Cause.**
Your **private key** is readable by other accounts on your own machine, so SSH refuses to use it.
This is the client protecting you, not a bug.

**Fix.**

```bash
chmod 600 ~/.ssh/id_ed25519
```

### `Could not resolve hostname lab`

**Cause.**
`lab` is an alias that only exists inside `~/.ssh/config`, and SSH did not find it there.
The file is missing, the `Host lab` line is misspelled, or the file is in the wrong place.

**Fix.**
Check the path and the content:

```bash
cat ~/.ssh/config
```

It must be `~/.ssh/config` exactly, on **the machine you are connecting from**, with `Host lab` at the left margin and the settings indented beneath it.

### `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`

**Cause.**
The server is presenting a **different identity** than the one your machine recorded the first time.
In this lab the innocent explanation is almost always the right one: you **rebuilt the machine or restored a snapshot**, so it has a new host key.

**Fix.**
Only when you know why it changed:

```bash
ssh-keygen -R 10.0.2.6      # forget the old key for that address
```

Then connect again and accept the new fingerprint.

> [!warning] Do not make a habit of this
> Outside a lab, this warning is what tells you something is impersonating the server you meant to reach.
> Clearing it reflexively is how people train themselves past the one alarm that matters.

---

# Windows

### Windows Setup says this PC can't run Windows 11

**Cause.**
The virtual machine is missing one of the three things Windows 11 checks for: **EFI**, **TPM 2.0**, or **Secure Boot**.

**Fix.**
Power the machine off.
In **Settings**, then **System**, enable **EFI**, **TPM 2.0** and **Secure Boot**, then start the install again.

### Setup won't let me continue without a Microsoft account

**Cause.**
Windows pushes hard toward a Microsoft account, and the exact route out moves between builds.

**Fix.**
On **Pro**, at the account step choose **"Set up for work or school"**, then **"Sign-in options"**, then **"Domain join instead"**, which gives you the local-account form.
If your build does not offer that path, finish Setup with a Microsoft account **you are willing to throw away**, then convert it under **Settings**, **Accounts**, **Your info**, **"Sign in with a local account instead"**.

**Do not use a command-line bypass you found online.**
Microsoft is removing them, so anything you learn that way stops working without warning.

### I can't ping the Windows machine

**Cause.**
**Nothing is wrong.**
Windows Firewall drops unsolicited ICMP by default, so the machine does not answer pings even when it is working perfectly and sitting on the right network.

**Fix.**
Nothing to fix.
Check that machine a different way: confirm it has a `10.0.2.x` address with `ipconfig`, and confirm it can reach the others.
If you genuinely want it to answer, the rule to enable is *File and Printer Sharing (Echo Request - ICMPv4-In)*, and you are changing the machine's security posture to make one diagnostic more convenient.

### There's a watermark in the corner saying Windows isn't activated

**Cause.**
You installed without a product key, which is **deliberate** in this course.

**Fix.**
Nothing.
Windows runs indefinitely this way.
The watermark stays and personalization settings are locked, and neither affects a single thing this course asks you to do.

---

# Snapshots and disk space

### I restored a snapshot and the work I'd done is gone

**Cause.**
Restoring puts the **whole machine** back to the moment the snapshot was taken.
It is not an undo of the one change you regret, and it does not know which changes you wanted to keep.

**Fix.**
There is none after the fact, which is the lesson.
**From now on, copy anything you want to keep off the machine before restoring:**

```bash
scp important-notes.txt lab-notes-backup.txt      # or to your submission repository
```

### I'm running out of disk space and I haven't installed anything

**Cause.**
**Snapshots.**
Each one holds a copy of the disk as it was at that moment, and they add up quickly across three machines.

**Fix.**
Delete the ones you no longer need, oldest first:

```bash
VBoxManage snapshot "Ubuntu" list
VBoxManage snapshot "Ubuntu" delete "before the web exercise"
```

> [!note] Deleting a snapshot does not roll anything back
> It **merges** that point into the disk and frees the space it was holding.
> **Restore** is the one that rolls back.
> These two get confused, and only one of them loses work.

### How many snapshots should I keep?

**Two per machine is usually right.**
One at `clean install`, taken the moment the machine first worked, and one before anything you expect to break it.
Ten is a full disk.

**Name them for the state they hold**, never for the date.
`clean install` and `before the web exercise` tell you what you are going back to.
A date does not.
