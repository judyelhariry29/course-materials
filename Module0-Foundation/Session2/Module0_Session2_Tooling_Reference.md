# Module 0 · Session 2 — Tooling Reference

## The Working Environment and the Submission Workflow

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session used each of these tools for one job in the submission cycle.
> **This is the fuller treatment**, so that when you need one of them for something the session did not cover, you are reading a reference rather than searching.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Everything below runs **inside Kali**, where the tools are installed.
> Wherever a command says **`YOUR-USERNAME`**, type your GitHub username.

---

# Markdown

Every worksheet in this course is a Markdown file.
You type the **source**, plain text with a few marks in it, and a program such as Obsidian or GitHub shows the **rendered view**, where the marks have become headings, lists and pictures.
The file itself is only ever the source, which is why any program can open it.

## Paragraphs and line breaks

**A blank line ends a paragraph.**
Lines with no blank line between them belong to the same paragraph.

**Obsidian and GitHub treat a single line break differently.**
Obsidian shows it as a new line.
GitHub joins the lines into one paragraph.
This course writes **one sentence per line**, which reads as clean lines in Obsidian and as a normal paragraph on GitHub.
Never break a sentence across two lines: Obsidian shows it cut in half.

## Headings

```markdown
# Top level
## Second level
### Third level
```

The `#` marks need **a space after them**.
`###Lab Checks` is not a heading: both Obsidian and GitHub show it as the text you typed.

## Emphasis, and escaping a mark

```markdown
**bold**   *italic*   `code`
```

The marks must **touch the word**: `** bold**` shows its stars instead of making anything bold.
To show a mark itself, put a backslash before it: `\*` shows a star, `\#` a hash.

## Lists and checkboxes

```markdown
- an item
- another item
  - nested: two spaces, under the text of the item above

1. a numbered item
2. the next one
   - nested: three spaces, under the text of `1. `

- [ ] a checkbox, open
- [x] a checkbox, ticked
```

A dash or a number followed by **a space** starts an item.
A nested item lines up with the **text** of the item above it, not with its marker.

## Code

A span inside a sentence takes one backtick on each side: `` `git status` `` shows `git status`.
A block takes three backticks on a line of their own, above and below, and the word after the opening three chooses the coloring:

````markdown
```bash
git status
```
````

**Always close a block.**
A block left open runs on until the next three backticks anywhere below it, and everything in between, headings and pictures included, is shown as code.
In a worksheet, those next three backticks are usually an answer box further down, so from the mistake onward the worksheet's headings disappear and its questions and boxes swap places.
If a heading below your text has vanished in the reading view, look for an open block above it.

## Links and images

```markdown
[the course materials](https://github.com)
![ex1-session-folder](screenshots/ex1-session-folder.png)
```

**One character apart.**
The `!` makes the same line show the picture instead of a link to it.
The text in brackets is the **alternative text**, shown when the picture cannot be.

**The path is read from the folder the worksheet is in.**
`screenshots/ex1-session-folder.png` means *the `screenshots` folder beside this file*, which is true on your machine, on GitHub, and on your instructor's machine.
A full path such as `/home/kali/...` is true only on your own machine.

**No spaces in file names.**
`![a](screenshots/task1 lab card.png)` is not an image at all: Obsidian and GitHub both show the line as text, even when a file of exactly that name exists.

## Tables

```markdown
| Machine | Role | Address |
|---|---|---|
| Kali | workstation | 10.0.2.4 |
```

The second row, the **delimiter row**, is what makes the first one a header, and without it there is no table.
The pipes do not need to line up.
Leave a blank line before and after a table.

**Never put a table inside a list item.**
Obsidian's editing view shows it as raw pipes, so write the rows as a nested list instead:

```markdown
2. Set these:
   - **Subfolder name**: `screenshots`
   - **New link format**: Path from current file
```

## Quotes, callouts and dividers

```markdown
> A quote.

> [!note] A callout's title
> A callout is a quote whose first line names its type.

---
```

The course's worksheets use four callout types: `note`, `important`, `warning` and `example`.
A divider is `---` on its own line, with a blank line above and below: directly under a line of text, `---` turns that text into a heading instead.

**On GitHub, a callout is an ordinary quote.**
Only Obsidian draws the colored box.
GitHub shows a titled callout as a quote whose first line reads `[!example] Evidence — screenshot`, as text.
That is expected, and nothing in the worksheet is broken.

## Where Obsidian and GitHub differ

