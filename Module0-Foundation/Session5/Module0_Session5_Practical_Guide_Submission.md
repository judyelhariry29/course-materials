# Module 0 · Session 5 — Practical Guide Submission

## Python Essentials for Cybersecurity

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Practical Guide and paste your code, terminal output, screenshots and written answers into the slots below, in guide order.
> Setup has no slots of its own: everything it builds is used, and so proven, by the exercises.
>
> **Paste inside each box, never over its first or last line.**
> A box for code opens with `python`, and a box for a command with its output opens with `bash`.
> Each command's output goes in its own box, as the slot asks.
>
> **Screenshots are evidence you did the work yourself.**
> Pasted text can be copied from anywhere.
> A screenshot of your own machine cannot.
>
> - Capture with **Flameshot**, on the **Print Screen** key.
> - Save each one in the `screenshots/` folder beside this file, under the name its slot gives, for example `ex1-venv.png`, and embed it with `![ex1-venv](screenshots/ex1-venv.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder**.
> The paths inside this file are relative to that folder, so a file handed in alone shows empty boxes where your evidence should be.

---

# Required Exercises

---

## Exercise 1: Give a Project Its Own Python — REQUIRED

**Your `which python3` output, with the environment active:**

```
(paste output here)
```

**Your `pip show requests` output, inside the environment:**

```
(paste output here)
```

**Your `python3 -m pip show requests` output, after `deactivate`:**

```
(paste output here)
```

**Your `hello.py`:**

```python
(paste your hello.py here)
```

**The four `hello.py` commands, with what they printed:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the terminal from `deactivate` down to Kali's `Location:` line — `ex1-venv.png`)*

**Q1. After `source .venv/bin/activate` you typed `python3` and `pip` exactly as before, yet they ran the environment's copies.
What did activation change, and how does the shell's search for a command produce that result?**

```
(your answer here)
```

**Q2. Kali's own copy of `requests` lists fifteen Kali packages under `Required-by:`.
Why does Kali refuse `pip install` outside an environment, and what could go wrong if it allowed it?**

```
(your answer here)
```

**Q3. After `chmod +x`, `./hello.py` ran with no `python3` in front of it.
Which line of the file chose the program that read it, and which `python3` did that line find while your environment was active?**

```
(your answer here)
```

---

## Exercise 2: Take One Log Line Apart — REQUIRED

**Your completed `logline.py`** (all `# TODO`s filled in):

```python
(paste your completed logline.py here)
```

**The run where you typed `3389`:**

```bash
(paste command and output here)
```

**The run where you typed `rdp`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the `rdp` run and its traceback — `ex2-logline.png`)*

**Q1. `LINE[42:47]` gives the text `'51544'`, and `int()` turns it into the number `51544`.
Why must a port be converted before `{dst_port:#06x}` or `0 <= asked <= 65535` can work on it?**

```
(your answer here)
```

**Q2. Typing `rdp` stopped the program with a `ValueError`.
Which call raised it, and why is that call the one that fails rather than `input()`?**

```
(your answer here)
```

**Q3. Your slices work because this firewall pads every field to a fixed width.
What would go wrong with your slices on a line from a firewall whose source-host field is one character wider, and what does that tell you about where slice positions come from?**

```
(your answer here)
```

---

## Exercise 3: Tally a Firewall's Day — REQUIRED

**Your `tally.py`:**

```python
(paste your tally.py here)
```

**Its output:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the `python3 tally.py` run — `ex3-tally.png`)*

**Q1. Your counts use `actions.get(action, 0) + 1`.
What does `.get` return the first time an action appears, and what would `actions[action] + 1` do on that same first event?**

```
(your answer here)
```

**Q2. Nine events passed the port check, yet the output says `Unique sources: 4`.
How does a set produce that number without any code that looks for repeats?**

```
(your answer here)
```

**Q3. Your loop skips the two impossible ports before counting anything.
What would the summary have reported if they had been counted, and why does that matter to someone reading it to decide what happened on the network?**

```
(your answer here)
```

---

## Exercise 4: Split a Script Into a Module — REQUIRED

**Your completed `endpoint.py`** (all `# TODO`s filled in):

```python
(paste your completed endpoint.py here)
```

**Your completed `check.py`** (all `# TODO`s filled in):

```python
(paste your completed check.py here)
```

**Your `python3 endpoint.py` output:**

```
(paste output here)
```

**Your `python3 check.py` output:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(both runs in the terminal — `ex4-check.png`)*

