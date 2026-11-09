# Module 0 · Session 1 — Home Task Submission

## Proving the Lab Does What It Claims

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact** for the home task.
> Paste your commands, their output, your screenshots and your written answers into the slots below, in task order.
>
> Keep screenshots in a `screenshots/` folder beside this file and embed each with `![task2-plain-nat](screenshots/task2-plain-nat.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this file together with its `screenshots/` folder**.

> [!important] Tasks 2 and 4 must be put back
> Both of them change a machine on purpose and both of them end by restoring it.
> **Your last piece of evidence in each is the proof that you restored it.**
> A task left half-done breaks the lab for the next session, and it is marked as incomplete.

---

# Task 1: Finish the build

**Was anything unfinished at the end of the session?**

```
(your answer here)
```

**The three checks, from Kali:**

```bash
(paste ip a, ping, and ssh lab here)
```

**Check 1 from each of the three machines (`ip a` on Kali and Ubuntu, `ipconfig` on Windows):**

```
Kali:
Ubuntu:
Windows:
```

> [!example] Evidence — screenshot
> *(all three checks in one terminal — `task1-checks.png`)*

---

# Task 2: Prove a NAT Network is not NAT

**Your prediction, written before you changed anything:**

```
(what you expected each of the three checks to do under plain NAT)
```

**The three checks with Kali on plain NAT:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the failing check, with the adapter setting visible if you can fit both — `task2-plain-nat.png`)*

**The three checks after you restored CyberLab:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(Adapter 1 back on NAT Network / CyberLab, and the checks passing — `task2-restored.png`)*

**Q1. Which checks changed and which did not?
Be exact about which one failed first.**

```
(your answer here)
```

**Q2. Kali still reached the internet under plain NAT.
Explain why that is consistent with it being unable to reach Ubuntu.**

```
(your answer here)
```

**Q3. What does the first failing check tell you that the others do not?**

```
(your answer here)
```

---

# Task 3: Prove the client config is not only for `ssh`

**`ssh lab uptime`:**

```bash
(paste command and output here)
```

**`scp lab-notes.txt lab:`:**

```bash
(paste command and output here)
```

**`scp lab:lab-notes.txt returned-notes.txt` and `cat returned-notes.txt`:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(all three commands in one terminal — `task3-scp.png`)*

**Q1. Neither `scp` command named an address, an account or a key.
Where did each of those come from?**

```
(your answer here)
```

**Q2. The server's address is handed out by DHCP and could change.
What exactly would you edit, and how many places?**

```
(your answer here)
```

**Q3. Name one thing `ssh lab uptime` lets you do that opening a session and typing `uptime` does not.**

```
(your answer here)
```

---

# Task 4: Prove what a snapshot actually restores

**Creating the file, and `ls ~` showing it:**

```
(paste output here)
```

**Stopping the listener, and the failing `ssh lab` from Kali:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the failed connection — `task4-broken.png`)*

**After restoring `clean install` — is SSH working, and is the file there?**

```bash
(paste ssh lab and ls ~ here)
```

> [!example] Evidence — screenshot
> *(the restored machine with SSH working — `task4-restored.png`)*

**Q1. What happened to `important-notes.txt`, and why?**

```
(your answer here)
```

**Q2. Explain "restoring is not undoing your last action" in your own words, using what you just observed.**

```
(your answer here)
```

**Q3. Name one thing a snapshot does not protect you from.**

```
(your answer here)
```

---

# Task 5: Short answers

**Q1. Why is the network created before the machines rather than after?
What specifically would you have to redo if you built the machines first?**

```
(your answer here)
```

**Q2. A ping to your Windows machine fails.
Give two different explanations, one where the lab is working correctly and one where it is not, and say which check would tell them apart.**

```
(your answer here)
```

**Q3. When you log in with a key, what crosses the wire?
Explain why someone who captured it still could not log in as you afterward.**

```
(your answer here)
```

**Q4. Why does the server never need your private key?
What does it hold instead, and what can it do with that?**

```
(your answer here)
```

**Q5. Nothing outside can start a conversation with your lab machines, and no rule was written to stop it.
Explain where that protection actually comes from.**

```
(your answer here)
```

**Q6. That protection does not work in the other direction.
Say what stops you from reaching something real, in one sentence.**

```
(your answer here)
```

---

# Confirmation

- [ ] Kali's Adapter 1 is back on **NAT Network / CyberLab**
- [ ] The Ubuntu machine has been **restored** and `ssh lab` works
- [ ] All three machines boot and all three checks pass
- [ ] Screenshots are in `screenshots/` beside this file

---

# AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain an error VirtualBox showed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
