## Version Control Using Git and the Command Line: A Comprehensive Command Reference

This document provides an exhaustive reference for Git commands used in the command line. It covers all major subcommands, their options (both short and long flags), and practical examples. The focus is on local repository operations, but remote interactions are also included where relevant. Whether you are a beginner seeking to understand each flag or an experienced developer looking for a quick reminder, this guide offers detailed explanations and realistic scenarios.

---

### Table of Contents

1. [Getting Help](#1-getting-help)
2. [Setup and Configuration](#2-setup-and-configuration)
3. [Creating and Cloning Repositories](#3-creating-and-cloning-repositories)
4. [Basic Snapshotting](#4-basic-snapshotting)
   - [git status](#git-status)
   - [git add](#git-add)
   - [git commit](#git-commit)
   - [git diff](#git-diff)
   - [git rm](#git-rm)
   - [git mv](#git-mv)
5. [Viewing History](#5-viewing-history)
   - [git log](#git-log)
   - [git show](#git-show)
   - [git shortlog](#git-shortlog)
6. [Undoing Changes](#6-undoing-changes)
   - [git restore](#git-restore)
   - [git reset](#git-reset)
   - [git revert](#git-revert)
   - [git clean](#git-clean)
   - [git reflog](#git-reflog)
7. [Branching and Merging](#7-branching-and-merging)
   - [git branch](#git-branch)
   - [git checkout / git switch](#git-checkout--git-switch)
   - [git merge](#git-merge)
   - [git rebase](#git-rebase)
   - [git cherry-pick](#git-cherry-pick)
8. [Stashing](#8-stashing)
   - [git stash](#git-stash)
9. [Remote Repositories](#9-remote-repositories)
   - [git remote](#git-remote)
   - [git fetch](#git-fetch)
   - [git pull](#git-pull)
   - [git push](#git-push)
10. [Tags](#10-tags)
    - [git tag](#git-tag)
11. [Inspection and Comparison](#11-inspection-and-comparison)
    - [git blame](#git-blame)
    - [git grep](#git-grep)
    - [git diff (advanced)](#git-diff-advanced)
12. [Advanced Commands](#12-advanced-commands)
    - [git bisect](#git-bisect)
    - [git submodule](#git-submodule)
    - [git worktree](#git-worktree)
13. [Aliases and Customisation](#13-aliases-and-customisation)
14. [Summary of Common Flags](#14-summary-of-common-flags)

---

### 1. Getting Help

Before diving into commands, it is essential to know how to access Git’s built‑in documentation. Every command and its options can be viewed with:

```bash
git help <command>
git <command> --help
```

For example:

```bash
git help commit
git add --help
```

This opens the manual page in your default browser or terminal pager.

---

### 2. Setup and Configuration

**`git config`** – Set configuration variables at three levels: system (`--system`), global (`--global`), and local (`--local`, default).

**Common flags**:

- `--global` – applies to your user account.
- `--list` (`-l`) – lists all settings.
- `--edit` (`-e`) – opens the configuration file in your editor.
- `--unset` – removes a setting.
- `--add` – adds a new line (useful for multi‑valued options).

**Examples**:

```bash
# Set user name and email (global)
git config --global user.name "John Doe"
git config --global user.email "john@example.com"

# Set default editor to VS Code
git config --global core.editor "code --wait"

# Set an alias
git config --global alias.co checkout

# List all configuration
git config --list

# View a specific key
git config user.name

# Edit global config directly
git config --global --edit
```

Configuration files are stored in:
- System: `[git-install-dir]/etc/gitconfig`
- Global: `~/.gitconfig` or `~/.config/git/config`
- Local: `.git/config` in the repository.

---

### 3. Creating and Cloning Repositories

**`git init`** – Initialises a new Git repository in the current directory.

```bash
git init
# Creates a .git folder

git init my-project
# Creates a new directory 'my-project' and initialises a repo inside it
```

**`git clone`** – Copies an existing repository from a URL.

```bash
git clone https://github.com/user/repo.git
# Clones into a directory named 'repo'

git clone https://github.com/user/repo.git myfolder
# Clones into 'myfolder'

git clone --depth 1 https://github.com/user/repo.git
# Shallow clone (only the latest commit, reduces download size)

git clone --branch develop --single-branch https://github.com/user/repo.git
# Clone only the 'develop' branch
```

**Flags for clone**:
- `--depth <n>` – creates a shallow clone with history truncated to the specified number of commits.
- `--branch <name>` (`-b`) – checks out a specific branch instead of the default.
- `--single-branch` – only fetches history for the branch specified.
- `--recurse-submodules` – initialises and clones submodules recursively.

---

### 4. Basic Snapshotting

#### git status

Shows the state of the working directory and staging area.

```bash
git status
# Displays which files are modified, staged, or untracked

git status -s
# Short format (one line per file, with status codes)
# Example output:
#  M README.md   (modified, not staged)
# M  file.txt    (modified, staged)
# ?? newfile.py  (untracked)
```

**Flags**:
- `-s` (`--short`) – compact output.
- `-b` (`--branch`) – shows branch information even in short format.
- `--ignored` – shows ignored files as well.

#### git add

Stages changes for commit.

**Common flags**:

- `-A` (`--all`) – stages all changes (including deletions and new files) in the entire repository.
- `.` – stages all changes in the current directory and subdirectories (similar to `-A` but respects current directory).
- `-u` (`--update`) – stages modifications and deletions for tracked files only (does not stage new files).
- `-p` (`--patch`) – interactively choose hunks to stage.
- `-n` (`--dry-run`) – shows what would be added without actually adding.
- `-v` (`--verbose`) – verbose output.

**Examples**:

```bash
git add file.txt
# Stages a single file

git add src/*.js
# Stages all .js files in src/

git add -A
# Stages all changes (new, modified, deleted) in the whole repo

git add .
# Stages all changes in the current directory and below

git add -u
# Stages modifications and deletions for already tracked files

git add -p
# Enters interactive patch mode where you can review and stage parts of files
```

#### git commit

Records staged changes in the repository history.

**Common flags**:

- `-m "message"` – specifies the commit message inline.
- `-a` (`--all`) – automatically stages all tracked files (modified and deleted) before committing. Equivalent to running `git add -u` first.
- `--amend` – modifies the most recent commit instead of creating a new one. Can be used to change the message or add forgotten files.
- `--no-edit` – when amending, use the previous message without opening the editor.
- `--author="Name <email>"` – overrides the commit author.
- `--date="date"` – sets the commit date.
- `--dry-run` – shows what would be committed without actually committing.
- `-v` – shows the diff in the commit message editor.

**Examples**:

```bash
git commit -m "Initial commit"
# Commit staged changes with inline message

git commit -a -m "Fix typo"
# Stage all tracked changes and commit (shortcut for git add -u && git commit -m)

git commit --amend -m "Better commit message"
# Replace the last commit with a new message

git commit --amend --no-edit
# Add staged changes to the last commit without changing the message

git commit --author="Jane Doe <jane@example.com>" -m "Co-authored commit"
# Set a different author
```

**Note**: `git commit -a` stages only tracked files; new (untracked) files must be added explicitly with `git add`.

#### git diff

Shows differences between various states: working directory, staging area, commits, branches, etc.

**Basic forms**:

- `git diff` – changes in working directory that are not yet staged.
- `git diff --staged` (or `--cached`) – changes staged for the next commit (staging area vs last commit).
- `git diff HEAD` – changes in working directory vs last commit (includes both staged and unstaged).
- `git diff <commit>` – changes in working directory vs given commit.
- `git diff <commit1> <commit2>` – changes between two commits.
- `git diff <branch1> <branch2>` – changes between tips of two branches.
- `git diff <commit> -- <file>` – changes for a specific file.

**Common flags**:

- `--stat` – shows summary of changes (number of insertions/deletions per file).
- `--name-only` – shows only names of changed files.
- `--name-status` – shows names and status (M, A, D) of changed files.
- `--cached` – same as `--staged`.
- `--word-diff` – shows word‑level differences.
- `--color-words` – highlights changed words.
- `--check` – warns about whitespace errors.
- `--patience` – uses patience diff algorithm for better readability.
- `--no-index` – compares two files outside a repository.
- `-U<n>` – sets number of context lines (e.g., `-U5`).

**Examples**:

```bash
git diff
# Unstaged changes

git diff --staged
# Staged changes

git diff HEAD~2 HEAD
# Changes between two commits ago and now

git diff main feature
# Diff between main branch and feature branch

git diff --stat
# Summary of changes

git diff --name-only
# Just file names

git diff --word-diff
# Word-by-word diff

git diff --cached --check
# Check staged changes for whitespace errors
```

#### git rm

Removes files from the working directory and stages the removal for the next commit.

**Common flags**:

- `--cached` – removes the file from the staging area and Git’s tracking, but leaves it in the working directory. Useful for stopping tracking a file (e.g., one that should be ignored).
- `-f` (`--force`) – force removal even if the file has unstaged changes.
- `-r` – recursively remove directories.

**Examples**:

```bash
git rm file.txt
# Removes file.txt from disk and stages the deletion

git rm --cached secret.conf
# Stops tracking secret.conf but keeps it on disk (add to .gitignore afterwards)

git rm -r old-folder/
# Removes entire directory recursively

git rm -f important.log
# Force removal despite local modifications
```

#### git mv

Moves or renames a file and stages the change.

```bash
git mv oldname.txt newname.txt
# Renames file and stages it
```

Equivalent to:
```bash
mv oldname.txt newname.txt
git add -A   # or git add oldname.txt newname.txt
```

---

### 5. Viewing History

#### git log

Displays commit history.

**Common flags**:

- `--oneline` – each commit on one line (abbreviated hash + subject).
- `--graph` – ASCII graph of branch structure.
- `--all` – shows all branches.
- `--decorate` – adds branch/tag names to commits.
- `--author=<pattern>` – filter by author.
- `--committer=<pattern>` – filter by committer.
- `--grep=<pattern>` – filter commit messages by pattern.
- `-S<string>` – filter commits that introduced or removed a string (pickaxe).
- `-G<regex>` – similar but with regex.
- `--since`, `--after`, `--until`, `--before` – date filters.
- `-n <number>` – limit to last N commits.
- `--pretty=format:"%h %s"` – custom formatting.
- `--stat` – show file change statistics.
- `--patch` (`-p`) – show the diff of each commit.
- `--name-only` – list files changed.
- `--name-status` – list files with status.

**Examples**:

```bash
git log
# Full history

git log --oneline
# 1a2b3c4 Fix typo in README
# 5d6e7f8 Add login feature

git log --oneline --graph --all --decorate
# Pretty graph with branches

git log --author="John" --since="2 weeks ago"
# Commits by John in last two weeks

git log -S"function foo" --oneline
# Commits that added or removed "function foo"

git log --grep="bugfix" -i
# Case-insensitive search for "bugfix" in messages

git log --pretty=format:"%h - %an, %ar : %s"
# Custom format: hash, author, relative date, subject

git log --stat -2
# Show statistics for last two commits

git log -p file.txt
# Show full diff of commits affecting file.txt
```

#### git show

Displays information about a specific object (commit, tag, tree, blob).

```bash
git show <commit>
# Shows commit message and diff

git show --name-only <commit>
# Only list changed files

git show <tag>
# Shows tag details and the commit it points to

git show HEAD:file.txt
# Shows content of file.txt as it exists in the latest commit
```

**Flags**: many of the same as `git log` for formatting diffs.

#### git shortlog

Summarises `git log` output grouped by author, often used for release notes.

```bash
git shortlog
# Groups commits by author, listing subjects

git shortlog -sn
# Shows only count and author names (numbered)

git shortlog -e
# Includes email addresses

git shortlog -s -n --since="1 month ago"
# Number of commits per author in last month, sorted
```

---

### 6. Undoing Changes

#### git restore

A modern command to restore working tree files or unstage. Introduced in Git 2.23 as a clearer alternative to `git checkout` for file operations.

**Forms**:

- `git restore <file>` – discards changes in working directory (like `git checkout -- <file>`).
- `git restore --staged <file>` – unstages a file (like `git reset HEAD <file>`).
- `git restore --source=<commit> <file>` – restores file to the state from a specific commit.

**Flags**:

- `-s <commit>` (`--source`) – specifies the source.
- `-W` (`--worktree`) – target the working tree (default if no `--staged`).
- `--staged` – target the index (staging area).
- `-p` – interactively select hunks to restore.

**Examples**:

```bash
git restore file.txt
# Discard unstaged changes to file.txt

git restore --staged file.txt
# Unstage file.txt (keep working copy changes)

git restore --source=HEAD~2 file.txt
# Restore file.txt to how it was two commits ago (both staged and working copy)

git restore -p file.txt
# Interactively choose which changes to discard
```

#### git reset

Moves the current branch pointer and optionally resets the staging area and working directory. It is powerful but can be destructive.

**Modes**:

- `--soft` – moves HEAD to the specified commit, but leaves the index and working directory unchanged. Changes from the undone commits become staged.
- `--mixed` (default) – moves HEAD and resets the index to match the specified commit, but leaves working directory unchanged. Changes become unstaged.
- `--hard` – moves HEAD, resets the index, and overwrites working directory to match the specified commit. **All uncommitted changes are lost**.

**Forms**:

- `git reset <commit>` – resets current branch to `<commit>` (default `--mixed`).
- `git reset <file>` – unstages the file (equivalent to `git restore --staged <file>`). This form does not move HEAD.
- `git reset --hard HEAD~1` – discard last commit and all its changes.

**Examples**:

```bash
git reset HEAD~1
# Undo last commit, keep changes unstaged (--mixed)

git reset --soft HEAD~1
# Undo last commit, keep changes staged

git reset --hard HEAD~1
# Completely remove last commit and all changes

git reset --hard origin/main
# Discard all local commits and make current branch exactly like origin/main

git reset file.txt
# Unstage file.txt (shortcut for git reset HEAD file.txt)
```

**Caution**: Avoid resetting commits that have been pushed to shared branches. Use `git revert` instead.

#### git revert

Creates a new commit that undoes the changes of a specified commit. It is safe for public history because it does not rewrite existing commits.

```bash
git revert HEAD
# Creates a new commit that undoes the last commit

git revert abc1234
# Reverts the specific commit with hash abc1234

git revert -n HEAD~3..HEAD
# Reverts a range of commits but does not auto‑commit (-n), leaving changes staged
```

**Flags**:

- `-e` (`--edit`) – edit the commit message (default).
- `--no-edit` – use the generated message without editing.
- `-n` (`--no-commit`) – revert changes but do not create a commit (useful for reverting multiple commits and committing together).
- `-m <parent-number>` – for merge commits, specifies which parent to keep (usually `-m 1` to keep the first parent).

#### git clean

Removes untracked files from the working directory.

**Flags**:

- `-n` (`--dry-run`) – show what would be removed.
- `-f` (`--force`) – actually remove files (required unless `clean.requireForce` is false).
- `-d` – also remove untracked directories.
- `-x` – also remove ignored files.
- `-X` – remove only ignored files.

**Examples**:

```bash
git clean -n
# Preview untracked files that would be removed

git clean -f
# Remove untracked files

git clean -fd
# Remove untracked files and directories

git clean -fdx
# Remove everything untracked, including ignored files and directories (be careful!)
```

#### git reflog

Git keeps a log of where HEAD and branch tips have pointed (local only). This is your safety net for recovering lost commits.

```bash
git reflog
# Shows history of HEAD movements

git reflog show main
# Shows history of main branch

git reset --hard HEAD@{2}
# Reset to the state HEAD was two moves ago

git checkout -b recovery abc1234
# Create a new branch from a lost commit found in reflog
```

---

### 7. Branching and Merging

#### git branch

Lists, creates, or deletes branches.

**Common flags**:

- `-a` – list all branches (local and remote).
- `-r` – list only remote branches.
- `-v` (`-vv`) – verbose, show last commit on each branch.
- `--merged` – show branches merged into current branch.
- `--no-merged` – show branches not merged.
- `-d` – delete a branch (only if merged).
- `-D` – force delete a branch (even if not merged).
- `-m` – rename/move a branch.
- `-c` – copy a branch.

**Examples**:

```bash
git branch
# List local branches

git branch -a
# List all branches (local + remote)

git branch feature
# Create new branch 'feature' (stays on current branch)

git branch -d feature
# Delete 'feature' if merged

git branch -D feature
# Force delete 'feature'

git branch -m oldname newname
# Rename branch

git branch --merged
# Show branches that have been merged into current branch

git branch --no-merged main
# Show branches not merged into main
```

#### git checkout / git switch

`git checkout` is a versatile command for switching branches or restoring files. Since Git 2.23, the new commands `git switch` (for branches) and `git restore` (for files) provide clearer intent. Both are covered here.

**`git checkout`**:

- Switch branches: `git checkout <branch>`
- Create and switch: `git checkout -b <new-branch>`
- Checkout a commit (detached HEAD): `git checkout <commit-hash>`
- Restore a file: `git checkout -- <file>` (discard changes)
- Restore a file from another branch/commit: `git checkout <branch> -- <file>`

**`git switch`**:

- Switch to an existing branch: `git switch <branch>`
- Create and switch: `git switch -c <new-branch>`
- Switch to a previous branch: `git switch -`
- Detached HEAD: `git switch --detach <commit>`

**Flags** common to both (where applicable):

- `-b` (for checkout) / `-c` (for switch) – create branch.
- `-f` (`--force`) – force switch even if working directory has changes (overwrites them).
- `--merge` – merge local changes into the new branch.

**Examples**:

```bash
git checkout main
# Switch to main

git checkout -b feature
# Create and switch to feature

git checkout -- file.txt
# Discard unstaged changes in file.txt

git switch develop
# Switch to develop

git switch -c hotfix
# Create and switch to hotfix

git switch -
# Switch to previous branch
```

#### git merge

Combines changes from another branch into the current branch.

**Common flags**:

- `--no-ff` – create a merge commit even if fast‑forward is possible.
- `--ff-only` – only merge if fast‑forward is possible; otherwise abort.
- `--squash` – squash all commits from the other branch into one change, but do not commit (staged). You then commit manually.
- `--abort` – abort the current merge due to conflicts.
- `--continue` – after resolving conflicts, continue the merge.
- `-m <message>` – set the merge commit message.
- `--no-commit` – perform the merge but stop before creating a commit (staged).

**Examples**:

```bash
git checkout main
git merge feature
# Merge feature into main (may fast‑forward)

git merge --no-ff feature
# Force a merge commit even if fast‑forward possible

git merge --squash feature
# Squash all feature commits into one set of changes, staged for commit

git merge --abort
# If conflicts, abort and go back to pre‑merge state
```

**Conflict resolution**: After resolving conflicts manually, `git add` the resolved files and then `git commit` (or `git merge --continue`).

#### git rebase

Reapplies commits on top of another base tip. Used to maintain a linear history.

**Common flags**:

- `-i` (`--interactive`) – interactively edit, squash, reorder commits.
- `--onto <newbase>` – used to transplant a branch onto a different base.
- `--continue` – after resolving conflicts, continue the rebase.
- `--skip` – skip the current commit (if problematic).
- `--abort` – abort the rebase and return to original state.
- `--autosquash` – automatically squash fixup commits (used with interactive rebase).
- `-X<strategy-option>` – pass merge strategy options (e.g., `-Xours` to favour current branch on conflicts).

**Examples**:

```bash
git checkout feature
git rebase main
# Reapply feature commits on top of current main

git rebase --interactive HEAD~3
# Interactively rebase last three commits

git rebase --onto main feature-branch base-branch
# Transplant branch from base-branch to main

git rebase --continue
# After resolving conflicts during rebase
```

**Warning**: Rebasing rewrites history. Do not rebase commits that have been pushed to a shared branch unless you coordinate with the team.

#### git cherry-pick

Applies a specific commit from one branch onto the current branch.

```bash
git cherry-pick abc1234
# Apply commit abc1234 to current branch

git cherry-pick -n abc1234
# Apply but don't commit (staged)

git cherry-pick -x abc1234
# Append a line "(cherry picked from commit ...)" to the commit message
```

**Flags**:

- `-e` (`--edit`) – edit commit message.
- `-n` (`--no-commit`) – apply changes but don't commit.
- `-x` – add reference to original commit (useful for tracking).
- `--signoff` – add Signed‑off‑by line.

---

### 8. Stashing

#### git stash

Temporarily shelves changes (modified tracked files and staged changes) so you can work on something else, then reapply them later.

**Common subcommands and flags**:

- `git stash` – stashes both staged and unstaged changes (equivalent to `git stash push`).
- `git stash push -m "message"` – stash with a description.
- `git stash list` – lists all stashes.
- `git stash show` – shows diff summary of the latest stash (or `git stash show stash@{1}`).
- `git stash pop` – applies the latest stash and removes it from stash list.
- `git stash apply` – applies the latest stash but keeps it in stash list.
- `git stash drop` – removes the latest stash.
- `git stash clear` – removes all stashes.
- `git stash branch <branchname>` – creates a new branch from the stash and drops it.
- `-u` (`--include-untracked`) – also stash untracked files.
- `-a` (`--all`) – stash all files, including ignored ones.

**Examples**:

```bash
git stash
# Stash current changes

git stash save "WIP on login feature"
# Stash with a message

git stash list
# stash@{0}: On feature: WIP on login feature
# stash@{1}: On main: fix typo

git stash show -p stash@{1}
# Show full diff of a specific stash

git stash pop
# Apply and remove the most recent stash

git stash apply stash@{2}
# Apply a specific stash without removing it

git stash drop stash@{0}
# Delete a specific stash

git stash branch new-feature
# Create a branch from stash and drop it (useful if stash conflicts with current state)
```

---

### 9. Remote Repositories

#### git remote

Manages remote repositories.

**Common commands and flags**:

- `git remote -v` – list remotes with URLs (verbose).
- `git remote add <name> <url>` – add a new remote.
- `git remote remove <name>` – remove a remote.
- `git remote rename <old> <new>` – rename a remote.
- `git remote set-url <name> <newurl>` – change URL.
- `git remote show <name>` – show information about a remote.
- `git remote prune <name>` – delete stale remote‑tracking branches.

**Examples**:

```bash
git remote -v
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)

git remote add upstream https://github.com/other/repo.git

git remote rename origin upstream

git remote set-url origin git@github.com:user/repo.git

git remote show origin
```

#### git fetch

Downloads objects and references from a remote repository without merging.

```bash
git fetch origin
# Fetches all branches from origin

git fetch origin main
# Fetches only main branch

git fetch --all
# Fetches from all remotes

git fetch --prune
# Remove any remote‑tracking branches that no longer exist on remote

git fetch --tags
# Fetch tags as well
```

#### git pull

Fetches from a remote and integrates (merges or rebases) into the current branch.

```bash
git pull origin main
# Fetch origin/main and merge into current branch

git pull --rebase origin main
# Fetch and rebase instead of merge

git pull --no-commit
# Pull but don't auto‑commit merge (staged)
```

**Common flags**:

- `--rebase` – use rebase instead of merge.
- `--ff-only` – only fast‑forward; abort if not possible.
- `--no-ff` – always create a merge commit (even if fast‑forward possible).
- `-v` – verbose.

#### git push

Uploads local commits to a remote repository.

```bash
git push origin main
# Push local main to origin/main

git push -u origin feature
# Push and set upstream, so later just 'git push' works

git push --all origin
# Push all branches

git push --tags
# Push tags

git push origin --delete feature
# Delete remote branch 'feature'

git push --force
# Force push (overwrite remote history) – use with extreme caution

git push --force-with-lease
# Safer force push: only overwrite if your local copy is up to date with remote
```

**Common flags**:

- `-u` (`--set-upstream`) – set upstream reference.
- `--delete` – delete a remote branch or tag.
- `--tags` – push tags.
- `--all` – push all branches.
- `--prune` – remove remote branches that don't exist locally.
- `--force` (`-f`) – force update (may lose commits).
- `--force-with-lease` – safer force push.
- `-n` (`--dry-run`) – show what would be pushed.

---

### 10. Tags

#### git tag

Creates, lists, or deletes tags.

**Common flags**:

- `-a` – create an annotated tag (requires message).
- `-m "message"` – message for annotated tag.
- `-d` – delete a tag.
- `-l` (`--list`) – list tags (default with pattern).
- `-v` – verify tag signature.
- `-f` – force (move an existing tag).

**Examples**:

```bash
git tag
# List tags

git tag -l "v1.*"
# List tags matching pattern

git tag v1.0.0
# Create lightweight tag

git tag -a v1.0.0 -m "Release version 1.0.0"
# Create annotated tag

git tag -d v1.0.0
# Delete local tag

git push origin v1.0.0
# Push a specific tag to remote

git push origin --tags
# Push all tags

git push origin --delete v1.0.0
# Delete remote tag
```

---

### 11. Inspection and Comparison

#### git blame

Shows who last modified each line of a file and in which commit.

```bash
git blame file.txt
# Annotates each line with commit hash, author, timestamp

git blame -L 10,20 file.txt
# Blame only lines 10 to 20

git blame -w
# Ignore whitespace changes

git blame -e
# Show author email instead of name

git blame -C
# Detect lines moved or copied from other files
```

#### git grep

Searches for patterns in tracked files.

```bash
git grep "TODO"
# Search all tracked files for "TODO"

git grep -n "function" -- *.js
# Show line numbers, only in .js files

git grep -c "error"
# Count occurrences per file

git grep -i "fixme"
# Case‑insensitive search

git grep -l "main"
# List only file names containing "main"
```

**Flags**: many like `grep` (e.g., `-w` for whole word, `-v` for invert match).

#### git diff (advanced)

Beyond basic diff, you can compare arbitrary objects and use advanced options.

**Comparing branches/tags/commits**:

```bash
git diff main..feature
# Changes from main to feature (same as git diff main feature)

git diff main...feature
# Changes in feature since it diverged from main (i.e., common ancestor)

git diff --cached HEAD~3
# Compare staged changes with a specific old commit
```

**Other useful diff flags**:

- `--word-diff` – shows word diff.
- `--color-words` – color‑coded word diff.
- `--stat` – summary.
- `--patch` (`-p`) – show full diff (default for commits).
- `--raw` – raw format.
- `--name-only` – only file names.
- `--name-status` – file names and status (A, M, D).
- `--ignore-space-change` (`-b`) – ignore whitespace changes.
- `--ignore-all-space` (`-w`) – ignore all whitespace.
- `--ignore-blank-lines` – ignore blank lines.
- `--diff-filter=ACMRTUXB` – only show files with certain status (e.g., `--diff-filter=M` for modified only).
- `--no-index` – compare two files outside a repo.

**Examples**:

```bash
git diff --word-diff
# Word diff

git diff --stat --ignore-space-change
# Summary with whitespace ignored

git diff --name-status HEAD~5 HEAD
# List files changed with status between two commits

git diff --diff-filter=M --name-only
# Names of files that were modified
```

---

### 12. Advanced Commands

#### git bisect

Uses binary search to find the commit that introduced a bug.

**Workflow**:

```bash
git bisect start
git bisect bad                 # Current commit is bad
git bisect good v1.0           # Known good commit
# Git checks out a middle commit. Test it.
git bisect good                # If this commit is good
git bisect bad                 # If this commit is bad
# Repeat until culprit is found.
git bisect reset               # End bisect and return to original branch
```

**Flags**:

- `git bisect visualize` – shows remaining commits in gitk.
- `git bisect run <script>` – automate testing with a script.

#### git submodule

Manages external repositories inside your repository.

**Commands**:

```bash
git submodule add https://github.com/user/lib.git libs/lib
# Adds submodule, creates .gitmodules

git submodule status
# Show status of submodules

git submodule update --init --recursive
# After cloning a repo with submodules, initialize and update them

git submodule foreach git pull origin main
# Run a command in each submodule
```

**Flags**:

- `--recursive` – operate on nested submodules.
- `--remote` – update to the latest commit on the remote branch.

#### git worktree

Lets you have multiple branches checked out in separate directories, sharing the same repository.

```bash
git worktree add ../hotfix hotfix-branch
# Create a new working tree for hotfix-branch in ../hotfix

git worktree list
# List all worktrees

git worktree remove ../hotfix
# Remove a worktree
```

---

### 13. Aliases and Customisation

You can create shortcuts for frequently used commands using Git aliases.

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

Now you can use `git co` instead of `git checkout`.

To include flags in aliases, you often need to use a shell command with `!`. Example:

```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
```

Aliases are stored in `~/.gitconfig`.

---

### 14. Summary of Common Flags

Here is a quick reference for frequently used flags across commands:

| Flag          | Meaning                                      | Commonly used with               |
|---------------|----------------------------------------------|----------------------------------|
| `-a`          | all (stage all, commit all, list all, etc.) | add, commit, branch              |
| `-m`          | message                                      | commit, tag, merge               |
| `-d`          | delete                                       | branch, tag, remote              |
| `-D`          | force delete                                 | branch                           |
| `-f`          | force                                        | rm, clean, push, branch          |
| `-i`          | interactive                                  | rebase, add                      |
| `-p`          | patch (interactive)                          | add, restore, log                |
| `-n`          | dry-run                                      | commit, clean, push              |
| `-v`          | verbose                                      | many commands                    |
| `-u`          | set upstream / update                        | push, add                        |
| `-c`          | copy / create                                | branch, switch                   |
| `-r`          | remote                                       | branch, log                      |
| `--amend`     | amend last commit                            | commit                           |
| `--cached`    | staging area                                 | diff, rm, restore                |
| `--hard`      | reset hard                                   | reset                            |
| `--soft`      | reset soft                                   | reset                            |
| `--mixed`     | reset mixed (default)                        | reset                            |
| `--staged`    | staging area                                 | diff, restore                    |
| `--oneline`   | compact log                                  | log                              |
| `--graph`     | show branch graph                            | log                              |
| `--decorate`  | show refs                                    | log                              |
| `--all`       | all branches/remotes                         | log, fetch, push                 |
| `--tags`      | include tags                                 | push, fetch                      |
| `--force-with-lease` | safer force push                      | push                             |
| `--prune`     | remove stale references                      | fetch, remote                    |
| `--rebase`    | rebase instead of merge                      | pull                             |

---

### Conclusion

This document has covered the vast majority of Git commands and their flags that you will encounter in daily development. By understanding each command’s options and practicing with the examples, you will be able to navigate Git with confidence, whether you are committing changes, inspecting history, branching, or undoing mistakes. Remember that `git help <command>` is always available for the most detailed and up‑to‑date information.

Mastering the command line interface to Git unlocks its full power and flexibility, making you a more effective and self‑reliant developer.