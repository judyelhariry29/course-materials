# Module 0 · Session 1 — Home Task

## Proving the Lab Does What It Claims

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> This session built a lab.
> **This home task makes you prove it behaves the way it was described**, by changing one thing at a time and watching what breaks.
> Every task here is **reversible**, and putting each one back is part of the task.
>
> There is no code in this one.
> What is being assessed is whether you can make a change, predict the result, observe what actually happened, and explain the difference.
>
> Paste your commands, their output, your screenshots and your answers into **`Module0_Session1_Home_Task_Submission.md`**.
> That is the graded document.

> [!important] Everything here is required
> There are no optional tasks.
> Task 1 may already be finished, in which case say so and move on.

> [!warning] Everything stays inside your own lab
> Every command here is aimed at machines you built on your own computer.
> Nothing in this task touches a network you do not own, and nothing in this course ever should without written permission.

> [!warning] Do Task 4 only after you have the snapshots
> Task 4 deliberately changes a machine and then undoes it by restoring.
> If you skipped the snapshots, go back and take them first.

---

# Task 1: Finish the build

If any machine is unfinished, finish it now from the session's Practical Guide, picking up wherever you stopped.

Then run the three checks one more time, from Kali:

```bash
ip a
ping -c 1 <your Ubuntu address>
ssh lab
```

> [!example] Submission
> All three commands with their output, plus check 1 from each of the three machines, using `ip a` on Kali and Ubuntu and `ipconfig` on Windows.
> If the build was already finished, say so and paste the checks anyway.
> **If something still fails, paste the exact error.**
> An error you can show is a two-minute fix.
> Screenshot: `task1-checks.png`.

---

# Task 2: Prove a NAT Network is not NAT

The lab uses a **NAT Network** rather than plain **NAT**, and the reason given was that plain NAT puts each machine on a private network of its own where it cannot see the others.
Test that claim.

1. **Predict first, in writing.**
   With Kali moved to plain NAT, what do you expect from each of the three checks?
   Write your prediction down **before** you change anything.
2. Shut Kali down.
   In **Settings**, then **Network**, then **Adapter 1**, change **Attached to** from `NAT Network` to `NAT`.
   Leave everything else alone.
3. Start Kali and run all three checks again.
4. **Put it back.**
   Shut Kali down, set Adapter 1 back to **NAT Network** with **Name: CyberLab**, start it, and confirm all three checks pass again.

> [!example] Submission
> Your written prediction, the output of all three checks under plain NAT, and the output of all three after you restored CyberLab.
> Screenshots: `task2-plain-nat.png` for the failing check, and `task2-restored.png` for Adapter 1 back on CyberLab with the checks passing.
> Then answer:
>
> - **Which checks changed, and which did not?**
>   Be exact about which one failed first.
> - Kali still reached the internet under plain NAT.
>   **Explain why that is consistent with it being unable to reach Ubuntu.**
> - **What does the first failing check tell you that the others do not?**

---

# Task 3: Prove the client config is not only for `ssh`

The `~/.ssh/config` entry you wrote turns an address, an account and a key path into the single word `lab`.
That file is read by more than one program.

From Kali:

1. **Run one command on the server without opening a session on it:**

   ```bash
   ssh lab uptime
   ```

2. **Copy a file to the server using the same alias:**

   ```bash
   echo "built on $(date)" > lab-notes.txt
   scp lab-notes.txt lab:
   ```

3. **Copy it back, under a different name, to prove the direction reverses:**

   ```bash
   scp lab:lab-notes.txt returned-notes.txt
   cat returned-notes.txt
   ```

> [!example] Submission
> All three commands with their output, and a screenshot of them in one terminal (`task3-scp.png`).
> Then answer:
>
> - **Neither `scp` command named an address, an account or a key.
>   Where did each of those come from?**
> - The server's address is handed out by DHCP and could change.
>   **What exactly would you edit, and how many places?**
> - **Why is `ssh lab uptime` useful?**
>   Name one thing it lets you do that opening a session and typing `uptime` does not.

---

# Task 4: Prove what a snapshot actually restores

The claim was that a snapshot puts the **whole machine** back to a named point, and that this is what makes the lab disposable.
Test both halves of that.

On the **Ubuntu** machine, **at its own console**, because step 2 takes SSH away:

1. **Leave a mark that you would notice:**

   ```bash
   echo "work I care about" > ~/important-notes.txt
   ls ~
   ```

2. **Break something you will miss.**
   Stop SSH from listening, then confirm it is down:

   ```bash
   sudo systemctl stop ssh.socket
   systemctl is-active ssh.socket ssh.service
   ```

   > [!warning] Stop the socket, not only the service
   > Current Ubuntu does not keep the SSH server running.
   > **systemd holds port 22 itself**, through `ssh.socket`, and starts the server only when a connection arrives.
   > `systemctl stop ssh` therefore stops a service that was not the thing listening, and the next connection starts it straight back up.
   > Stopping `ssh.socket` takes the listener away, and the service stops with it.
   > Both lines of the second command should read `inactive`.

3. From Kali, confirm it is genuinely broken:

   ```bash
   ssh lab
   ```

4. **Restore.**
   Shut the machine down, select it in VirtualBox, open **Snapshots**, select `clean install`, and **Restore**.
5. Start it and check both things: is SSH working again, and is `~/important-notes.txt` still there?

> [!example] Submission
> The output from each step, including the failing `ssh lab`, and the state of both SSH and the file after the restore.
> Screenshots: `task4-broken.png` for the failed connection, and `task4-restored.png` for the machine working again.
> Then answer:
>
> - **What happened to `important-notes.txt`, and why?**
> - The session warned that **restoring is not undoing your last action**.
>   Explain that warning in your own words, using what you just observed.
> - **Name one thing a snapshot does not protect you from.**

---

# Task 5: Short answers

Answer these in your own words.
Two or three sentences each is enough, and a correct short answer beats a long one.

1. **Why is the network created before the machines rather than after?**
   What specifically would you have to redo if you built the machines first?
2. **A ping to your Windows machine fails.**
   Give two different explanations, one where the lab is working correctly and one where it is not, and say **which check would tell them apart**.
3. **When you log in with a key, what crosses the wire?**
   Explain why someone who captured it still could not log in as you afterward.
4. **Why does the server never need your private key?**
   What does it hold instead, and what can it do with that?
5. **Nothing outside can start a conversation with your lab machines, and no rule was written to stop it.**
   Explain where that protection actually comes from.
6. **That protection does not work in the other direction.**
   Say what stops you from reaching something real, in one sentence.

---

# What "done" looks like

- All three machines built, and the three checks pass
- Task 2 done and **put back**, with Kali on CyberLab again
- Task 3 done, with all three commands shown
- Task 4 done and **restored**, with SSH working again
- All six short answers written
- Everything pasted into `Module0_Session1_Home_Task_Submission.md`

> [!warning] Leave the lab in a working state
> Tasks 2 and 4 both change a machine on purpose.
> **Both of them end by putting it back.**
> The next session expects the lab exactly as this session's checks left it.
