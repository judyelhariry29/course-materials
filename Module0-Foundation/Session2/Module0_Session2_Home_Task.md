# Module 0 · Session 2 — Home Task

## A Lab Card, Written and Handed In

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> In the Practical Guide you ran the submission cycle once, with help.
> **This home task runs it once more, at home, on your own.**
> The content is easy on purpose: you write about the lab you built in Session 1, and you correct a short piece of broken Markdown.
> What is assessed is the mechanics: Markdown that renders, screenshots that show, and commits that reach GitHub before the deadline.
>
> Your worksheet is **`Module0_Session2_Home_Task_Submission.md`**, already in your repository's `Module0-Foundation/Session2` folder since the Practical Guide's Exercise 1.
> Work in Kali, with the tools you set up in class.
> The deadline is **22:00 on the Saturday of the session's week**, and only what is on GitHub then counts.

> [!important] Everything here is required
> There are no optional tasks.

---

# Before You Start: Pull Your Repository

Your instructor's feedback on the Practical Guide arrives in your own repository, so pull it before you write anything:

```bash
cd ~/student-YOUR-USERNAME
git pull
```

Then open the worksheet in Obsidian: **Module0-Foundation**, then **Session2**, then **Module0_Session2_Home_Task_Submission.md**.

---

# Task 1: Write a Lab Card in Markdown

A **lab card** is a short page that describes your lab, the kind of note you keep so that you, or someone helping you, can see the whole lab at a glance.
You write it **directly into your worksheet**, in the space Task 1 marks, as Markdown that Obsidian renders.
Everything on it comes from your own Session 1 lab.

The card has exactly these six parts, in this order:

1. **A heading:** `### My Lab`, with a space after the three `#`.
2. **One sentence** saying what the lab is for, with one word in **bold**.
3. **A table** of your three machines, with the columns **Machine**, **Role** and **Address**.
   Take each address from the machine itself: `ip a` on Kali and Ubuntu, `ipconfig` on Windows.
   The table needs its delimiter row, and a blank line before and after it.
4. **A fenced code block** that opens with ` ```bash ` and holds the one command that shows Kali's address.
5. **A checklist** of three items, one per check from Session 1, each ticked (`- [x]`) if it passes on your lab today and left open (`- [ ]`) if it does not.
6. **A callout** of type `note`, holding one sentence: the first thing you would check if `ssh lab` stopped working.

When the card is written, press **Ctrl+E** and read it in the reading view.
The heading, table, code block, checklist and callout should each show as themselves, with no stray `#`, `|` or backticks.
**Then look past the card:** the worksheet's **Task 2** heading below it must still show as a heading.
If it has disappeared, a code block in your card is not closed.
The open block runs on until the next three backticks in the worksheet, so from there on, headings, questions and answer boxes are shown in the wrong form.
Press **Ctrl+E** again to go back to editing.

**Capture the evidence.**
With the reading view showing the whole card, press **Print Screen**, select the card, and save it as `task1-lab-card.png` in `Module0-Foundation/Session2/screenshots`.
Embed it in the worksheet where Task 1's evidence callout asks for it.

> [!example] Submission
> The card itself, written in the worksheet, and `task1-lab-card.png` showing it rendered.
> Then answer:
>
> - **Your screenshot's path is `screenshots/task1-lab-card.png`, not `/home/kali/student-YOUR-USERNAME/...`.**
>   Where is that path read from, and why would the full path show a broken image to your instructor even though it works on your machine?
> - **Your screenshot line starts with `!`.**
>   What would the same line show without the `!`?

**Commit**, from VS Code's built-in terminal (**Terminal**, then **New Terminal**, with your repository's folder open):

```bash
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: home task 1"
```

---

# Task 2: Correct a Broken Section

This section was typed to record one check, and it has **four mistakes**, one on each of the lines numbered below.
All four are common, and each changes what Obsidian and GitHub show.

````markdown
###Lab Checks

| Check | Result |
| Kali reaches Ubuntu | passed |

```bash
ping -c 1 10.0.2.5

![task1 lab card](screenshots/task1 lab card.png)
````

| Line | Text |
|---|---|
| 1 | `###Lab Checks` |
| 3–4 | the two table lines |
| 6 | ` ```bash ` |
| 9 | the image line |

1. **Find the four mistakes.**
   For each numbered line, say what is wrong and what Obsidian shows because of it.
2. **Write the corrected section directly into your worksheet**, in the space Task 2 marks.
   Keep its content, and change only what the four mistakes need.
   The image in it is your own `task1-lab-card.png`, so once the section is right, the picture appears.
3. **Check it in the reading view** with **Ctrl+E**: a heading, a two-row table, a code block holding only the `ping` line, and your lab card's picture below it.
   The worksheet's **Task 3** heading below it must still show as a heading: if it has disappeared, a code block in your section is not closed.

**Capture the evidence.**
Take a screenshot of the corrected section in the reading view and save it as `task2-fixed.png`.

> [!example] Submission
> The four mistakes, one per line, the corrected section written in the worksheet, and `task2-fixed.png`.
> Then answer:
>
> - **The mistake on line 6 broke more than its own line.**
>   What did it do to the rest of the section, and why does that make it the most expensive of the four in a worksheet?

**Commit:**

```bash
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: home task 2"
```

---

# Task 3: Hand It In and Confirm It Arrived

Your two commits are still only on your machine.

1. **Look at each screenshot once** before pushing: none may show a password, a key or a token.
2. **Push, then check**, in VS Code's built-in terminal:

   ```bash
   git push
   git status
   git log --oneline -3
   ```

   `git status` must say `Your branch is up to date with 'origin/main'.`
   If it says **ahead**, the push did not happen: read the error `git push` printed.
3. **Look at it the way your instructor will.**
   Open your repository on GitHub in Firefox, then **Module0-Foundation**, **Session2**, and your Home Task Submission.
   The card's table and checklist, the corrected section and both pictures should all show.

**Capture the evidence.**
Take a screenshot of the worksheet on GitHub showing the lab card and its picture, and save it as `task3-github.png`.

> [!example] Submission
> The output of the three commands, and `task3-github.png`.
> Then answer:
>
> - **The newest line of `git log --oneline` shows `(HEAD -> main, origin/main)`.**
>   What does each of the two names tell you, and what would it mean if `origin/main` were one line lower?
> - **You committed twice but pushed once.**
>   Until the push, who could see your two commits, and what would that have meant at 22:00 on Saturday?

**Commit, then push again.**
Filling in this task changed the worksheet after the push you just recorded, so it needs one more commit, `Module 0 Session 2: home task 3`, and one more `git push`.
Run `git status` once more: it must say **up to date**.

---

# What "done" looks like

- The lab card written in the worksheet, and rendering in the reading view
- The broken section's four mistakes named, and the corrected section rendering with its picture
- Three commits, one per task, all on GitHub
- Three screenshots: `task1-lab-card.png`, `task2-fixed.png`, `task3-github.png`
- Five short answers written, and the AI Assistance line filled in
- `git status` saying **up to date** after the last push
