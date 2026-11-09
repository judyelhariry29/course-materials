# Module 0 · Session 2 — Practical Guide

## The Working Environment and the Submission Workflow

### Professional Training in Cybersecurity I

---

## Overview

This guide sets up the place you will work in for the rest of the course, inside Kali, and then carries your first real work all the way to GitHub.
By the end you will have:

1. **Four tools installed in Kali:** Obsidian, VS Code, Flameshot and Git
2. **Git set up once**, so your name is on every commit and a pull behaves predictably
3. **Your SSH key on GitHub**, proven with one command
4. **Two repositories on your machine:** the course's materials, and your own
5. **Obsidian and VS Code set up** for the way this course uses them
6. **This session's worksheet and your Session 1 worksheets pushed** to your own repository

**We do this together in the session, and you finish whatever is left at home.**
The guide is written to be picked up from wherever you stopped, by somebody working alone.

> [!example] Submission
> Your worksheet is **`Module0_Session2_Practical_Guide_Submission.md`**.
> It arrives on your machine in Exercise 1, when you clone the course's repository, so the setup steps before it have no **Record** box: each ends with a **Checkpoint** instead, and Exercise 4 records all of them at once with commands you can run at any time.

> [!important] You must complete
> All of it.
> Every later session starts with a pull and ends with a push, so a step missing here stops every submission after it.

> [!important] Work in this order
> Each part needs the one before it.
> GitHub has to accept your key before you can clone, and your worksheet exists only after the clone.

> [!note] Your course's name appears in commands
> Your repositories live in **`Professional-Training-Cybersecurity-I`**, the GitHub organization of your course, and every command and address in this guide already uses it.
> Wherever it says **`YOUR-USERNAME`**, type your GitHub username.

---

# Before the Session

---

## Step 1: Create a GitHub account

GitHub is the website that stores your repository and the course's.
If you already have an account, use it and skip to Step 2.

1. In Firefox inside Kali, open `https://github.com/signup` and follow the form.
2. **Choose the username with care.**
   It becomes part of your repository's name, `student-YOUR-USERNAME`, and it appears on every submission you make.
   Use one you would be comfortable putting on a job application.
3. Confirm your email address from the message GitHub sends you.

> [!tip] If GitHub asks you to turn on two-factor authentication
> GitHub requires it for many accounts, and it protects the account your work lives in.
> Use an authenticator app on your phone, and keep the recovery codes GitHub gives you somewhere safe **outside** any repository.

## Step 2: Send your username

Post your username in the class Telegram group, **exactly as GitHub shows it** on your profile page, `https://github.com/YOUR-USERNAME`.
Your instructor creates your repository from it, and a misspelled username means a repository you cannot reach.

## Step 3: Accept the invitation

GitHub emails you an invitation to join your course's organization.
Accept it from the email, or open `https://github.com/orgs/Professional-Training-Cybersecurity-I/invitation` while signed in.

**Checkpoint:** both of these pages open for you and show a README:

- `https://github.com/Professional-Training-Cybersecurity-I/course-materials`
- `https://github.com/Professional-Training-Cybersecurity-I/student-YOUR-USERNAME`

Your repository is **private**: only you and your instructor can see it.
If both pages show *404 This is not the web page you are looking for*, the invitation has not been accepted yet, or has not been sent.
Ask in the Telegram group.

If `course-materials` opens and only your own repository shows 404, you have joined, and your instructor has not given you access to your repository yet.
Do not accept anything again: your repository opens once your instructor finishes setting it up, before the session.

---

# Setup

---

## Step 4: Install the four tools

> [!note] How Linux installs software
> Linux installs software as **packages**: a file holding the program together with a list of the other packages it needs.
> **`apt`** is Kali's package manager.
> It downloads packages from Kali's **repository**, a server holding thousands of them, and installs each one together with everything it needs.
> Kali's package format is **`.deb`**, and all four tools arrive as one.
> Git and Flameshot come from Kali's repository, where `apt` checks each package's signature and keeps it updated.
> VS Code and Obsidian come from their makers as a downloaded `.deb` file, which `apt` installs the same way.

1. **Refresh the list of available packages:**

   ```bash
   sudo apt update
   ```

   `sudo` runs the command as the administrator and asks for **your Kali password**, the one you set in Session 1.
   Nothing appears while you type it.
   That is deliberate, not a frozen terminal.

   > [!tip] Upgrade the rest of Kali at home
   > `sudo apt full-upgrade` brings every installed package up to date, which is what Kali advises for a rolling system.
   > Run it at home rather than in class: on an image a few months old it can download several gigabytes, and a whole class doing that at once saturates the connection.