| You type | Obsidian shows | GitHub shows |
|---|---|---|
| two lines with no blank line between | two lines | one paragraph |
| `> [!note] Title` | a colored callout box | a quote beginning `[!note] Title` |
| `![[image.png]]` | the picture | the text `![[image.png]]` |
| `[[Some Name]]` in a sentence | a link to a note | the text `[[Some Name]]` |
| a table inside a list item | raw pipes, while editing | a table |

**Grade by the right-hand column.**
Your worksheet is read on GitHub, so something that shows only in Obsidian is missing for grading.
To write double brackets as text, escape them: `\[\[Wikilinks\]\]`.

---

# Obsidian

## A vault is a folder

Obsidian opens a **vault**, which is an ordinary folder.
Every note is a plain `.md` file in it, and nothing is imported or converted.
Your vault is your repository's folder, so a worksheet you fill in is already where Git can hand it in.

Obsidian keeps its own settings in a hidden `.obsidian` folder inside the vault.
Your repository's `.gitignore` lists that folder, so it never reaches GitHub.

## The five link settings

**Settings**, then **Files and links**:

- **Default location for new attachments**: *In subfolder under current folder*
- **Subfolder name**: `screenshots`
- **New link format**: *Path from current file*
- **Automatically update internal links**: on
- **Use \[\[Wikilinks\]\]**: off

Together they make a pasted picture land in the `screenshots` folder beside the note you pasted it into, with a standard link that GitHub shows.

## Keys worth knowing

| Key | What it does |
|---|---|
| **Ctrl+E** | switch between editing and the reading view |
| **Ctrl+O** | open a note by typing part of its name |
| **Ctrl+P** | the command palette: every command, by name |
| **Ctrl+V** | paste, including a picture from the clipboard |

**Obsidian saves as you type.**
There is no Save button, and nothing to remember before a commit.

---

# VS Code

## Opening a folder

```bash
code ~/student-YOUR-USERNAME     # open your repository
code .                           # open the folder the terminal is in
```

VS Code opens a **folder**, not a single file, and its Explorer lists everything in it.

## Restricted Mode and trust

A folder VS Code has not seen before opens in **Restricted Mode**, with a banner across the top.
**Manage**, in that banner, then **Trust**, trusts the folder.
Trusting it lets VS Code run the folder's tasks, apply its settings, run the debugger and activate every extension, so a folder from anywhere else can run code on your machine the moment you trust it.
**Trust only folders you made or got from the course.**

## The built-in terminal

**Terminal**, then **New Terminal**, opens a terminal **in the folder VS Code opened**.
Commands typed there act on that folder, so `git` works without a `cd`.

## Saving

**VS Code does not save as you type.**
A dot on a file's tab means it has unsaved changes, and Git sees only what is saved.
Press **Ctrl+S** before you commit.

## Extensions

```bash
code --install-extension ms-python.python   # install by identifier
code --list-extensions                      # what is installed
```

An extension's **name** is not unique, and look-alikes exist.
Its **identifier**, `publisher.name`, is.
Check the identifier and the publisher's verified mark before installing, because an extension runs with your permissions and can read your files.

## Keys worth knowing

| Key | What it does |
|---|---|
| **Ctrl+S** | save |
| **Ctrl+P** | open a file by typing part of its name |
| **Ctrl+Shift+P** | the command palette |
| **Ctrl+Shift+X** | the Extensions view |
| **Ctrl+\`** | show or hide the terminal |

---

# Flameshot

```bash
flameshot gui        # start a capture: what the Print Screen key runs
flameshot config     # open the settings
```

## The setting Kali's desktop needs

On Kali's Xfce desktop, Flameshot's default capture method waits for a service Xfce does not provide, and gives up after 30 seconds without capturing anything.
**Use legacy X11 screenshot method (deprecated)**, on the **General** tab of `flameshot config`, makes it capture directly.
The setting is stored in `~/.config/flameshot/flameshot.ini`.

## Capturing

Pressing Print Screen dims the screen and shows a box listing Flameshot's keys.
Drag across the region you want, draw a box around the line that proves your result, then press **Ctrl+S** to save.
**Esc** leaves without capturing.

**Save it where the worksheet looks.**
The save window starts in `Pictures`, with a date and time as the name.
Change both: the session's `screenshots` folder, and the name the worksheet's slot gives, without spaces.

> [!warning] Never capture a key, a password or a token
> A screenshot pushed to GitHub is published, and Git keeps it in the history even after you delete the file.

---

# Installing software: `apt` and `dpkg`

```bash
sudo apt update                          # refresh the list of available packages
sudo apt install -y flameshot            # install from Kali's repository
sudo apt install ~/Downloads/code_*_amd64.deb   # install a downloaded .deb
sudo apt full-upgrade                    # bring every installed package up to date
apt list --upgradable                    # what an upgrade would change
sudo apt remove flameshot                # uninstall
dpkg-query -W git code flameshot obsidian   # which of these are installed, and their versions
```

**A downloaded `.deb` needs a path.**
Without one, `apt` reads the name as a package to find in the repository, and stops:

```
Error: Couldn't find any package by glob 'code.deb'
```

`./code.deb` or `~/Downloads/code_*_amd64.deb` tells `apt` it is a file.
Use `apt`, as this course does, not the older `apt-get`: given the same bare name, `apt-get` reads it as a pattern and can install a different package whose name happens to match.

**Installing a package that is already installed is safe.**
`apt` says so in one line and changes nothing:

```
git is already the newest version (1:2.53.0-1).
```

**Installing a file from your home folder ends with a notice**, which is not an error:

```
Notice: Download is performed unsandboxed as root as file '/home/kali/Downloads/code_1.139.1-1790309529_amd64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```

