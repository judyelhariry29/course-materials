# Module 0 · Session 1 — Practical Guide

## The Virtual Lab: VirtualBox, the Course Machines, and SSH

### Professional Training in Cybersecurity I

---

## Overview

This is the only setup the course asks of you, and everything after it runs inside what you build here.
By the end you will have:

1. **VirtualBox installed** on your own computer, and nothing else installed on it
2. **CyberLab**, one network the machines meet on, created before any machine exists
3. **Kali Linux**, the workstation you sit at, with the tools already on it
4. **Ubuntu Server**, the peer with no screen worth using
5. **Windows 11**, the machine later modules land on
6. **A key-based SSH connection** from Kali to the server, reduced to a single word
7. **An end-to-end check** that tells you the lab is real, and **a snapshot of each machine**

**We start all three machines together in the session, and you finish whatever is left at home.**
This guide is written to be picked up from wherever you stopped, by somebody working alone.

> [!example] Submission
> Work in **`Module0_Session1_Practical_Guide_Submission.md`** as you go.
> Each build step below ends with a **Record** box naming exactly what to capture, with the filename to save a screenshot under.
> Most of them are one screenshot or one line of terminal output, taken at the moment it works, which takes seconds then and an hour to reconstruct later.
>
> **The Submission also asks one or two questions per exercise.**
> Answer them as you go, while the reason you did something is still in front of you.

> [!important] You must complete
> All of it.
> This is a build rather than a set of exercises, and a half-built lab blocks every later session.
> Nothing here is optional and nothing here is graded on cleverness.

> [!important] Build in this order
> **The network is created before any machine**, because a machine is attached to a network that already exists.
> Creating it afterwards means going back and editing every machine you already made.
> The rest of the order exists because Windows takes the longest, so it starts early and installs while you work on something else.

---

# Pre-Session Setup

---

## Step 1: The four downloads

If you have not started these, start them now and read on while they run.
They are several gigabytes between them.

1. **VirtualBox**, from `https://www.virtualbox.org/wiki/Downloads`
2. **The Kali Linux VirtualBox image**, from `https://www.kali.org/get-kali/#kali-virtual-machines`.
   The **VirtualBox** image, not the installer ISO and not the VMware one.
3. **The Ubuntu Server ISO**, from `https://ubuntu.com/download/server`.
   Server, not Desktop.
4. **The Windows 11 ISO**, from `https://www.microsoft.com/software-download/windows11`.
   Choose **Download disk image (ISO)**.
   It is the largest, so start it first.

Keep all four in one folder.

## Step 2: What your computer needs

| Requirement | Minimum | Comfortable |
| --- | --- | --- |
| RAM | 8 GB, one machine at a time | 16 GB, all three together |
| Free disk | 100 GB | 120 GB |
| CPU | 64-bit with virtualization support | the same |

**On 8 GB you can still take this course.**
You run one machine at a time instead of three.
Some exercises need two machines talking, so those take longer, and nothing is closed to you.

## Step 3: Turn on virtualization in your firmware

This is the most common reason a virtual machine refuses to start, and **it cannot be fixed from inside the operating system.**

Restart, enter the firmware settings (usually `F2`, `F10`, `Del`, or `Esc` during startup), find a setting named **Intel VT-x**, **Intel Virtualization Technology**, **AMD-V**, or **SVM Mode**, enable it, save, and reboot.

**Confirm it:**

- **Windows:** Task Manager, Performance, CPU, look for *Virtualization: Enabled*
- **Linux:** `grep -c -E 'vmx|svm' /proc/cpuinfo`, and any number above zero means it is on

> [!warning] Apple silicon cannot run this lab
> A Mac with Apple silicon has no virtualization setting to turn on, and that is not the obstacle.
> VirtualBox on an Arm processor runs **Arm guests only**, and all three machines this course builds are x86-64 images.
> No firmware setting changes that, and the emulation switches suggested online are unsupported and far too slow to work in.
>
> **Raise this with your instructor before the session rather than working around it.**
> An Intel Mac, or a Windows or Linux computer, will build the lab exactly as written.

---

# The Build

---

## Exercise 1: Install VirtualBox — REQUIRED

