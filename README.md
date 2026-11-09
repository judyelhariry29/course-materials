# Professional Training in Cybersecurity I — Course Materials

Everything the course hands out lives here, one folder per session.

**This repository is read-only for you.**
Pull it, never push to it, and never fill anything in here.

When a document changes, `git pull` brings you the new version, which is why documents are never sent as files in chat.

## What a session folder holds

| File ending | What it is |
|---|---|
| `_Presentation.pdf` | the session's slides |
| `_Practical_Guide.md` | the session's exercises, step by step |
| `_Home_Task.md` | the home task, done on your own |
| `_Tooling_Reference.md` | every tool the session uses, in full, for looking things up |
| `_Troubleshooting_FAQ.md` | problems listed by what you see, each with its cause and its fix |
| `_Practical_Guide_Submission.md`, `_Home_Task_Submission.md` | the two blank worksheets you fill in and hand in |

## Starting a session

Your instructor puts each session's guide, home task and two blank worksheets into your own repository, in a folder with the same path the session has here.
Start every session by pulling both repositories.
For Module 0 Session 2:

```bash
cd ~/course-materials
git pull
cd ~/student-YOUR-USERNAME
git pull
ls Module0-Foundation/Session2
```

Open the guide and its worksheet side by side in Obsidian, from your own repository.
The presentation, the Tooling Reference and the Troubleshooting FAQ stay here, so read them in this folder.
Fill in only the worksheets, and never edit, move or delete the guide or the home task in your repository, because your instructor's fixes arrive in them through `git pull`.
Keep the session's folder exactly where it is, because the grader finds your work by its path.
The README of your own repository says how to hand them in, and both are due by **22:00 on the Saturday of the session's week**.

> [!warning]
> **Never fill in a worksheet here.**
> Work done inside this repository can never be handed in.
> Your next `git pull` here also stops, with `error: cannot pull with rebase: You have unstaged changes.`
> The session's Troubleshooting FAQ shows how to move the work to your own repository and recover.