2. **Install Git** from Kali's repository:

   ```bash
   sudo apt install -y git
   ```

   Git already ships with Kali, so `apt` most likely installs nothing and says so in one line, with your version number in the brackets:

   ```
   git is already the newest version (1:2.53.0-1).
   ```

   That line is a success: Git is installed and current.
   If Kali has a newer Git than yours, `apt` upgrades it instead.
   Either way, you end with the newest version.
   Asking for a package that is already installed is always safe, which is why this guide asks rather than assuming.

3. **Install Flameshot** from Kali's repository:

   ```bash
   sudo apt install -y flameshot
   ```

   The install ends with a few lines such as `No services need to be restarted.` That is `apt` checking whether anything running needs a restart after the install.
   Nothing does.

4. **Install VS Code.**
   In Firefox, open `https://code.visualstudio.com/download` and choose **.deb**, **x64**, under **Debian, Ubuntu**.
   Firefox saves it in your `Downloads` folder.
   Then:

   ```bash
   sudo apt install ~/Downloads/code_*_amd64.deb
   ```

   Partway through, the terminal turns blue and shows a question titled **Configuring code**: *Add Microsoft apt repository for Visual Studio Code?*
   **`<Yes>`** is already highlighted, so press **Enter**.
   That repository is what keeps VS Code updated along with the rest of Kali.

5. **Install Obsidian.**
   In Firefox, open `https://obsidian.md/download` and choose **Deb** under Linux.
   Then:

   ```bash
   sudo apt install ~/Downloads/obsidian_*_amd64.deb
   ```

> [!note] The last line of both installs is a notice, not an error
> Installing a file from your `Downloads` folder ends with:
>
> ```
> Notice: Download is performed unsandboxed as root as file '/home/kali/Downloads/code_1.139.1-1790309529_amd64.deb' couldn't be accessed by user '_apt'. - pkgAcquire::Run (13: Permission denied)
> ```
>
> `apt` normally reads packages as a restricted helper user, which cannot open files in your home folder, so it read this one as the administrator instead.
> The words *Permission denied* belong to that first attempt.
> The install itself succeeded, and the checkpoint below proves it.

> [!warning] Download both files from these two addresses only
> Search results and advertisements lead to look-alike sites that serve modified installers.
> A `.deb` runs its install scripts as the administrator, so a modified one owns the machine.

**Checkpoint:**

```bash
dpkg-query -W git code flameshot obsidian
```

`dpkg-query` lists installed packages, in alphabetical order.
You want **four lines**, one per tool, each with a version number after the name.
Your numbers will be newer than these:

```
code	1.139.1-1790309529
flameshot	14.0.0-4
git	1:2.53.0-1
obsidian	1.13.7
```

## Step 5: Put Flameshot on the Print Screen key

> [!note] Why one key
> Every exercise from here on ends with a screenshot, so capturing has to cost one key press.
> Kali's desktop, **Xfce**, gives the **Print Screen** key to its own screenshot tool, which cannot draw the box that marks the line proving your result.
> This step hands the key to Flameshot.

1. **Switch Flameshot to X11 capture.**
   On Kali's desktop, Flameshot's default way of taking the picture waits for a service that Xfce does not provide, so Print Screen would appear to do nothing.
   Open Flameshot's settings:

   ```bash
   flameshot config
   ```

   On the **General** tab, scroll the list of options, tick **Use legacy X11 screenshot method (deprecated)**, and close the window.
   The setting is saved as soon as you tick it.
2. Open **Settings Manager** from the applications menu, then **Keyboard**, then the **Application Shortcuts** tab.
3. Find the row whose shortcut is **Print** on its own.
   Its command starts with `/usr/share/kali-themes/xfce4-s`, cut off by the column's width.
   Select it and click **Remove**.
   Leave the rows that use Print with a modifier, such as **Ctrl+Print**, alone.
4. Click **Add**.
   In the **Shortcut Command** window, type the command below and click **OK**:

   ```
   flameshot gui
   ```

5. A window says *Please press a key*.
   Press **Print Screen**.
   The list now shows `flameshot gui` with the shortcut **Print**.
   Click **Close**.

