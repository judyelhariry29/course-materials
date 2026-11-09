# Module 0 · Session 2 — Troubleshooting & FAQ

## The Working Environment and the Submission Workflow

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the sentence you would say out loud, or the first line of the error**, not the step you were on.
> The headings are written the way the problem sounds, and an error is quoted exactly as the terminal prints it, so you can search for it.
> Each entry gives the **cause** before the **fix**, so you learn what happened rather than only what to type.
>
> If nothing here matches, note **the exact step, the exact command and everything it printed**, and ask in the Telegram group.

## Contents

- [Markdown](#markdown)
- [Screenshots](#screenshots)
- [VS Code and installing](#vs-code-and-installing)
- [Committing](#committing)
- [Pushing and pulling](#pushing-and-pulling)
- [GitHub and SSH](#github-and-ssh)
- [Shared folders](#shared-folders)

---

# Markdown

### My heading shows the `#` signs as text

**Cause.**
There is no space after the `#` signs.
`#Results` and `###Lab Checks` are ordinary text, in Obsidian and on GitHub.

**Fix.**
Put one space after the last `#`: `# Results`, `### Lab Checks`.

### The stars around my bold word still show, or a number between stars went italic

**Cause.**
A pair of stars makes emphasis only when the stars touch the words inside them.
`** both**` has a space after the opening stars, so it stays as typed.
The opposite happens in `5*3*7`: the stars touch the `3`, so it becomes an italic 3 between the 5 and the 7.

**Fix.**
Close the gap for emphasis: `**both**`.
For a star you mean as a star, put a backslash in front of it: `5\*3\*7`.

### My list isn't a list

**Cause.**
Either the marker has no space after it, or the indentation is short.
`-check the network` is text.
An item under `1. Start Kali` indented by two spaces does not go inside the numbered item: it starts a second list.

**Fix.**
Put one space after the marker: `- check the network`.
Indent an item under a numbered item by **three spaces**, so that it starts under the item's first word:

```markdown
1. Start Kali
   - check the network
```

### A normal line of text turned into a big heading

**Cause.**
A line of `---` directly under a line of text turns that text into a heading, instead of drawing a divider below it.

**Fix.**
Leave a blank line between the text and the `---`.

### My table shows as lines full of `|`

**Cause.**
The **delimiter row** is missing.
Without the line of dashes under the header row, there is no table, and the lines show as text with their pipes.

**Fix.**
Put the delimiter row directly under the header row, with one cell of dashes per column:

```markdown
| Check | Result |
|---|---|
| Kali reaches Ubuntu | passed |
```

### Everything after my code block is shown as code, and headings have disappeared

**Cause.**
A code block was **opened and never closed**.
It does not stop at the end of its own line: it runs on until the **next three backticks anywhere below it**, and everything in between is shown as code.
In a worksheet, those next backticks usually open an answer box further down, so from the mistake onward headings disappear, and questions and answer boxes swap places.

**Fix.**
Find the block you opened last before the damage starts, and close it with three backticks on a line of their own.
Then check that the **next heading** below it shows as a heading again.

### Lines I wrote one under another run together on GitHub

**Cause.**
GitHub joins lines that follow each other into one paragraph.
Obsidian shows each line on its own, so the two disagree only about this.

**Fix.**
Leave a blank line between lines that must stay apart, such as `**Student Name:**` and `**Date:**`.

### My callout is a colored box in Obsidian, but a plain quote on GitHub

**Nothing is wrong.**
A callout with a title, such as `> [!example] Evidence — screenshot`, is Obsidian's own notation.
GitHub shows it as a quote, with `[!example]` and the title as ordinary text.
Everything inside it, the picture below it included, still shows.

---

# Screenshots

### My screenshot shows in Obsidian, but not on GitHub

**Cause.**
The image line works only on your machine.
GitHub, and the instructor who grades from it, read the line exactly as written, while Obsidian searches its whole vault for a file of that name.
There are three ways to get here:

- **An Obsidian embed**, `![[ex1.png]]`.
  GitHub shows it as the text `![[ex1.png]]`.
- **A path without the folder**, `![ex1](ex1.png)`.
  Obsidian finds the file in `screenshots` by its name, and GitHub looks next to the worksheet, where there is no such file.
- **A full path**, `![ex1](/home/kali/student-YOUR-USERNAME/...)`.
  That folder exists on your machine and nowhere else.

The course's grading check reports each of them as an incomplete submission, for example:

```
[Incomplete submission]
  evidence: Module0_Session2_Practical_Guide_Submission.md: image reference does not resolve: ex1.png
[Incomplete submission]
  evidence: Module0_Session2_Practical_Guide_Submission.md: Obsidian embed ![[ex1.png]] is not a standard image link and was not checked
```

**Fix.**
Write the standard image line, with the path from the worksheet's folder:

```markdown
![ex1](screenshots/ex1.png)
```

Then check the worksheet on github.com, where the grader sees it.

### Obsidian writes `![[...]]` when I paste or drag in an image

**Cause.**
Obsidian's link settings are still at their defaults, and its default is its own embed.

**Fix.**
In **Settings**, then **Files and links**, set these, as in the Practical Guide's setup:

- **Default location for new attachments**: *In subfolder under current folder*
- **Subfolder name**: `screenshots`
- **New link format**: *Path from current file*
- **Use \[\[Wikilinks\]\]**: off

The settings shape the links Obsidian writes from then on, so rewrite any `![[...]]` already in the worksheet by hand, as `![ex1](screenshots/ex1.png)`.

### My image line shows as text, not a picture

**Cause.**
The file name has a **space** in it.
The path stops at the space, so the line is not an image at all, even when a file of that exact name exists.

**Fix.**
Rename the file with no spaces, using `-` instead, and write the new name in the image line:

```bash
mv "screenshots/ex 1.png" screenshots/ex1.png
```

### My picture shows inside the evidence box

**Cause.**
The image line sits directly under the `[!example]` callout, so it is read as the callout's last line.

**Fix.**
Leave one blank line between the callout and the image line.
The blank line ends the callout.

### Print Screen does nothing

**Cause.**
On Kali's Xfce desktop, Flameshot's default way of taking the picture waits for a service that Xfce does not have, so nothing appears.

**Fix.**
Run `flameshot config`, and on the **General** tab tick **Use legacy X11 screenshot method (deprecated)**.
Press **Print Screen** again: the screen dims and a box lists Flameshot's keys.

### Print Screen opens a different screenshot window

**Cause.**
Xfce's own screenshot tool still has the key.

**Fix.**
In **Settings Manager**, then **Keyboard**, then **Application Shortcuts**, remove the row whose shortcut is **Print** on its own and whose command starts with `/usr/share/kali-themes/xfce4-s`.
Then add `flameshot gui` with the shortcut **Print**, as in the Practical Guide's setup.

### My screenshot saved into `Pictures`

**Cause.**
Flameshot's save window starts in `Pictures`, with a date and time as the name.

**Fix.**
Move it to the worksheet's `screenshots` folder, with the name the worksheet asks for:

```bash
mv ~/Pictures/2026-09-27_12-41.png ~/student-YOUR-USERNAME/Module0-Foundation/Session2/screenshots/ex1.png
```

Next time, change the folder and the name in the save window before clicking **Save**.

---

# VS Code and installing

### VS Code says *Restricted Mode* across the top

**Cause.**
Every folder VS Code has not seen before opens in **Restricted Mode**, which switches off the features that could run code from the folder: its tasks, its settings, and extensions that have not declared themselves safe there.

**Fix.**
Click **Manage** in the banner, then **Trust**.
Do this only for a folder you made yourself or got from the course, because in a trusted folder the folder's own settings and tasks can run.

### `git status` says nothing changed, but I edited the file

**Cause.**
The file is **not saved**.
VS Code does not save on its own, and a dot on the file's tab means unsaved changes.
Git sees only what is on disk.

**Fix.**
Save with **Ctrl+S**, then run `git status` again.
Obsidian saves as you type, so this happens in VS Code, not in Obsidian.

### `Error: Couldn't find any package by glob 'code.deb'`

```
Error: Couldn't find any package by glob 'code.deb'
```

**Cause.**
`apt` reads a bare name as the name of a package to download, not as a file, and there is no package called `code.deb`.

**Fix.**
Give the file's path, starting with `./` when you are in its folder:

```bash
sudo apt install ./code.deb
```

Do not switch to `apt-get` to get past the error.
`apt-get` treats a name it cannot find as a pattern, and can install a different package whose name happens to match.

### The install ended with a *Notice* about *Permission denied*

```
Notice: Download is performed unsandboxed as root as file '/home/kali/Downloads/code_1.139.1-1790309529_amd64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
```

**Nothing is wrong.**
`apt` first tries to read the file as its own restricted user, `_apt`, which cannot open your `Downloads` folder.
It then reads it as root and installs it, and the notice reports only the first attempt.
Check the installation itself: `dpkg-query -W code` lists it with its version.

---

# Committing

### `Author identity unknown`

```
$ git commit -m "Module 0 Session 1: exercise 3"
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'kali@kali.(none)')
```

**Cause.**
Git writes a name and an email on every commit, and none are set on this machine.
Nothing was committed.

**Fix.**
Set them once, with your own name and email in place of the examples, then commit again:

```bash
git config --global user.name "Omar Khaled"
git config --global user.email "omar.khaled@example.com"
git config --global pull.rebase true
git commit -m "Module 0 Session 1: exercise 3"
```

The third line belongs to the same one-time setup, and the pull entries below explain it.
A commit that worked names its ID on the first line:

```
[main 7481e68] Module 0 Session 1: exercise 3
 1 file changed, 1 insertion(+)
```

### `no changes added to commit`

```
$ git commit -m "Module 0 Session 1: exercise 3"
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   Module0-Foundation/Session1/Module0_Session1_Practical_Guide_Submission.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**Cause.**
The file changed, but it was not **added**, so the commit had nothing to hold.
Git printed the status instead, and nothing was committed.

**Fix.**
Add the session's folder, then commit:

```bash
git add Module0-Foundation/Session1
git commit -m "Module 0 Session 1: exercise 3"
```

### `nothing added to commit but untracked files present`

```
$ git commit -m "Module 0 Session 2: exercise 1"
On branch main
Your branch is ahead of 'origin/main' by 2 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Module0-Foundation/Session2/

nothing added to commit but untracked files present (use "git add" to track)
```

**Cause.**
The same mistake, with a new folder.
Git has never recorded anything in `Module0-Foundation/Session2/`, so it lists it as **untracked** and commits nothing.

**Fix.**

```bash
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: exercise 1"
```

### `git commit` opened a screen full of lines starting with `#`

At the top of the terminal:

```
  GNU nano 9.2    /home/kali/student-YOUR-USERNAME/.git/COMMIT_EDITMSG

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
```

And at the bottom:

```
^G Help      ^O Write Out ^F Where Is  ^K Cut       ^T Execute   ^C Location
^X Exit      ^R Read File ^\ Replace   ^U Paste     ^J Justify   ^/ Go To Line
```

**Cause.**
The commit was run **without `-m`**, so Git opened the editor **nano** for you to write the message in.
Your Kali may show a different version number.
`^` means **Ctrl**.

**Fix.**
Type the message on the empty first line, then:

1. **Ctrl+O** to save.
   nano shows the file's name at the bottom.
   Press **Enter** to keep it.
2. **Ctrl+X** to leave.

Git finishes the commit as soon as nano closes:

```
[main 3e81ecf] Module 0 Session 2: home task 2
 1 file changed, 1 insertion(+), 1 deletion(-)
```

If you pressed **Ctrl+X** first, nano asks:

```
Save modified buffer?
 Y Yes
 N No           ^C Cancel
```

Press **Y**, then **Enter** to keep the file's name.
Next time, give the message on the command line with `-m "..."`, and nano never opens.

### `Aborting commit due to empty commit message.`

```
$ git commit
Aborting commit due to empty commit message.
```

**Cause.**
nano was closed without a message saved in it, so Git canceled the commit.
Your changes are still added and waiting.

**Fix.**
Commit again with the message on the command line:

```bash
git commit -m "Module 0 Session 2: home task 2"
```

### The commit says `create mode 100755`

```
[main c46b5b9] Module 0 Session 2: home task
 1 file changed, 1 insertion(+)
 create mode 100755 Module0-Foundation/Session2/Module0_Session2_Home_Task_Submission.md
```

**Cause.**
`100755` means Git recorded the file as a **program**, because it was marked executable.
Every file copied out of a VirtualBox shared folder is, unless it is copied with `--no-preserve=mode`.
A worksheet is not a program, and `100644` is right for it.

**Fix.**
Take the executable mark off, then commit the change:

```bash
chmod 644 Module0-Foundation/Session2/*.md
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: worksheets are not programs"
```

```
[main 44f559e] Module 0 Session 2: worksheets are not programs
 1 file changed, 0 insertions(+), 0 deletions(-)
 mode change 100755 => 100644 Module0-Foundation/Session2/Module0_Session2_Home_Task_Submission.md
```

For screenshots copied the same way, run the same `chmod 644` on `screenshots/*`.

---

# Pushing and pulling

### `git status` says my branch is ahead of `origin/main`

```
$ git status
On branch main
Your branch is ahead of 'origin/main' by 3 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**Cause.**
The work is committed, and the commits are **only on your machine**.
*Nothing to commit* is true and does not mean handed in: GitHub does not have these three commits, and only GitHub's copy is graded.

**Fix.**

```bash
git push
git status
```

The status must end with `Your branch is up to date with 'origin/main'.`

### `git push` says `Everything up-to-date`, but GitHub doesn't have my work

```
$ git push
Everything up-to-date
```

**Cause.**
There is no commit to send.
The work was never committed, never added, or, in VS Code, never saved.

**Fix.**
Run `git status` and follow what it says.
A file listed as modified or untracked goes through `git add` and `git commit`, and then `git push`.

### `fatal: not a git repository`

```
$ git status
fatal: not a git repository (or any of the parent directories): .git
```

**Cause.**
Git was run **outside your repository**.
Git commands work only inside a repository's folder, or a folder below it.
In VS Code, open the repository's folder, not a single file, so that the built-in terminal starts inside it.

**Fix.**

```bash
cd ~/student-YOUR-USERNAME
git status
```

### `git push` says `! [rejected]`

```
$ git push
To github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

**Cause.**
GitHub has a commit your machine does not.
Almost always, a file was edited on github.com, or the work was pushed from another machine.
Git refuses to push, because the push would throw that commit away.

**Fix.**
Pull, then push:

```bash
git pull
git push
```

```
Successfully rebased and updated refs/heads/main.
```

The pull puts GitHub's commit under yours, and the push then goes through.
To keep this from happening, edit your worksheets only on Kali, never on github.com.

### `fatal: Need to specify how to reconcile divergent branches.`

```
$ git pull
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 295 bytes | 295.00 KiB/s, done.
From github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME
   44f559e..decc826  main       -> origin/main
hint: You have divergent branches and need to specify how to reconcile them.
hint: You can do so by running one of the following commands sometime before
hint: your next pull:
hint:
hint:   git config pull.rebase false  # merge
hint:   git config pull.rebase true   # rebase
hint:   git config pull.ff only       # fast-forward only
hint:
hint: You can replace "git config" with "git config --global" to set a default
hint: preference for all repositories. You can also pass --rebase, --no-rebase,
hint: or --ff-only on the command line to override the configured default per
hint: invocation.
fatal: Need to specify how to reconcile divergent branches.
```

**Cause.**
`pull.rebase true`, from the one-time Git setup, is not set on this machine.
Both GitHub and your machine have new commits, and Git will not choose how to combine them for you.

**Fix.**
Set it once, then pull again:

```bash
git config --global pull.rebase true
git pull
```

Do not pick the `false` line from the hints: it opens nano for a merge message and adds an extra commit to your history.

### `CONFLICT (content): Merge conflict in ...`

```
$ git pull
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 5 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
Unpacking objects: 100% (5/5), 449 bytes | 224.00 KiB/s, done.
From github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME
   9826100..82cba29  main       -> origin/main
Auto-merging Module0-Foundation/Session1/Module0_Session1_Practical_Guide_Submission.md
CONFLICT (content): Merge conflict in Module0-Foundation/Session1/Module0_Session1_Practical_Guide_Submission.md
error: could not apply 0acfbc9... Module 0 Session 1: exercise 3, A3 reworded
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
hint: Disable this message with "git config set advice.mergeConflict false"
Could not apply 0acfbc9... # Module 0 Session 1: exercise 3, A3 reworded
```

**Cause.**
The **same lines** of the same file were changed on github.com and on your machine, and Git cannot tell which version you want.
The pull stopped halfway, and `git status` now begins with `interactive rebase in progress`.

**Fix.**
Put everything back as it was before the pull:

```bash
git rebase --abort
git status
```

```
On branch main
Your branch and 'origin/main' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" if you want to integrate the remote branch with yours)

nothing to commit, working tree clean
```

Your commit is safe, and nothing is lost.
Do not try the other hints: this course does not cover combining two versions by hand.
Post the output of `git status` in the Telegram group, and your instructor will help you finish.

### `error: cannot pull with rebase: You have unstaged changes.`

```
$ git pull
error: cannot pull with rebase: You have unstaged changes.
error: Please commit or stash them.
```

**Cause.**
A file in this repository has changes that are not committed, and the pull refuses to run over them.
Where it happens decides the fix.

**Fix, in `course-materials`.**
You filled in a worksheet inside `course-materials` instead of in your own repository.
`course-materials` is read-only for you, so work there can never be handed in.
Copy the worksheet into your repository first, then throw away the changes in `course-materials` and pull:

```bash
cp ~/course-materials/Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md ~/student-YOUR-USERNAME/Module0-Foundation/Session2/
cd ~/course-materials
git restore .
git pull
```

Copy only the worksheet you filled in, because `cp` replaces a file of the same name in your repository without asking.
`git restore .` throws away every change in `course-materials`, which is what you want there and nowhere else.

**Fix, in your own repository.**
Commit your work first, then pull:

```bash
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: exercise 3"
git pull
```

---

# GitHub and SSH

### `git@github.com: Permission denied (publickey).`

```
$ ssh -T git@github.com
git@github.com: Permission denied (publickey).
```

A clone, pull or push shows the same line, followed by:

```
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

**Cause.**
GitHub does not have the public key of the key pair on this machine.
The key was never added in GitHub's settings, a different key was added, or the key pair on Kali was made again after it was added.

**Fix.**
Compare the fingerprint of your key with the list in GitHub's **Settings**, then **SSH and GPG keys**:

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

If it is not in the list, add the contents of `~/.ssh/id_ed25519.pub` there, as in the Practical Guide's setup.
Then `ssh -T git@github.com` again.

### `ssh -T` says GitHub does not provide shell access, so did it fail?

```
$ ssh -T git@github.com
Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

**It worked.**
That line is GitHub's success message: it recognized your key and your username.
GitHub accepts keys for Git only, so it closes the connection, and `ssh` reports that as a failure to the shell.
Nothing needs fixing.

### `The authenticity of host 'github.com' can't be established`

**Cause.**
This is your machine's first connection to GitHub, so it has no record of GitHub's identity yet.
It asks once, then remembers.

**Fix.**
Compare the fingerprint it shows with GitHub's published one before typing `yes`.
GitHub's ED25519 fingerprint was `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` on 2026-09-27, and GitHub's documentation lists the current value.
**If they do not match, type `no`** and ask in the Telegram group.
**If it ever asks again on the same machine, stop and find out why**, because the machine answering may not be GitHub.

### `ERROR: Repository not found.`

```
$ git clone git@github.com:Professional-Training-Cybersecurity-I/student-omar-khaled.git
Cloning into 'student-omar-khaled'...
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

**Cause.**
Your key works, and GitHub has no repository at that address **that you can see**.
The name is mistyped, which is the usual case, or you have not accepted the organization's invitation yet, or your instructor has not given you access to your repository yet.
A private repository you cannot see is reported exactly as one that does not exist.

**Fix.**
Copy the address from your repository's page instead of typing it: **Code**, then **SSH**.
It ends in `student-` followed by your GitHub username, spelled exactly as GitHub shows it.
If the page itself shows *404 This is not the web page you are looking for*, see the next entry.

### The course pages show *404 This is not the web page you are looking for*

**Cause.**
You are not a member of the organization yet: the invitation has not been accepted, or it has not been sent.
GitHub shows a private page you cannot open as a page that does not exist.
If `course-materials` opens and only your own repository shows 404, you are a member already, and your instructor has not given you access to your repository yet.

**Fix.**
Accept the invitation in the email from GitHub, or at `https://github.com/orgs/Professional-Training-Cybersecurity-I/invitation`.
If there is no invitation, ask in the Telegram group, with your GitHub username exactly as your profile page shows it.
If only your own repository shows 404, do not accept anything again: it opens once your instructor gives you access.
If it still shows 404 when the session starts, ask in the Telegram group.

### `Username for 'https://github.com':`

```
$ git clone https://github.com/Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
Cloning into 'student-YOUR-USERNAME'...
Username for 'https://github.com':
```

**Cause.**
You copied the **HTTPS** address.
It asks for a username and password, and your GitHub password does not work there: only your SSH key does, on the SSH address.

**Fix.**
Press **Ctrl+C**.
On the repository's page, choose **Code**, then **SSH**, and clone with the address that starts with `git@github.com:`.

### `fatal: destination path '...' already exists and is not an empty directory.`

```
$ git clone git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
fatal: destination path 'student-YOUR-USERNAME' already exists and is not an empty directory.
```

**Cause.**
The repository is **already cloned**, into the folder it names.
A clone is made once per machine.

**Fix.**
Use the copy you have, and bring it up to date instead of cloning again:

```bash
cd ~/student-YOUR-USERNAME
git pull
```

---

# Shared folders

### `ls` says `Permission denied` on `/media/sf_...`

**Cause.**
Your Kali user is not in the group that is allowed to read shared folders, `vboxsf`.

**Fix.**

```bash
sudo usermod -aG vboxsf $USER
```

Log out of Kali and back in, which is when a new group takes effect, and `ls` again.

### Files I copied from a shared folder are committed as `100755`

**Cause.**
Every file in a shared folder looks executable to Kali, and `cp` keeps that mark unless told not to.

**Fix.**
Copy with `--no-preserve=mode`:

```bash
cp --no-preserve=mode /media/sf_session1/Module0_Session1_*_Submission.md Module0-Foundation/Session1/
```

For files already committed that way, see *The commit says `create mode 100755`* above.