Run the installer and accept the defaults.

- **On Windows**, the installer warns that it will reset your network connection.
  That is expected and it comes back on its own.
- **On Linux**, install the package for your distribution rather than the generic `.run` file, so the kernel modules get rebuilt when your kernel updates.

**Checkpoint:** VirtualBox opens and shows the Manager window with an empty machine list.

> [!warning] If 64-bit guest types are missing from the wizard
> Or the machine later refuses to start with a VT-x error, or it starts and crawls: virtualization is off in your firmware.
> Go back to Step 3.
> Nothing below will work until it is on.

> [!warning] On a Windows host, Hyper-V and WSL2 conflict with VirtualBox
> With either enabled, VirtualBox refuses to start machines or runs them extremely slowly.
> Turn Hyper-V off before building the lab.
> Everything this course does with containers runs inside Kali, so you lose nothing.

> [!example] Record
> A screenshot of the VirtualBox Manager window (`ex1-manager.png`).
> The Submission also asks how you confirmed virtualization was on, so note what you checked and what it said.

---

## Exercise 2: Create the CyberLab network — REQUIRED

One network that all three machines join.
They can reach each other and the internet on it, and nothing outside can start a conversation with them.

**In the VirtualBox Manager:**

1. **Tools**, then the **Network** panel, then the **NAT Networks** tab
2. **Create**
3. Set these three and leave the rest alone:
   - **Name:** `CyberLab`
   - **IPv4 Prefix:** `10.0.2.0/24`
   - **Enable DHCP:** on
4. **Apply**

**The same thing from a terminal**, if you prefer:

```bash
VBoxManage natnetwork add --netname CyberLab --network "10.0.2.0/24" --enable --dhcp on
```

**Checkpoint:**

```bash
VBoxManage list natnets
```

You want a block naming `CyberLab`, with `Network: 10.0.2.0/24`, `Gateway: 10.0.2.1`, and `DHCP Server: Yes`.

> [!note] A NAT Network is not the same as NAT
> Plain **NAT** gives each machine a private network of its own where it cannot see the others.
> A **NAT Network** is one shared network.
> That difference is the whole reason this course uses the second one: the machines have to be able to reach each other.

> [!example] Record
> The output of `VBoxManage list natnets` showing the CyberLab block, **and** a screenshot of the NAT Networks tab (`ex2-cyberlab.png`).

---

## Exercise 3: Build Kali — REQUIRED

Kali is **imported rather than installed**, so it is running within minutes.
The other two are real installs.

1. **Extract the archive.**
   It is a `.7z` containing a `.vbox` file next to a large `.vdi` disk.
   Keep them together, in a folder you intend to leave alone.

   ```bash
   7z x kali-linux-*-virtualbox-amd64.7z
   ```

2. **Add it to VirtualBox:** **Machine**, then **Add**, then select the extracted `.vbox` file.

   > [!warning] This is Add, not Import Appliance
   > **Import Appliance** is for `.ova` files and it will not see a `.vbox`.
   > This is the single most common place to get stuck on this machine.

3. **Set memory** to **4096 MB** in **Settings**, then **System**.

4. **Attach it to CyberLab:** **Settings**, then **Network**, then **Adapter 1**:
   - **Attached to:** NAT Network
   - **Name:** CyberLab

5. **Start it and log in.**
   The image ships with `kali` as both the user name and the password.

   > [!warning] Change that password now
   > It is published by Kali as the image default, which means everybody has it.
   > Run `passwd` the first time you log in.

**Checkpoint:** you reach the Kali desktop and a terminal opens.

> [!example] Record
> The output of `ip a` showing your `10.0.2.x` address, and a screenshot of the Kali desktop with a terminal open (`ex3-kali-desktop.png`).

---

## Exercise 4: Build Ubuntu Server — REQUIRED

A real install, and the machine with no screen of its own once it is built.

1. **Machine**, then **New**:
   - **Name:** `Ubuntu`
   - **Type:** Linux, **Version:** Ubuntu (64-bit)
   - **Memory:** 2048 MB
   - **Disk:** new virtual hard disk, **25 GB**, dynamically allocated