**Checkpoint:** press **Print Screen**.
The screen dims and a box lists Flameshot's keys, among them **Ctrl+s** *Save screenshot to a file* and **Esc** *Exit*.
Press **Esc** to leave without capturing.
If nothing happens within a few seconds, go back to item 1: the X11 option is not ticked.

> [!tip] A laptop without a Print Screen key
> Many laptops put it on another key together with **Fn**.
> If yours has none, bind `flameshot gui` to a free combination instead, such as **Ctrl+Shift+S**, and use that everywhere this guide says Print Screen.

## Step 6: Set up Git once

> [!note] What Git copies into every commit
> Git writes a **name and an email** into every commit you make, and it takes both from your settings.
> **`--global`** stores them once for your Kali user, in the file `~/.gitconfig`, so every repository on this machine uses them.
> The third setting decides what `git pull` does in the one situation where it would otherwise stop with an error: GitHub holds a commit that your machine does not, and your machine holds one that GitHub does not.
> With **`pull.rebase true`**, Git places your commits after GitHub's and carries on.

Type your own name and email in place of the examples:

```bash
git config --global user.name "Omar Khaled"
git config --global user.email "omar.khaled@example.com"
git config --global pull.rebase true
```

- **The name** is your full name in English letters, as it appears on the class list, so your instructor recognizes your commits at a glance.
- **The email** is the one your GitHub account uses, so GitHub links each commit to your account.

**Checkpoint:**

```bash
git config --global --list
```

You want these three lines, with your own name and email.
Any other lines already there can stay.

```
user.name=Omar Khaled
user.email=omar.khaled@example.com
pull.rebase=true
```

## Step 7: Put your key on GitHub

> [!note] The same key pair, a different server
> Last session you made an SSH key pair on Kali and copied its public half to the lab server, which then let you in without a password.
> GitHub works the same way: it stores your **public** key, and every clone, push and pull proves you hold the matching **private** key.
> The one difference is how the public key gets there.
> GitHub gives you no shell to run `ssh-copy-id` against, so you paste it into a web page instead.

1. **Print your public key:**

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

   One line, starting with `ssh-ed25519`.
   Select the whole line and copy it with **Ctrl+Shift+C**.

   If the terminal says `cat: /home/kali/.ssh/id_ed25519.pub: No such file or directory`, you have no key pair yet.
   Make one with `ssh-keygen -t ed25519`: press **Enter** to accept the default location, then choose a passphrase or press **Enter** twice for none.
   Then print it again.

   > [!warning] Only the file ending in `.pub`
   > `~/.ssh/id_ed25519`, without `.pub`, is your **private** key.
   > It never leaves this machine and is never pasted anywhere, including GitHub and the class group.

2. **Add it on GitHub.**
   Click your profile picture in the top right corner, then **Settings**, then **SSH and GPG keys** in the **Access** section of the sidebar, then **New SSH key**:
   - **Title:** `Kali lab`
   - **Key type:** Authentication Key
   - **Key:** paste the line you copied

   Click **Add SSH key**.
   GitHub may ask you to confirm your password or your second factor first.

3. **Prove GitHub accepts it:**

   ```bash
   ssh -T git@github.com
   ```

   **The first time only**, SSH has never seen GitHub, so it prints GitHub's key fingerprint and asks whether to trust it.
   Compare the **ED25519** fingerprint it prints with the one GitHub publishes at `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints`, which on 2026-09-26 read:

   ```
   SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU
   ```

   If they match, type `yes`.
   **If they do not, type `no`** and ask in the Telegram group: something between you and GitHub is not GitHub.

   If you set a passphrase on the key last session, SSH asks for it now, and again on every clone, push and pull.
   That is the key's passphrase, not your GitHub password.

   The whole first exchange looks like this, with your username in the last line:

   ```
   $ ssh -T git@github.com
   The authenticity of host 'github.com (140.82.121.4)' can't be established.
   ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
   Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
   ```

**Checkpoint:** the last line starts with `Hi YOUR-USERNAME!` and ends with `You've successfully authenticated, but GitHub does not provide shell access.` That sentence is the success message, not an error.
GitHub lets you in to use Git and to nothing else.

---

# Required Exercises

---

## Exercise 1: Clone Both Repositories and Start the Session — REQUIRED