`apt` first tries to read the file as a restricted helper user, which cannot open your home folder, and then reads it as the administrator.
The install succeeded.

**`dpkg-query -W`** lists each installed package with its version, one per line, in alphabetical order:

```
code	1.139.1-1790309529
flameshot	14.0.0-4
git	1:2.53.0-1
obsidian	1.13.7
```

> [!warning] A `.deb` runs its install scripts as the administrator
> Download one only from its maker's own site, never from a search result or an advertisement.

---

# Git

This course uses Git for one job: handing in work.
**Branches, merges and conflicts are left out on purpose**, and nothing below needs them.

## The one-time settings

```bash
git config --global user.name "Omar Khaled"
git config --global user.email "omar.khaled@example.com"
git config --global pull.rebase true
git config --global --list      # all your settings
git config user.name            # one of them
```

`git config user.name` prints one value:

```
Omar Khaled
```

`--global` stores them for your Kali user, in `~/.gitconfig`.
`pull.rebase true` is what lets `git pull` continue when both GitHub and your machine have new commits, by placing yours after GitHub's.

## Where things stand: `git status`

`git status` changes nothing, so run it whenever you are unsure.
Its three common answers, from a real worksheet:

**Nothing to do:**

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Edited, and a new file Git has never seen:**

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Module0-Foundation/Session2/screenshots/ex5-github.png

no changes added to commit (use "git add" and/or "git commit -a")
```

**Added, and ready to commit:**

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md
	new file:   Module0-Foundation/Session2/screenshots/ex5-github.png
```

**Committed but not pushed** reads `Your branch is ahead of 'origin/main' by 1 commit.`
Until you push, GitHub does not have it.

## Seeing a change before you commit it: `git diff`

```bash
git diff                   # what you changed and have not added
git diff --staged          # what you added, which is what the next commit will hold
git diff --staged --stat   # the same, as one line per file
```

`git diff` shows each changed line, the old one with `-` and the new one with `+`:

```
diff --git a/Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md b/Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md
index eec2f4a..7407096 100644
--- a/Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md
+++ b/Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md
@@ -6,7 +6,7 @@
 
 **Student Name:** Omar Khaled
 
-**Date:** 2026-09-27
+**Date:** 2026-09-28
 
 ---
 
```

**After `git add`, `git diff` prints nothing**, because the change is no longer unadded.
`git diff --staged --stat` then shows what the commit will take:

```
 .../Module0_Session2_Practical_Guide_Submission.md     |   2 +-
 Module0-Foundation/Session2/screenshots/ex5-github.png | Bin 0 -> 152500 bytes
 2 files changed, 1 insertion(+), 1 deletion(-)
```

A screenshot is shown as `Bin`, for binary: Git can say that it changed, not how.

## Undoing before a commit: `git restore`

```bash
git restore --staged <file>   # take a file back out of the next commit; your edit stays
git restore <file>            # throw away your edit, back to the last commit
```

**`--staged` is the safe one.**
It only takes the file out of what `git add` chose, and the file on disk is untouched.
Unstaging a new screenshot puts it back under *Untracked files*.

> [!warning] `git restore <file>` cannot be undone
> It replaces the file on disk with its last committed version.
> An edit you had not committed is gone, and Git has no copy of it.

Neither command prints anything when it works.
Run `git status` afterward to see the result.

## Committing

```bash
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: exercise 3"
```

**Add the session folder, not everything.**
`git add .` in the repository's top folder also takes anything else lying there.

**Always give `-m` a message.**
Without it, Git opens the **nano** editor for one.
Type the message on the first line, then **Ctrl+O**, **Enter** and **Ctrl+X** to save and leave.