**Q1. `parse_endpoint` ends with `return host, int(port)`.
What single value does the caller receive, and how does `host, port = endpoint.parse_endpoint(text)` turn it into two names?**

```
(your answer here)
```

**Q2. `check.py` imports `endpoint.py`, which runs it, yet `endpoint.py`'s three test lines did not appear in `check.py`'s output.
Which line of `endpoint.py` kept them out, and how does it tell the two runs apart?**

```
(your answer here)
```

**Q3. The parsing could have stayed inside `check.py`.
What does putting it in a module of its own give the next tool that needs to read `host:port` text?**

```
(your answer here)
```

---

## Exercise 5: Read a Log That Has Bad Lines — REQUIRED

**Your `clean.py`:**

```python
(paste your clean.py here)
```

**Your `python3 clean.py` output:**

```
(paste output here)
```

**Your `cat clean.log` output:**

```
(paste output here)
```

**The run from `/tmp`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the run, `cat clean.log` and the run from `/tmp` — `ex5-clean.png`)*

**Reading a traceback.**
Your answers to the guide's questions on the `unhandled.py` traceback, one value each:

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**2c —** _Answer:_

**3a —** _Answer:_

**Q1. The line `09:16:00 10.0.0.12` has no port, and the line ending `ssh` has a port that is not a number.
Which operation fails on each line, and why does one `except ValueError` handle both?**

```
(your answer here)
```

**Q2. A bad line is skipped and the loop carries on, but a missing `access.log` ends the program with `raise SystemExit`.
Why does the program treat these two failures differently?**

```
(your answer here)
```

**Q3. Your `except` names `ValueError`.
What would a bare `except:` catch as well, and why would that make a mistake in your own code harder to find?**

```
(your answer here)
```

---

## Exercise 6: Decode a Binary Address File — REQUIRED

**Your completed `readaddrs.py`** (all `# TODO`s filled in):

```python
(paste your completed readaddrs.py here)
```

**The run on `addrs.bin`:**

```bash
(paste command and output here)
```

**The run on `bad.bin`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**The run on `short.bin`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the three runs in the terminal — `ex6-readaddrs.png`)*

**Q1. `data[0:4]` and `data[4]` read the same bytes object.
What type does each return, and why does the tag check use a slice while the count uses an index?**

```
(your answer here)
```

**Q2. `short.bin` ended with `needs 17 bytes, has 12`.
Without the length check, what would your program have done with that file?**

```
(your answer here)
```

**Q3. `bad.bin` is laid out like `addrs.bin`, but its tag reads `ADR2`.
Why does a reader check the tag before reading anything else in a file?**

```
(your answer here)
```

---

## Exercise 7: Turn a Script Into a Command-Line Tool — REQUIRED

**Your `lines.py`:**

```python
(paste your lines.py here)
```

**Your `addrcheck.py`:**

```python
(paste your addrcheck.py here)
```

**`python3 lines.py`:**

```bash
(paste command and output here)
```

**`python3 lines.py clean.log`:**

```bash
(paste command and output here)
```

**`python3 lines.py access.log clean.log`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**`python3 addrcheck.py -h`:**

```bash
(paste command and output here)
```

**`python3 addrcheck.py 10.0.0.5 --port 22`:**

```bash
(paste command and output here)
```

**`python3 addrcheck.py 2001:db8::1`:**

```bash
(paste command and output here)
```

**`python3 addrcheck.py 10.0.0.256`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**`python3 addrcheck.py 10.0.0.5 --port ssh`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**`python3 addrcheck.py 10.0.0.5 --port 70000`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the `10.0.0.256` and `70000` runs with their two exit statuses — `ex7-addrcheck.png`)*

**Q1. `python3 addrcheck.py 10.0.0.256` never reached your first `print`.
What rejected the address, and at which point in your program did that happen?**

```
(your answer here)
```

**Q2. `--port ssh` ended with exit status 2, and `--port 70000` with 1.
What does each status say about how the run failed, and why would a script that runs your tool care about the difference?**

```
(your answer here)
```

**Q3. `lines.py` reads `sys.argv` itself, and `addrcheck.py` hands its arguments to `argparse`.
Name two things `argparse` gave `addrcheck.py` that `lines.py` either does not have or had to write by hand.**

```
(your answer here)
```

---

## Anything that failed

If something did not work, describe it here: **the exact step, the exact message, and what you tried.**
This is not a penalty.
A failure you can describe is a two-minute fix, and describing it accurately is a graded skill in this course.

```
(your answer here, or "nothing failed")
```

---

## AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the traceback `tally.py` printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
