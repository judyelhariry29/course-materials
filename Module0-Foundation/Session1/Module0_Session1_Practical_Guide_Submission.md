# Module 0 · Session 1 — Practical Guide Submission

## The Virtual Lab: VirtualBox, the Course Machines, and SSH

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Practical Guide and paste your terminal output, screenshots and written answers into the slots below, in guide order.
>
> **Screenshots are evidence you did the work yourself.**
> Pasted text can be copied from anywhere.
> A screenshot of your own machine cannot.
>
> - **Capture each window where it actually lives.**
>   The VirtualBox Manager, the NAT Networks tab and the Snapshots panels belong to your **host**, so capture those with the host's own tool (`PrtSc` on Windows or Ubuntu, `Shift`+`Command`+`4` on macOS).
>   Anything inside a machine is captured from that machine's own desktop.
>   A dedicated capture tool arrives in a later session, and nothing here needs it.
> - Keep them in a `screenshots/` folder beside this file, named for the exercise, for example `ex3-kali-desktop.png`, and embed each one with `![ex3-kali-desktop](screenshots/ex3-kali-desktop.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder**.
> The paths inside this file are relative to that folder, so a file handed in alone shows empty boxes where your evidence should be.

---

# The Build

---

## Exercise 1: Install VirtualBox — REQUIRED

> [!example] Evidence — screenshot
> *(the VirtualBox Manager window — `ex1-manager.png`)*

**Q1. Did you have to change anything in your firmware, and how did you confirm virtualization was on?**

```
(your answer here)
```

---

## Exercise 2: Create the CyberLab network — REQUIRED

**Your `VBoxManage list natnets` output, the CyberLab block:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the NAT Networks tab showing CyberLab — `ex2-cyberlab.png`)*

**Q1. Why does the network have to exist before the machines rather than after?**

```
(your answer here)
```

**Q2. What does a NAT Network give you that plain NAT does not?**

```
(your answer here)
```

---

## Exercise 3: Build Kali — REQUIRED

**`ip a` on Kali, the line showing your address:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the Kali desktop with a terminal open — `ex3-kali-desktop.png`)*

**Q1. Kali is imported and the other two are installed.
What is the difference, and why is this machine the one that is imported?**

```
(your answer here)
```

**Q2. The image ships with a published default password.
What did you do about it, and why does it matter that the default is published?**

```
(your answer here)
```

---

## Exercise 4: Build Ubuntu Server — REQUIRED

**`ip a` on Ubuntu, the line showing your address:**

```
(paste output here)
```

**The user name you created:**

```
(should be student)
```

> [!example] Evidence — screenshot
> *(the Ubuntu login prompt or a logged-in console — `ex4-ubuntu-console.png`)*

**Q1. What does the "Install OpenSSH server" checkbox do, and what would it have cost you to miss it?**

```
(your answer here)
```

---

## Exercise 5: Build Windows 11 — REQUIRED

**`ipconfig` on Windows, the line showing your address:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the Windows desktop — `ex5-windows-desktop.png`)*

**Q1. You installed without a product key.
What are the consequences, and why was that chosen over an evaluation edition?**

```
(your answer here)
```

**Q2. Which route did you use to create a local account, and why is a local account the right choice for a lab machine?**

```
(your answer here)
```

---

## Exercise 6: Reach the server over SSH — REQUIRED

**Your `~/.ssh/config` entry, as you actually wrote it:**

```
(paste your Host block here)
```

**`ssh lab` landing on the server:**

```bash
(paste the terminal here, from the command to the server prompt)
```

> [!example] Evidence — screenshot
> *(your Kali terminal showing `ssh lab` and the server prompt — `ex6-ssh-lab.png`)*

**Q1. Where does your private key live, and what did the server receive instead?**

```
(your answer here)
```

**Q2. You typed the Ubuntu password exactly once, during `ssh-copy-id`.
Why is it not needed after that?**

```
(your answer here)
```

---

## Exercise 7: Verify the whole lab — REQUIRED

**Check 1 — `ip a` on Kali and Ubuntu, `ipconfig` on Windows:**

```
Kali:
Ubuntu:
Windows:
```

**Check 2 — `ping -c 1 <ubuntu address>` from Kali:**

```
(paste output here)
```

**Check 3 — `ssh lab` from Kali:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(all three checks in one terminal — `ex7-three-checks.png`)*

**Q1. Suppose check 1 passed and check 2 failed.
What do you know, and what have you ruled out?**

```
(your answer here)
```

**Q2. Why is check 2 not run against the Windows machine?**

```
(your answer here)
```

---

## Exercise 8: Take the snapshots — REQUIRED

> [!example] Evidence — screenshot
> *(the Snapshots panel for each of the three machines, showing `clean install` — `ex8-snapshots-kali.png`, `ex8-snapshots-ubuntu.png`, `ex8-snapshots-windows.png`)*

**Q1. Why is a snapshot named for the state it holds rather than for the date?**

```
(your answer here)
```

**Q2. You have a file on a machine that you want to keep, and you are about to restore a snapshot taken before that file existed.
What has to happen first, and why?**

```
(your answer here)
```

---

## Anything that failed

If something did not work, describe it here: **the exact step, the exact error, and what you tried.**
This is not a penalty.
A failure you can describe is a two-minute fix, and describing it accurately is a graded skill in this course.

```
(your answer here, or "nothing failed")
```

---

## AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain an error VirtualBox showed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