2. **Attach it to CyberLab** in **Settings**, then **Network**, exactly as you did for Kali.

3. **Attach the ISO:** **Settings**, then **Storage**, select the empty optical drive, choose the Ubuntu Server ISO.

4. **Start it and work through the installer.**
   Defaults are correct except where noted:
   - **Network:** it should already show a `10.0.2.x` address, which tells you CyberLab works before you have even finished installing
   - **Storage:** use the entire disk.
     It is a virtual disk and there is nothing else on it
   - **Profile:** a server name of `ubuntu`, and a user name of **`student`**.
     Use that exact name.
     Every example in this course assumes it, and matching it now saves you translating every command later.
     Choose your own password and write it down
   - **SSH Setup: check "Install OpenSSH server"**

   > [!warning] The OpenSSH checkbox is the expensive one to miss
   > Without it the machine has **no way in over the network**, and the only fix is installing it by hand at the console you were trying to avoid using.
   > It is one checkbox and it is easy to click past.

5. **Reboot when the installer asks**, and remove the ISO if VirtualBox has not done it for you.

**Checkpoint:** the machine boots to a text login prompt and your account works.

> [!example] Record
> The output of `ip a` on the Ubuntu machine, the user name you created, and a screenshot of the console (`ex4-ubuntu-console.png`).
> **Write that address down.**
> Exercise 6 needs it.

---

## Exercise 5: Build Windows 11 — REQUIRED

The longest of the three, which is why it started early.

1. **Machine**, then **New**:
   - **Name:** `Windows`
   - **Type:** Microsoft Windows, **Version:** Windows 11 (64-bit)
   - **Memory:** 4096 MB, **Processors:** 2
   - **Disk:** **64 GB**, dynamically allocated
   - In **Settings**, then **System**: **enable EFI**, **TPM 2.0**, and **Secure Boot**.
     Windows 11 checks for all three and refuses to install without them

2. **Attach it to CyberLab**, exactly as before.

3. **Attach the Windows ISO** in **Settings**, then **Storage**.

4. **Work through Setup:**
   - **Edition: Windows 11 Pro**, for two reasons that the next bullets give
   - **When it asks for a product key, choose "I don't have a product key".**
     This is deliberate.
     Windows runs indefinitely without activation.
     You get a watermark in the corner and personalization settings are locked, and neither affects a single thing this course does.
     **That is the first reason this machine is Pro rather than an evaluation build:** a Windows 11 Enterprise evaluation expires **90 days after it is installed**, which would spend most of the license in the weeks before any module that needs a Windows target runs
   - **Custom install**, and select the whole empty disk
   - **Create a local account, not a Microsoft account.**
     This is a disposable lab machine and it should not carry anybody's real identity.
     **Windows 11 Pro supports this and Home does not**, which is the second reason the edition is Pro.
     At the account step choose **"Set up for work or school"**, then **"Sign-in options"**, then **"Domain join instead"**, and Setup gives you the local-account form.
     Use **`student`** here too
   - If your build does not offer that path, finish Setup with a Microsoft account **you are willing to throw away**, reach the desktop, and convert it under **Settings**, then **Accounts**, then **Your info**, then **"Sign in with a local account instead"**.
     Both routes are supported.
     **Do not use a command-line bypass** found online.
     Microsoft is removing them, so anything you learn that way stops working without warning

**Checkpoint:** the machine reaches the Windows desktop.

> [!note] Windows will not answer a ping, and that is correct
> Its firewall drops unsolicited ICMP by default, so a ping to this machine fails even when everything is working.
> Do not go hunting for a fault.
> Check this machine with an address and a login instead.

> [!example] Record
> Its address from `ipconfig`, and a screenshot of the Windows desktop (`ex5-windows-desktop.png`).

---

## Exercise 6: Reach the server over SSH — REQUIRED

The Ubuntu machine has no screen worth using, so this is how it gets used from here on.
**Everything below is typed on Kali.**

1. **Use the Ubuntu address you wrote down** in Exercise 4.
   Everywhere `10.0.2.6` appears below, put yours instead.
   Addresses come from DHCP, so **yours will not be the one printed here.**