> [!note] Two repositories, one direction each
> **Cloning** copies a repository from GitHub to your machine, with every commit it holds, once.
> After that, a pull brings only what is new.
> You clone two repositories, and each one moves work in one direction only:
>
> - **`course-materials`** carries the course's documents **to you**.
>   You only ever pull it.
> - **`student-YOUR-USERNAME`** carries your work **to your instructor**.
>   You pull it for feedback and push your work into it.
>
> Each session, your instructor puts the session's guide, home task and blank worksheets into the second, you fill in the worksheets there, and you push.
> The address you clone from also decides how Git proves who you are: an **SSH** address uses the key you just added, and any other address does not.

1. **Copy the SSH address of `course-materials`.**
   On its GitHub page, click the green **Code** button, choose the **SSH** tab, and click the copy icon beside the address.
   It looks like this:

   ```
   git@github.com:Professional-Training-Cybersecurity-I/course-materials.git
   ```

2. **Clone it into your home folder.**
   Go to your home folder with `cd ~`, then type `git clone ` with a space after it, paste the address with **Ctrl+Shift+V**, and press Enter:

   ```bash
   cd ~
   git clone git@github.com:Professional-Training-Cybersecurity-I/course-materials.git
   ```

3. **Do the same for your own repository**, copying its SSH address from its own page:

   ```bash
   git clone git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
   ```

   > [!warning] If Git asks for a username
   > `Username for 'https://github.com':` means you copied the **HTTPS** address.
   > Press **Ctrl+C**, go back to the **SSH** tab, and clone again.
   > The HTTPS address cannot use your key.

4. **Look inside your own repository.**
   Your instructor has already put this session's folder into it, at the same path the session has in `course-materials`, so your repository mirrors the course's:

   ```bash
   cd ~/student-YOUR-USERNAME
   ls Module0-Foundation/Session2
   ```

   The folder holds four files and a `screenshots` folder:

   - `Module0_Session2_Practical_Guide_Submission.md` and `Module0_Session2_Home_Task_Submission.md` are the blank **worksheets**, yours to fill in.
   - `Module0_Session2_Practical_Guide.md` is this guide and `Module0_Session2_Home_Task.md` is the home task, placed beside the worksheets so you can read them side by side in Exercise 2.

   The Tooling Reference, the Troubleshooting FAQ and the presentation stay in `~/course-materials/Module0-Foundation/Session2`.

5. **Confirm your repository uses the SSH address:**

   ```bash
   git remote -v
   ```

   Both lines, `(fetch)` and `(push)`, should start with `git@github.com:`.
   That is the address every later push goes to.

   `git remote -v` prints:

   ```
   origin	git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git (fetch)
   origin	git@github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git (push)
   ```

**Checkpoint:** `ls` lists the two `_Submission.md` worksheets, the guide, the home task and `screenshots`, and `git remote -v` shows the `git@github.com:` address twice.

> [!warning] Never fill in a worksheet inside `course-materials`
> That folder belongs to the course.
> A worksheet edited there is never handed in, and the next `git pull` in it stops with `error: cannot pull with rebase: You have unstaged changes.`, because your edit is in the way.
> Always work in the copy in `~/student-YOUR-USERNAME`.

> [!important] Fill in the worksheets only
> Never edit, move or delete the guide or the home task in your repository.
> Your instructor's fixes arrive in them through `git pull`, and a changed copy stops that pull.
> A fix never replaces a worksheet you have started, so your answers are safe.

**Your first screenshot.**
Every Record box from here on names a screenshot and the file to save it as:

1. Press **Print Screen** and drag a box around the terminal, from the `cd ~/student-YOUR-USERNAME` line down to the `git remote -v` output.
2. Press **Ctrl+S**.
   A **Save screenshot** window opens in `Pictures`, with a name made of the date and time, such as `2026-09-27_12-41.png`.
3. Go to `~/student-YOUR-USERNAME/Module0-Foundation/Session2/screenshots`, replace the name with `ex1-session-folder.png`, and click **Save**.
   Faster: select the whole name and type the full path instead, `/home/kali/student-YOUR-USERNAME/Module0-Foundation/Session2/screenshots/ex1-session-folder.png`, then press **Enter**.

The worksheet links each screenshot as `screenshots/<name>.png`, a path read from the worksheet's own folder.
A screenshot saved anywhere else, or under any other name, shows as a broken image.

