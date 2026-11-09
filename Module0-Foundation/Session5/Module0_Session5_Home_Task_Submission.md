# Module 0 · Session 5 — Home Task Submission

## Checking Connections Against a Watchlist

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Home Task and paste your code, terminal output, screenshot and written answers into the slots below, in task order.
> Everything here is required.
>
> **Paste inside each box, never over its first or last line.**
> A box for code opens with `python`, and a box for a command with its output opens with `bash`.
> Each slot gets its own box, as the slot asks.
>
> **The screenshot is evidence you did the work yourself.**
> Pasted text can be copied from anywhere.
> A screenshot of your own machine cannot.
>
> - Capture with **Flameshot**, on the **Print Screen** key.
> - Save it in the `screenshots/` folder beside this file as `task1-watchlist.png`, and embed it with `![task1-watchlist](screenshots/task1-watchlist.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder**.
> The paths inside this file are relative to that folder, so a file handed in alone shows an empty box where your evidence should be.

---

# Task 1: Build the Watchlist Checker — REQUIRED

**Your completed `watchlib.py`** (all `# TODO`s filled in):

```python
(paste your completed watchlib.py here)
```

**Your completed `watchlist.py`** (all `# TODO`s filled in):

```python
(paste your completed watchlist.py here)
```

**The three setup commands, from `./watchlist.py connections.log` to `./watchlist.py -h`:**

```bash
(paste commands and output here)
```

**`./watchlist.py connections.log`, then `cat report.txt`:**

```bash
(paste commands and output here)
```

**The `--out hits.txt` run, then `diff report.txt hits.txt && echo same`:**

```bash
(paste commands and output here)
```

**`./watchlist.py`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**`./watchlist.py missing.log`, followed by `echo $?`:**

```bash
(paste commands and output here)
```

**`head -c 6 watchlist.bin > cut.bin`, the run with `--watchlist cut.bin`, and `echo $?`:**

```bash
(paste commands and output here)
```

> [!example] Evidence — screenshot
> *(the check and `cat report.txt` in the terminal — `task1-watchlist.png`)*

**Q1. `connections.log` has ten lines, and the run reports `4 skipped`.
For each skipped line, name what is wrong with it and which line of your code raises the `ValueError` that skips it.**

```
(your answer here)
```

**Q2. `read_watchlist` turns each 4 bytes into an `ipaddress` address object, and `parse_line` does the same to each host, before they are compared with `in`.
Why convert both sides to the same type rather than compare the log's text with the watchlist's bytes, and what would `host in watched` give if only one side were converted?**

```
(your answer here)
```

**Q3. The run reports `3 watched`, yet the report lists only two hosts.
What does the third watched address tell a defender, and why is a watchlist that is never matched still worth checking against every day?**

```
(your answer here)
```

---

# Anything that failed

If something did not work, describe it here: **the exact step, the exact message, and what you tried.**
This is not a penalty.
A failure you can describe is a two-minute fix, and describing it accurately is a graded skill in this course.

```
(your answer here, or "nothing failed")
```

---

# AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `AttributeError` the starter printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