2. **Make a key pair**, if you do not already have one:

   ```bash
   ssh-keygen -t ed25519
   ```

   Accept the default location.
   A passphrase is your choice and it protects the key on disk.

   **The private half never leaves this machine.**
   Only the public half is copied anywhere, and the server never needs the private one.

3. **Copy the public half to the server:**

   ```bash
   ssh-copy-id student@10.0.2.6
   ```

   This asks for the Ubuntu password once.
   It is the last time you type it.

4. **Write a client config** so the whole command becomes one word.
   Create or edit `~/.ssh/config` on Kali:

   ```
   Host lab
       HostName 10.0.2.6
       User student
       IdentityFile ~/.ssh/id_ed25519
   ```

5. **Use it:**

   ```bash
   ssh lab
   ```

**Checkpoint:** you get a shell prompt on the Ubuntu machine **without typing a password**.

> [!note] The first connection asks you to confirm a fingerprint
> That is the client telling you it has never seen this server before, and recording its identity.
> Say yes once.
> If it ever asks again for a machine you have already accepted, something changed and it is worth finding out what.

> [!tip] The same alias works for file transfer
> `scp report.md lab:` copies a file to the server, because `scp`, `sftp` and `rsync` all read the same config file.

> [!example] Record
> Your `~/.ssh/config` entry as you actually wrote it, the terminal text from `ssh lab` to the server prompt, and a screenshot of it (`ex6-ssh-lab.png`).

---

## Exercise 7: Verify the whole lab — REQUIRED

Three checks, and **each one depends on the one before it**, so the first failure tells you exactly how far the lab got.
Run them from Kali.

| # | Command | What you should see | What a failure means |
| --- | --- | --- | --- |
| 1 | `ip a`, or `ipconfig` on Windows | a `10.0.2.x` address | the machine is not on CyberLab, or DHCP is off |
| 2 | `ping -c 1 <your Ubuntu address>` | a reply | both have addresses but are not on the same network |
| 3 | `ssh lab` | a shell prompt on the server | the network is fine, so the problem is SSH, the account, or the key |

**Run check 1 on all three machines**, with `ip a` on Kali and Ubuntu and `ipconfig` on Windows, which has no `ip` command.
Run check 2 against Ubuntu only, because Windows will not answer it and that is correct behavior rather than a broken lab.

**If all three pass, the lab is real.**

> [!example] Record
> All three commands with their output, check 1 from each of the three machines (`ipconfig` on the Windows one), and a screenshot of the three checks in one terminal (`ex7-three-checks.png`).

---

## Exercise 8: Take the snapshots — REQUIRED

Do this **before running anything in the lab**, on all three machines, while they are shut down.

1. Select the machine, open **Snapshots**, choose **Take**
2. Name it **`clean install`**

**Name a snapshot for the state it holds, not for the date.**
`clean install` and `before the web exercise` tell you what you are going back to.
A date does not.

**Take a second one before anything you expect to break a machine.**
Those two cover almost everything.

**They are not free.**
Each one keeps a copy of the disk as it was at that moment, so two per machine is usually right and ten is a full disk.

> [!warning] Restoring is not undoing your last action
> It puts the **whole machine** back to that point.
> Anything you wanted to keep comes off the machine first.

> [!example] Record
> A screenshot of the Snapshots panel for each machine showing `clean install` (`ex8-snapshots-kali.png`, `ex8-snapshots-ubuntu.png`, `ex8-snapshots-windows.png`).

---

# When something fails

**Note the exact step and the exact error, and bring both.**
A failure you can describe is a two-minute fix.
A failure described as "it did not work" is not.

The Troubleshooting FAQ is organized by the symptom in front of you rather than by the step that produced it, which is usually how you arrive at it.

---

# What "done" looks like

- VirtualBox installed, and CyberLab listed with DHCP on
- All three machines boot and you can log in to each
- `ssh lab` from Kali lands on the Ubuntu server without a password
- All three checks pass
- Each machine has a `clean install` snapshot
- Your Submission has a Record entry for every exercise above

**Everything after this session runs inside what you just built.**
If a machine is not finished, finish it before the next session rather than after it.