> [!example] Record
> The output of `git remote -v`, and the screenshot you just saved (`ex1-session-folder.png`).
> You paste them into the worksheet in Exercise 2, once Obsidian has it open.

---

## Exercise 2: Set Up Obsidian and Fill In the Worksheet — REQUIRED

> [!note] A vault is a folder
> Obsidian opens a **vault**: an ordinary folder, whose markdown files it lists, edits and shows rendered.
> Nothing is imported or converted, and every note stays a plain `.md` file that any other program can open.
> Your vault is **your own repository's folder**, so every worksheet you fill in this course is already where Git can hand it in.
> Obsidian keeps its own settings in a hidden `.obsidian` folder inside the vault, and your repository is set to ignore that folder, so it never reaches your instructor.

1. **Open your repository as a vault.**
   Start Obsidian.
   Its first window offers **Quick start** above three choices: ignore Quick start, which makes a new vault elsewhere, and click **Open** beside **Open folder as vault**.
   In the window that opens, click **Home**, select `student-YOUR-USERNAME`, and click **Select**.
   The file list on the left then shows `Module0-Foundation` and `README`.

2. **Set the five link settings, once.**
   Open **Settings** (the gear at the bottom left), then **Files and links**, and set these in the order the window shows them:

   - **Default location for new attachments**: *In subfolder under current folder*
   - **Subfolder name**: `screenshots`
   - **New link format**: *Path from current file*
   - **Automatically update internal links**: on
   - **Use \[\[Wikilinks\]\]**: off

   **Subfolder name** appears only after the setting above it reads *In subfolder under current folder*, and its gray *Attachments* is only a hint, so type `screenshots` into it.
   Together, the five make a pasted screenshot land in the worksheet's own `screenshots` folder, with a link that GitHub and the grading tools can read.

3. **Capture the settings.**
   With the **Files and links** page open, take a screenshot of it and save it as `ex2-obsidian-settings.png` in the session's `screenshots` folder, exactly as in Exercise 1.
   Close the settings.

4. **Open the worksheet.**
   In the file list on the left, open **Module0-Foundation**, then **Session2**, then **Module0_Session2_Practical_Guide_Submission.md**.
   Obsidian saves as you type, so there is no Save button.

5. **Open this guide beside it.**
   In the file list, right-click **Module0_Session2_Practical_Guide.md** and choose **Open to the right**.
   The guide opens in a second pane, beside the worksheet.
   Click into the guide's pane and press **Ctrl+E**, so it shows in the reading view and cannot be typed into by accident.
   From here on, follow the guide on one side and fill in the worksheet on the other.

6. **Fill in Exercises 1 and 2.**
   Write your name and the date at the top.
   Put each command's output **between** the two fence lines of its box, in place of the placeholder.
   Put each screenshot on its own line below its evidence box, after a blank line:

   ```markdown
   ![ex1-session-folder](screenshots/ex1-session-folder.png)
   ```

7. **Check the result.**
   Click into the worksheet's pane and press **Ctrl+E** to switch it to the reading view.
   Each output should sit in a gray box and each screenshot should show as a picture.
   Press **Ctrl+E** again to go back to editing.

> [!tip] Pasting a screenshot instead of saving it
> Flameshot's **Ctrl+C** copies a capture instead of saving it.
> Pressing **Ctrl+V** in the worksheet then saves it into `screenshots` and writes the link for you, under a name made of *Pasted image* and the time.
> Right-click the file in the list, choose **Rename**, and give it the name the Record box asks for: Obsidian corrects the link to match.
> Then type that same name between the square brackets.

> [!example] Record
> The screenshot of **Files and links** (`ex2-obsidian-settings.png`).
> The Submission also asks what the attachment settings do and why wikilinks are off, so note what each setting changed.

**Commit your work.**
A commit records the worksheet as it is now, on your machine:

```bash
cd ~/student-YOUR-USERNAME
git add Module0-Foundation/Session2
git commit -m "Module 0 Session 2: exercises 1 and 2"
```

From here on, each exercise ends with **Commit**, which means these three commands with that exercise's number in the message.
The commits stay on your machine until Exercise 5 pushes them.

The commit prints what it recorded.
The Home Task's blank worksheet goes in with it, because it is in the same folder: you fill it in at home.

