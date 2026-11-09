# Module 0 · Session 2 — Practical Guide Submission

## The Working Environment and the Submission Workflow

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Practical Guide and paste your terminal output, screenshots and written answers into the slots below, in guide order.
> The setup steps before Exercise 1 have no slots of their own: Exercise 4 records all of them.
>
> **Screenshots are evidence you did the work yourself.**
> Pasted text can be copied from anywhere.
> A screenshot of your own machine cannot.
>
> - Capture with **Flameshot**, on the **Print Screen** key you set up.
> - Save each one in the `screenshots/` folder beside this file, under the name its slot gives, for example `ex4-environment.png`, and embed it with `![ex4-environment](screenshots/ex4-environment.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder**.
> The paths inside this file are relative to that folder, so a file handed in alone shows empty boxes where your evidence should be.

---

# Required Exercises

---

## Exercise 1: Clone Both Repositories and Start the Session — REQUIRED

**Your `git remote -v` output, run in your own repository:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the terminal from `cd ~/student-YOUR-USERNAME` down to the `git remote -v` output — `ex1-session-folder.png`)*

**Q1. You cloned two repositories.
Which one do you push to, which one do you only pull, and why does the course keep them apart rather than giving you one?**

```
(your answer here)
```

**Q2. Suppose you had cloned your own repository with its HTTPS address instead of its SSH address.
What would have happened, and why?**

```
(your answer here)
```

---

## Exercise 2: Set Up Obsidian and Fill In the Worksheet — REQUIRED

> [!example] Evidence — screenshot
> *(Obsidian's **Files and links** settings, showing all five settings — `ex2-obsidian-settings.png`)*

**Q1. What do *Default location for new attachments* and *Subfolder name* do together when you paste a screenshot into this worksheet?**

```
(your answer here)
```

**Q2. Obsidian shows a `![[...]]` wikilink image perfectly well.
Why is *Use \[\[Wikilinks\]\]* turned off anyway?**

```
(your answer here)
```

---

## Exercise 3: Set Up VS Code — REQUIRED

**Your `git log --oneline` output, run in VS Code's built-in terminal:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(VS Code showing the Python extension's page, with its publisher and identifier, and the terminal below it — `ex3-vscode.png`)*

**Q1. `git log --oneline` worked without a `cd`.
Why, and what would have happened if you had opened a folder that is not a repository?**

```
(your answer here)
```

**Q2. The extension's name already said *Python*.
Why did you also check its identifier before installing it?**

```
(your answer here)
```

**Q3. You trusted your repository's folder when VS Code asked.
What would you be allowing if you trusted a folder you downloaded from somewhere else?**

```
(your answer here)
```

---

## Exercise 4: Verify the Environment — REQUIRED

**Check 1 — `dpkg-query -W git code flameshot obsidian`:**

```
(paste output here)
```

**Check 2 — `git config --global --list`:**

```
(paste output here)
```

**Check 3 — `ssh -T git@github.com`:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(all three checks in one terminal, captured with Print Screen — `ex4-environment.png`)*

**Q1. Suppose checks 1 and 2 passed and check 3 printed `Permission denied (publickey)`.
What do you know, and what have you ruled out?**

```
(your answer here)
```

**Q2. Check 3 did not ask about GitHub's fingerprint this time.
Why not, and what should you conclude if it ever asks again on this machine?**

```
(your answer here)
```

---

## Exercise 5: Push the Worksheet and Confirm It Arrived — REQUIRED

**Your `git push` output:**

```
(paste output here)
```

**Your `git status` output, after the push:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(this worksheet open on GitHub, showing at least one of its pictures — `ex5-github.png`)*

**Q1. Before the push, `git status` printed both `Your branch is ahead of 'origin/main'` and `nothing to commit, working tree clean`.
Which line decides whether your work counts at the deadline, and why?**

```
(your answer here)
```

**Q2. Why does the course judge the deadline by what is on GitHub rather than by the time on each commit?**

```
(your answer here)
```

**Q3. You can delete a file from your repository at any time.
Why check your screenshots for a password, key or token before pushing, rather than after?**

```
(your answer here)
```

---

## Exercise 6: Hand In the Session 1 Worksheets — REQUIRED

**Your `ls -R Module0-Foundation/Session1` output:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(the `Module0-Foundation/Session1` folder on GitHub, showing both worksheets and the `screenshots` folder — `ex6-session1-github.png`)*

**Q1. Why was the shared folder read-only, and why did you remove it once the files were copied?**

```
(your answer here)
```

**Q2. Why did you copy the two worksheets and the `screenshots` folder by name, rather than the whole shared folder?**

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

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the error `git push` printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
