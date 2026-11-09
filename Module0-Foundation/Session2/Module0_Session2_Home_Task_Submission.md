# Module 0 · Session 2 — Home Task Submission

## A Lab Card, Written and Handed In

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact** for the home task.
> Work through the Home Task and fill in the slots below, in task order.
>
> Two slots are different from the rest: **your lab card** in Task 1 and **your corrected section** in Task 2 are written directly on this page, as Markdown, not pasted into a box.
> Replace each one's placeholder line with your own Markdown, and check it in the reading view with **Ctrl+E**.
>
> Save each screenshot in the `screenshots/` folder beside this file, under the name its slot gives, and embed it with `![task1-lab-card](screenshots/task1-lab-card.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this file together with its `screenshots/` folder**.

---

# Task 1: Write a Lab Card in Markdown

**Your lab card, written directly below this line in place of the placeholder:**

### My Lab

This lab is designed to test network **connectivity** between virtual machines.

| Machine | Role              | Address     |
| ------- | ----------------- | ----------- |
| Kali    | Attacker / Client | 10.0.2.15   |
| Ubuntu  | Target Server     | 10.0.2.5    |
| Windows | Host / Management | 192.168.1.5 |
**Q1. Your screenshot's path is `screenshots/task1-lab-card.png`, not `/home/kali/student-YOUR-USERNAME/...`. Where is that path read from, and why would the full path show a broken image to your instructor even though it works on your machine?**

The path `screenshots/task1-lab-card.png` is read **relatively** from the location of the Markdown file itself. If you use the full local path (`/home/kali/...`), that path is unique to your specific machine; when your instructor clones and opens the repository on their own computer, that exact directory structure will not exist there, causing the image to appear broken even though it works locally on your machine[cite: 1].

**Q2. Your screenshot line starts with `!`. What would the same line show without the `!`?**

Without the exclamation mark `!` (written as `[task1-lab-card](screenshots/task1-lab-card.png)`), the line would render as a **standard clickable hyperlink** instead of embedding and displaying the actual image directly on the page[cite: 1, 2].

```

---

# Task 2: Correct a Broken Section

**The four mistakes: for each line, what is wrong, and what Obsidian shows because of it.**

**2a — Line 1 (`###Lab Checks`):** _Answer:**What is wrong:** Missing the required space between the header hashes (`###`) and the text (`Lab Checks`). **What Obsidian shows:** Renders as plain text instead of a formatted level-3 header_

**2b — Lines 3–4 (the two table lines):** _Answer:_**What is wrong:** Missing the markdown table delimiter row (`|---|---|`) right below the header row, and the table contains an unequal number of cells/pipes. **What Obsidian shows:** Renders as normal broken text or paragraphs instead of a structured table

**2c — Line 6 (` ```bash `):** _Answer:What is wrong: An unmatched/unclosed fenced code block marker. Since there is no closing set of backticks, it swallows everything that follows it.
What Obsidian shows: Turns the rest of the file into a giant code block, destroying all markdown formatting, headers, and images below it.**What is wrong:** An unmatched/unclosed fenced code block marker. Since there is no closing set of backticks, it swallows everything that follows it. **What Obsidian shows:** Turns the rest of the file into a giant code block, destroying all markdown formatting, headers, and images below it._

**2d — Line 9 (the image line):** _Answer:_**What is wrong:** Spaces are used inside the image file name and path (`task1 lab card.png`), which breaks markdown link parsing. **What Obsidian shows:** A broken image icon or a failed link because file paths cannot contain unescaped spaces.

**Your corrected section, written directly below this line in place of the placeholder:**

### Lab Checks

| Check | Result |
|---|---|
| Kali reaches Ubuntu | passed |

```bash
ping -c 1 10.0.2.5

> [!example] Evidence — screenshot
> *(the corrected section in the reading view, its picture showing — `task2-fixed.png`)*

**Q1. The mistake on line 6 broke more than its own line.
What did it do to the rest of the section, and why does that make it the most expensive of the four in a worksheet?**

```
he unmatched backticks of line 6 left the code block open, causing everything below it in the section to be treated as part of the code block instead of regular Markdown[cite: 3]. This makes it the most "expensive" mistake because a single missing character destroys the formatting, headers, tables, and images of the entire remaining section, requiring a complete structural review to fix[cite: 3].
```

---

# Task 3: Hand It In and Confirm It Arrived

**Your `git push` output:**

```
(paste output here)
```

**Your `git status` output, after the push:**

```
(paste output here)
```

**Your `git log --oneline -3` output:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(this worksheet open on GitHub, showing your lab card and its picture — `task3-github.png`)*

**Q1. The newest line of `git log --oneline` shows `(HEAD -> main, origin/main)`.
What does each of the two names tell you, and what would it mean if `origin/main` were one line lower?**

```
(your answer here)
```

**Q2. You committed twice but pushed once.
Until the push, who could see your two commits, and what would that have meant at 22:00 on Saturday?**

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

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the error `git push` printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