```
[main 17dc420] Module 0 Session 2: exercises 1 and 2
 4 files changed, 383 insertions(+)
 create mode 100644 Module0-Foundation/Session2/Module0_Session2_Home_Task_Submission.md
 create mode 100644 Module0-Foundation/Session2/Module0_Session2_Practical_Guide_Submission.md
 create mode 100644 Module0-Foundation/Session2/screenshots/ex1-session-folder.png
 create mode 100644 Module0-Foundation/Session2/screenshots/ex2-obsidian-settings.png
```

**Checkpoint:** run `git status`:

```
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**Ahead of `origin/main`** means GitHub does not have this commit yet.
That is expected until you push.

---

## Exercise 3: Set Up VS Code — REQUIRED

> [!note] An editor for code, and one place to run it
> **VS Code** is where you write and run code for the rest of the course.
> It opens a **folder** rather than a single file, and its **built-in terminal** starts inside that folder, so every command you type there acts on the project in front of you.
> On its own it knows no programming language: an **extension** adds one.
> The Python extension adds highlighting, running and error checking, and it is the only extension this session installs.
> Look-alike extensions exist, so you check who published it before installing.

1. **Open your repository in VS Code** from a terminal:

   ```bash
   code ~/student-YOUR-USERNAME
   ```

   The first launch shows two welcome pages.
   The first, **Welcome to VS Code**, offers a sign-in: click **Continue without Signing In** at its bottom right.
   The second, **Make It Yours**, offers color themes: pick one if you like, then click **Get Started**.
   This guide needs no sign-in, and the **Chat** panel on the right can be closed.

2. **Trust the folder.**
   VS Code opens it in **Restricted Mode**, with a banner across the top: *Restricted Mode is intended for safe code browsing.
   Trust this folder to enable all features.*
   Click **Manage** in that banner, then **Trust**.
   The page then reads *You trust this folder*.
   Trust only folders you made yourself or got from the course: in a trusted folder, VS Code runs the folder's tasks, applies its settings and activates every extension, so a folder from anywhere else can run code the moment you trust it.

3. **Install the Python extension.**
   Open the **Extensions** view with **Ctrl+Shift+X** and search for `Python`.
   Click the result named **Python**, then check two things on its page **before** clicking **Install**:
   - under the name, the publisher is **Microsoft**, with the blue verified mark
   - in the **Marketplace** box on the right, the **Identifier** is exactly `ms-python.python`

   The search also lists look-alikes such as *Python for VSCode*, by other publishers.
   Installing the right one also brings **Pylance**, **Python Debugger** and **Python Environments**, all published by Microsoft, and opens a *Get Started with Python Development* page that you can close.

4. **Open the built-in terminal** with **Terminal**, then **New Terminal**.
   Its prompt shows `~/student-YOUR-USERNAME`, the folder you opened.
   A gray hint about Copilot disappears as you start typing.
   Run:

   ```bash
   git log --oneline
   ```

   `git log --oneline` works here without any `cd`, because the terminal already sits in your repository.
   It shows your commit from Exercise 2 at the top, above the one GitHub made when your repository was created:

   ```
   17dc420 (HEAD -> main) Module 0 Session 2: exercises 1 and 2
   229c38f (origin/main, origin/HEAD) Initial commit
   ```

**Checkpoint:** the Extensions view lists **Python** as installed, and the terminal shows your Exercise 2 commit.

> [!example] Record
> The output of `git log --oneline`, and one screenshot of VS Code showing the Python extension's page with its publisher and identifier, and the terminal below it (`ex3-vscode.png`).

**Commit**, from this same terminal: it is already in the right folder, so the `cd` is not needed.
The message is `Module 0 Session 2: exercise 3`.

---

## Exercise 4: Verify the Environment — REQUIRED

> [!note] Three checks, each proving one part of the setup
> A setup is proven by checks that pass, not by steps that were followed.
> The three checks below each test one part of what you built before the worksheet existed, in order from your machine outwards: **the tools are installed**, **Git knows who you are**, and **GitHub accepts your key**.
> Because each check covers one part only, a failure points at the one step to repeat rather than at the whole setup.
> The fourth part, Flameshot on the Print Screen key, is proven by the screenshot you take of the other three.

Run the three in one terminal, in this order:

```bash
dpkg-query -W git code flameshot obsidian
git config --global --list
ssh -T git@github.com
```

- **Check 1** lists four packages, each with a version.
  A missing line means that tool's install in Step 4 did not finish.
- **Check 2** shows your name, your email and `pull.rebase=true`.
  A missing or misspelled value means repeating that line of Step 6.
- **Check 3** greets you by your GitHub username.
  It no longer asks about the fingerprint, because SSH recorded GitHub's key the first time.
  `git@github.com: Permission denied (publickey).` means GitHub does not have this machine's public key, so repeat Step 7.

All three passing look like this:

```
code	1.139.1-1790309529
flameshot	14.0.0-4
git	1:2.53.0-1
obsidian	1.13.7
user.name=Omar Khaled
user.email=omar.khaled@example.com
pull.rebase=true
Hi YOUR-USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
```

**Checkpoint:** all three pass.

> [!example] Record
> The output of each check, and one screenshot of all three in the terminal, taken with **Print Screen** (`ex4-environment.png`).

**Commit**, with the message `Module 0 Session 2: exercise 4`.

---

## Exercise 5: Push the Worksheet and Confirm It Arrived — REQUIRED

> [!note] A commit is not a submission
> Your commits so far exist only on your machine.
> **`git push`** sends them to your repository on GitHub, and **only GitHub's copy counts**: your instructor collects what is there at the deadline, 22:00 on the Saturday of the session's week.
> A commit that was never pushed is, for grading, work that was never done.
> Two checks close the loop: `git status` compares your machine with GitHub, and the repository's page in a browser shows what your instructor will see.

> [!warning] Before you push, check what is in the screenshots
> Git keeps every commit forever, so a password, key or token that reaches GitHub stays published even if you delete the file later.
> Look at each screenshot once before pushing.

1. **Push:**

   ```bash
   cd ~/student-YOUR-USERNAME
   git push
   ```

2. **Confirm your machine and GitHub agree:**

   ```bash
   git status
   ```

   You want `Your branch is up to date with 'origin/main'.` followed by `nothing to commit, working tree clean`.
   If it still says **ahead**, the push did not happen: read the error `git push` printed.

3. **Look at it the way your instructor will.**
   Open `https://github.com/Professional-Training-Cybersecurity-I/student-YOUR-USERNAME` in Firefox, then **Module0-Foundation**, **Session2**, and your Practical Guide Submission.
   GitHub shows it rendered: each output in a box, each screenshot as a picture.
   A screenshot that shows as a broken image here is broken for grading too.