## History: `git log`

```bash
git log --oneline       # one line per commit, newest first
git log --oneline -3    # only the newest three
git log -1              # the newest commit, in full
```

```
f5e9418 (HEAD -> main, origin/main, origin/HEAD) Module 0 Session 2: exercise 4
ccae9dc Module 0 Session 2: exercise 3
17dc420 Module 0 Session 2: exercises 1 and 2
```

**`HEAD -> main`** marks where you are: the newest commit on your machine.
**`origin/main`** marks the newest commit GitHub has, as of your last push or pull.
On the same line, GitHub has everything.
When `origin/main` sits lower, the commits above it are not on GitHub yet.

`git log -1` adds the full hash, the author and the date:

```
commit f5e9418d5577df7451390934a14c8386b55ea788 (HEAD -> main, origin/main, origin/HEAD)
Author: Omar Khaled <omar.khaled@example.com>
Date:   Sun Sep 27 19:05:44 2026 +0000

    Module 0 Session 2: exercise 4
```

## Remotes: `clone`, `push`, `pull`

```bash
git clone git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
git push          # send your commits to GitHub
git pull          # bring GitHub's new commits to your machine
git remote -v     # which address this repository pushes to
```

`git remote -v` must show the **SSH** address, starting `git@github.com:`:

```
origin	git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git (fetch)
origin	git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git (push)
```

A repository cloned with the `https://` address asks for a username and cannot use your key.
Switch it to SSH without cloning again:

```bash
git remote set-url origin git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
```

**Pull before you start work, push before the deadline.**
Only what is on GitHub at 22:00 on the Saturday of the session's week counts.

## Run it inside the repository

Every Git command acts on the repository that contains the folder you are in.
Anywhere else, it stops:

```
fatal: not a git repository (or any of the parent directories): .git
```

`cd ~/student-YOUR-USERNAME`, or open a new terminal in VS Code, and run it again.

---

# SSH for GitHub

GitHub uses the same key pair you made in Session 1 for the lab server.
It stores your **public** key, and every clone, push and pull proves you hold the matching **private** key.

```bash
cat ~/.ssh/id_ed25519.pub          # the public half: this is what you paste into GitHub
ssh -T git@github.com              # does GitHub accept this machine's key?
ssh -vT git@github.com             # the same, printing each step, including which key was offered
ssh-keygen -lf ~/.ssh/id_ed25519.pub   # your key's fingerprint, to match against GitHub's list
```

**The public key goes in GitHub's Settings, then SSH and GPG keys.**
GitHub has no shell for `ssh-copy-id`, so it is pasted into that page instead.
The private key, `~/.ssh/id_ed25519` without `.pub`, never leaves your machine.

**Success is a greeting:**

```
Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

**Failure is one line:**

```
git@github.com: Permission denied (publickey).
```

It means GitHub does not have the public key of the private key this machine offered.
The message came from GitHub, so the network works: the problem is the key alone.
`ssh -vT git@github.com` shows which key file was offered, which settles whether it is the one you pasted.

**The first connection asks you to accept GitHub's host key**, and answering `yes` stores it in `~/.ssh/known_hosts`.
Compare the fingerprint it shows with GitHub's published one before typing `yes`.
GitHub's ED25519 fingerprint was `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` on 2026-09-27, and GitHub's documentation lists the current value.
**If it ever asks again on the same machine, stop and find out why**, because the machine answering may not be GitHub.

---

# VirtualBox shared folders

A **shared folder** shows a folder of your computer, the **host**, inside Kali, at `/media/sf_` followed by the name you give it.
In the Kali machine's window: **Devices**, **Shared Folders**, **Shared Folders Settings**.

| Setting | What it does |
|---|---|
| **Folder Path** | the folder on the host |
| **Folder Name** | the name after `/media/sf_` in Kali |
| **Read-only** | Kali can read the files but never change them |
| **Auto-mount** | it appears in Kali at once, without a command |
| **Make Permanent** | it survives Kali shutting down: leave it off for a one-time copy |

**`Permission denied` on `/media/sf_...`** means your Kali user is not in the group allowed to read shared folders:

```bash
sudo usermod -aG vboxsf $USER    # then log out of Kali and back in
```

**Copy with `--no-preserve=mode`.**
Every file in a shared folder looks executable to Kali, and a plain `cp` keeps that, so Git would record your worksheets as programs:

```bash
cp --no-preserve=mode /media/sf_session1/Module0_Session1_*_Submission.md Module0-Foundation/Session1/
```

**Remove the shared folder once the copy is done.**
A lab machine has no reason to see your own computer's files.
