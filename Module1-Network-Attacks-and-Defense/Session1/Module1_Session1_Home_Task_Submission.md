# Module 1 · Session 1 — Home Task Submission

## Reading and Rewriting the Wire

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact** for the home task.
> Work through the Home Task and paste your final code, terminal output, and written answers into the slots below, in task order.
> **Every section is required.**
> There are no optional tasks, and every script must run without errors.
>
> **Paste inside each box, never over its first or last line.**
>
> **Screenshots are evidence you ran the work yourself.**
> A pasted output can be copied, but a screenshot of your own terminal cannot.
> Replace each screenshot slot with a real capture.
> - Use **Flameshot** for clean, annotated captures.
> - Keep them in a `screenshots/` folder beside this file, named for the task (for example `task1-forger.png` or `task4-report.png`), and embed each with `![task1-forger](screenshots/task1-forger.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# Pair 1: A Checksum Is Not a Signature

---

## Task 1: Forge a Source Address That Still Verifies — REQUIRED

> 🗡️ Offensive · 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`header_forger.py`, all TODOs filled in):

```python

```

**Your `header_forger.py` output** (all five rows, with `forged_spoof.bin` reading `src 10.0.0.99` and `valid`):

```
(paste the header_forger.py output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your run, with the spoofed but valid row visible, here — `task1-forger.png`)*

---

## Task 2: Audit a Frame Against Its Own Headers — REQUIRED

> 🛡️ Defensive · 🔨 **FROM SCRATCH**

**Your code** (`packet_auditor.py`):

```python

```

**Your `packet_auditor.py` output** (verdicts for all five frames):

```
(paste: python3 packet_auditor.py ref_frame.bin forged_ttl.bin forged_sloppy.bin forged_spoof.bin forged_length.bin)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the five verdicts here — `task2-auditor.png`)*

**Pair 1 questions**

**Q1. Your forger rewrote `forged_spoof.bin`'s source address and recomputed the checksum, and `packet_auditor.py` passed it.
Walk through why recomputing the checksum makes that edit invisible to any checksum-based test.**

```
(your answer here)
```

**Q2. The auditor caught `forged_sloppy.bin` and `forged_length.bin` but not `forged_spoof.bin`.
What class of forgery can a single frame's own headers expose, and what class can they never expose?
Which of the four forgeries sits on that boundary?**

```
(your answer here)
```

**Q3. A checksum proves the header was not corrupted in transit, and nothing about who wrote it.
Name what a receiver would actually need in order to trust the source of a frame, and say why arithmetic over the bytes cannot provide it.**

```
(your answer here)
```

---

# Pair 2: Plaintext Travels as Plaintext

---

## Task 3: Read the Payloads Out of a Capture — REQUIRED

> 🗡️ Offensive · 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`payload_harvester.py`, all TODOs filled in):

```python

```

**Your `payload_harvester.py` output** (the FTP `USER` and `PASS` in the clear, the decoded HTTP credentials, and the DNS hostname):

```
(paste the payload_harvester.py output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the recovered credentials here — `task3-harvester.png`)*

---

## Task 4: Report the Exposed Conversations — REQUIRED

> 🛡️ Defensive · 🔨 **FROM SCRATCH**

**Your code** (`exposure_report.py`):

```python

```

**Your report** (one row per conversation, with the verdicts and credential findings):

```
(paste the exposure_report.py output here)
```

**The `strings` cross-check:**

```
(paste: strings -n 4 lab_capture.bin)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your report beside the `strings` output here — `task4-report.png`)*

**Pair 2 questions**

**Q1. Your harvester turned the HTTP `Authorization: Basic` header into `admin:s3cr3t`.
Base64 is not encryption, so what did "decoding" it actually require, and why is calling that "breaking" the credential wrong?**

```
(your answer here)
```

**Q2. `exposure_report.py` rated the DNS frame PARTIAL rather than opaque, even though most of its bytes are binary.
Why is PARTIAL still an exposure, and what specifically leaked?**

```
(your answer here)
```

**Q3. Both tools failed on exactly the same one frame, the TLS record, and succeeded on every other conversation with the same simple parse.
What made that frame different, and what does that tell you the real fix for the exposed conversations is, and is not?**

```
(your answer here)
```

---

# Anything that failed

If something did not work, describe it here: **the exact step, the exact message, and what you tried.**
It earns no points itself, but a failure described precisely keeps the marks for everything that works.
A failure you can describe is a two-minute fix.

```
(your answer here, or "nothing failed")
```

---

# AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `struct.error` my forger printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