The push ends by naming your repository and the commits it moved:

```
To github.com:Professional-Training-Cybersecurity-I/student-YOUR-USERNAME.git
   229c38f..f5e9418  main -> main
```

**Checkpoint:** `git status` says **up to date**, and the worksheet on GitHub shows every screenshot.

> [!example] Record
> The output of `git push` and of `git status`, and a screenshot of your worksheet on GitHub showing at least one of its pictures (`ex5-github.png`).

**Commit, then push again.**
Filling in this exercise changed the worksheet after the push you just recorded, so it needs one more commit, `Module 0 Session 2: exercise 5`, and one more `git push`.
Run `git status` once more: it must say **up to date** again.

---

## Exercise 6: Hand In the Session 1 Worksheets — REQUIRED

> [!note] Moving files from your computer into Kali
> Your Session 1 worksheets and their screenshots are on your own computer, the **host**, and Kali cannot see the host's files.
> A **shared folder** is VirtualBox's way across: you name a folder on the host, and VirtualBox shows it inside Kali as `/media/sf_` followed by the name you give it.
> You make it **read-only**, so nothing inside Kali can change your host's files, and you remove it once the files are copied, because a lab machine has no reason to see your own computer.

1. **Gather the files on the host.**
   Put both Session 1 worksheets and their `screenshots` folder together in one folder of their own, as they were when you filled them in.

2. **Share that folder with Kali.**
   In the Kali machine's window, open **Devices**, then **Shared Folders**, then **Shared Folders Settings**, and add a folder:
   - **Folder Path:** the folder from step 1
   - **Folder Name:** `session1`
   - **Read-only:** on
   - **Auto-mount:** on

   Leave **Make Permanent** off: the share then disappears by itself when Kali shuts down.

3. **Find it in Kali:**

   ```bash
   ls /media/sf_session1 /media/sf_session1/screenshots
   ```

   You want the two worksheets, named exactly `Module0_Session1_Practical_Guide_Submission.md` and `Module0_Session1_Home_Task_Submission.md`, and your screenshots inside `screenshots`.
   A file saved twice from a chat often gains a suffix such as ` (1)`: rename it on the host to the exact name, because the grading tools look for that name and nothing else.
   If `ls` says `Permission denied`, your Kali user is not allowed to read shared folders yet.
   Run `sudo usermod -aG vboxsf $USER`, log out of Kali, log back in, and try again.

4. **Copy them into your repository**, into the Session 1 folder that mirrors the course's:

   ```bash
   cd ~/student-YOUR-USERNAME
   mkdir -p Module0-Foundation/Session1
   cp --no-preserve=mode /media/sf_session1/Module0_Session1_*_Submission.md Module0-Foundation/Session1/
   cp -r --no-preserve=mode /media/sf_session1/screenshots Module0-Foundation/Session1/
   ls -R Module0-Foundation/Session1
   ```

   `ls -R` shows exactly this, and nothing else:

   ```
   Module0-Foundation/Session1:
   Module0_Session1_Home_Task_Submission.md	screenshots
   Module0_Session1_Practical_Guide_Submission.md

   Module0-Foundation/Session1/screenshots:
   ex3-kali-desktop.png
   ```

   Your screenshot names are your own Session 1 names.

   Only the worksheets and the `screenshots` folder are copied, never the whole shared folder, so nothing else from your host reaches your repository.
   `--no-preserve=mode` matters too: every file in a shared folder looks executable to Kali, and without it Git would record your worksheets as programs.

5. **Add the AI Assistance line.**
   Every worksheet in this course ends with an **AI Assistance** section, and the Session 1 worksheets were first handed out without one.
   Open each Session 1 worksheet in Obsidian.
   If it does not already end with **AI Assistance**, add these lines at its very end, replacing the placeholder with `None`, or with the AI assistant you used and what you used it for:

   ````markdown
   ---

   ## AI Assistance

   ```
   (None, or: which assistant, and what for)
   ```
   ````

   Using an assistant for learning, explanation or debugging is allowed.
   Not disclosing it is an integrity violation.
   Edit the copies in your repository, not the ones on your host: the shared folder is read-only, and the repository's copies are the ones you hand in.

6. **Check them in Obsidian.**
   Open each Session 1 worksheet from the file list and switch to the reading view with **Ctrl+E**.
   Every screenshot should show as a picture, and the last section should be **AI Assistance**.

7. **Remove the shared folder.**
   Back in **Devices**, **Shared Folders**, **Shared Folders Settings**, select `session1` and remove it.

**Commit and push**, from your repository's folder:

```bash
git add Module0-Foundation/Session1
git commit -m "Module 0 Session 1: worksheets"
git push
git status
```

**Checkpoint:** `git status` says **up to date**, and on GitHub the folder `Module0-Foundation/Session1` shows both worksheets with their screenshots.

> [!example] Record
> The output of `ls -R Module0-Foundation/Session1`, and a screenshot of that folder on GitHub (`ex6-session1-github.png`).
> This one goes in **this session's** worksheet, then one more commit, `Module 0 Session 2: exercise 6`, and one more push.

---

# When something fails

**Note the exact step and copy the exact message Git or the terminal printed.**
Git's errors name their own fix far more often than not, and a message pasted in full into the Telegram group is a two-minute answer.
"It did not push" is not.

The Troubleshooting FAQ is organized by the symptom in front of you.
It covers every common Git mistake, each with Git's full message and the fix.

---

# What "done" looks like

- `dpkg-query` lists Git, VS Code, Flameshot and Obsidian
- **Print Screen** starts a Flameshot capture
- `git config --global --list` shows your name, your email and `pull.rebase=true`
- `ssh -T git@github.com` greets you by your username
- `~/course-materials` and `~/student-YOUR-USERNAME` are both cloned
- Obsidian opens your repository as its vault, with the five link settings set
- VS Code has the Python extension from Microsoft
- On GitHub, your repository holds `Module0-Foundation/Session1` and `Module0-Foundation/Session2`, every screenshot shows, and `git status` says **up to date**

**Then take a snapshot.**
Shut Kali down and, in the VirtualBox Manager, take a snapshot of it named **`tools installed`**.
From here, a broken environment costs a restore rather than an evening.
Your work is safe either way, because it is on GitHub: after a restore, one `git pull` brings it back.

**Every later session starts and ends the same way:** pull both repositories, open the new session's folder in your repository, fill in its worksheets beside its guide, commit each worksheet when it is finished, push, and check `git status`.
