## Introduction to Version Control and Git

This document provides a comprehensive introduction to version control systems, focusing on Git—the most widely used distributed version control system today. It covers fundamental concepts, practical workflows, and techniques for undoing mistakes. By the end, you will have a solid understanding of how to manage code changes effectively, collaborate with teams, and recover from errors with confidence.

---

### 1. What is Version Control?

Version control (also known as revision control or source control) is a system that records changes to a file or set of files over time so that you can recall specific versions later. It allows multiple people to work on the same project concurrently, tracks who made what changes and when, and provides mechanisms to merge contributions and resolve conflicts.

**Why version control is essential:**

- **History tracking**: Every change is logged, enabling you to revert to any previous state.
- **Collaboration**: Multiple developers can work on the same codebase without overwriting each other’s work.
- **Branching and experimentation**: You can create isolated branches to try new ideas without affecting the main codebase.
- **Accountability**: Each change is attributed to an author, which aids in code reviews and debugging.
- **Backup and recovery**: The repository serves as a backup of your entire project history.

Version control systems fall into two categories:

- **Centralized (CVCS)**: A single central server stores all versions. Examples: Subversion (SVN), CVS.
- **Distributed (DVCS)**: Every contributor has a full copy of the repository, including its entire history. Examples: Git, Mercurial.

Git is a distributed system, meaning that every clone is a full‑fledged repository with complete history. This enables offline work and multiple remote backups.

---

### 2. Core Concepts in Git

Before diving into commands and workflows, it is crucial to understand Git’s fundamental building blocks.

#### 2.1 Repository

A **repository** (or “repo”) is a directory that contains your project files and the entire revision history. It is stored in a hidden `.git` folder at the root of your project. Repositories can be local (on your machine) or remote (hosted on services like GitHub, GitLab, Bitbucket).

#### 2.2 Working Directory, Staging Area, and Git Directory

Git manages files in three main states:

- **Working directory**: The actual files you see and edit on your file system.
- **Staging area** (also called index): A file that stores information about what will go into your next commit.
- **Git directory** (repository): Where Git stores the metadata and object database for your project. This is the `.git` folder.

The basic workflow is:

1. Modify files in your working directory.
2. Stage the changes, adding snapshots of them to the staging area.
3. Commit, which takes the files as they are in the staging area and stores that snapshot permanently in the Git directory.

#### 2.3 Commit

A **commit** is a snapshot of your repository at a specific point in time. Each commit has a unique SHA‑1 hash (e.g., `a1b2c3d...`), an author, a timestamp, a commit message, and a pointer to its parent commit(s). Commits form a directed acyclic graph, representing the project history.

#### 2.4 Branch

A **branch** is a movable pointer to a commit. The default branch is usually called `main` (or `master`). Creating a new branch allows you to diverge from the main line of development and work independently without affecting the main branch. Branches are lightweight and cheap in Git.

#### 2.5 Remote

A **remote** is a version of the repository hosted on another server. Common remote names are `origin` (the default) and `upstream`. Remotes enable collaboration: you push your local changes to a remote and pull changes from others.

#### 2.6 HEAD

**HEAD** is a special pointer that indicates the current branch or commit you are working on. Usually, it points to the latest commit in the current branch. When you switch branches, HEAD moves to the new branch’s latest commit.

---

### 3. Basic Git Commands: Getting Started

This section covers the essential commands you will use daily. They assume Git is installed and configured (see the previous document on Git Bash for installation).

#### 3.1 Configuration

Set your identity globally (one‑time setup):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Set your preferred text editor (e.g., VS Code):

```bash
git config --global core.editor "code --wait"
```

View configuration:

```bash
git config --list
```

#### 3.2 Creating a Repository

**From scratch**:

```bash
mkdir my-project
cd my-project
git init
```

This creates an empty Git repository with a `.git` folder.

**Cloning an existing repository**:

```bash
git clone https://github.com/user/repo.git
cd repo
```

#### 3.3 Making Your First Commit

1. Create or modify files.
2. Check the status:

```bash
git status
```

3. Stage files:

```bash
git add file1.txt file2.py
# Or stage all changes:
git add .
```

4. Commit with a message:

```bash
git commit -m "Initial commit: add README and main script"
```

#### 3.4 Viewing History

```bash
git log                # Full history
git log --oneline      # Compact one‑line view
git log --graph        # Show branch structure
```

#### 3.5 Comparing Changes

```bash
git diff                # Working directory vs staging
git diff --staged       # Staging vs last commit
git diff HEAD           # Working directory vs last commit
git diff commit1 commit2 # Between two commits
```

#### 3.6 Working with Remotes

Add a remote:

```bash
git remote add origin https://github.com/user/repo.git
```

View remotes:

```bash
git remote -v
```

Push changes to remote:

```bash
git push origin main
```

Pull changes from remote:

```bash
git pull origin main
```

Fetch changes without merging:

```bash
git fetch origin
```

#### 3.7 Branching and Merging

List branches:

```bash
git branch
```

Create a new branch:

```bash
git branch feature-xyz
```

Switch to a branch:

```bash
git checkout feature-xyz
# Or with newer Git:
git switch feature-xyz
```

Create and switch in one command:

```bash
git checkout -b feature-xyz
# Or:
git switch -c feature-xyz
```

Merge a branch into the current branch:

```bash
git checkout main
git merge feature-xyz
```

Delete a branch (after merging):

```bash
git branch -d feature-xyz
```

---

### 4. A Detailed Professional Git Workflow

A professional workflow ensures that code changes are integrated smoothly, reviewed properly, and released reliably. While many variations exist, the following is a robust and widely adopted approach.

#### 4.1 Workflow Overview

We will describe a workflow based on **feature branches**, **pull requests**, and **continuous integration**. This is commonly known as **GitHub Flow** or a simplified Git Flow.

- **Main branch**: `main` (or `master`) always contains production‑ready code. It should be stable and deployable at all times.
- **Feature branches**: Each new feature, bug fix, or experiment is developed in a dedicated branch branched off `main`.
- **Pull requests (PRs) / Merge requests**: When work on a feature branch is complete, a pull request is opened to merge the branch into `main`. This triggers code review and automated tests.
- **Merging**: After approval and successful tests, the branch is merged (often with a merge commit or by rebasing).
- **Releases**: Tags are used to mark release points (e.g., `v1.0.0`). For larger projects, a `develop` branch may be used as an integration branch, but we focus on a simpler flow.

#### 4.2 Step‑by‑Step Workflow

**Step 1: Start a new feature**

Ensure your local `main` is up to date:

```bash
git checkout main
git pull origin main
```

Create a feature branch with a descriptive name:

```bash
git checkout -b feature/user-authentication
```

**Step 2: Develop the feature**

Make changes, commit regularly with clear messages:

```bash
git add .
git commit -m "Add login form UI"
git commit -m "Implement authentication logic"
git commit -m "Add tests for login"
```

Push the branch to the remote repository to back up your work and enable collaboration:

```bash
git push -u origin feature/user-authentication
```

The `-u` flag sets the upstream, so subsequent pushes can be done with just `git push`.

**Step 3: Open a pull request**

Navigate to your Git hosting platform (GitHub, GitLab, etc.) and open a pull request from `feature/user-authentication` into `main`. Fill in the description, link any related issues, and request reviewers.

**Step 4: Code review and discussion**

Reviewers comment on the code, suggest changes, or approve. If changes are requested, you continue committing to the same branch and push. The pull request updates automatically.

**Step 5: Run automated checks**

Continuous integration (CI) services (e.g., GitHub Actions, Jenkins) run tests and linters on the pull request. Ensure all checks pass.

**Step 6: Merge the feature branch**

Once approved and all checks pass, merge the pull request. There are several merge methods:

- **Create a merge commit**: Preserves all commits and adds a merge commit. This is the default.
- **Squash and merge**: Combines all feature branch commits into a single commit on `main`. Keeps history clean.
- **Rebase and merge**: Rebases the feature branch onto the tip of `main` and then fast‑forwards. Results in a linear history.

Choose the method that aligns with your team’s conventions.

After merging, delete the feature branch (the platform usually offers a button to do so). Also delete the local branch:

```bash
git branch -d feature/user-authentication
```

**Step 7: Update local main**

After merging, update your local `main`:

```bash
git checkout main
git pull origin main
```

**Step 8: Release**

When you are ready to release, create a tag:

```bash
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

You may also create a release on the hosting platform, attaching release notes.

#### 4.3 Handling Hotfixes

If a critical bug appears in production, you need a fast fix without including other unreleased features. The hotfix workflow:

1. Branch from `main` (the production state) with a name like `hotfix/critical-bug`.
2. Fix the bug, commit, push.
3. Open a pull request into `main`.
4. After review and testing, merge.
5. Tag the new release (e.g., `v1.2.4`).
6. If you have a long‑running development branch (e.g., `develop`), also merge the hotfix into that branch to keep it up to date.

#### 4.4 Best Practices for a Professional Workflow

- **Write meaningful commit messages**: Follow the conventional format: a short summary (50 chars or less), a blank line, then a detailed description if needed. Use imperative tense (“Add feature” not “Added feature”).
- **Keep commits atomic**: Each commit should represent a single logical change. This makes history easier to understand and revert if needed.
- **Pull frequently**: Regularly integrate changes from `main` into your feature branch to reduce merge conflicts.
- **Use `.gitignore`**: Exclude build artifacts, dependencies, and sensitive files from version control.
- **Protect the main branch**: On your Git host, enable branch protection rules that require pull request reviews, passing CI checks, and up‑to‑date branches before merging.
- **Automate testing and linting**: Run tests automatically on every push to a pull request.
- **Document your workflow**: Have a `CONTRIBUTING.md` file that explains the process for new contributors.

---

### 5. Undoing Mistakes in Git

Git provides powerful tools to correct errors. Understanding these commands is essential for maintaining a clean and accurate history.

#### 5.1 Undoing Changes in the Working Directory

If you have modified a file but haven’t staged it, and you want to discard those changes and revert to the version in the last commit:

```bash
git restore file.txt
# Or older syntax:
git checkout -- file.txt
```

#### 5.2 Unstaging Files

If you accidentally staged a file (with `git add`) and want to unstage it, keeping your changes in the working directory:

```bash
git restore --staged file.txt
# Or:
git reset HEAD file.txt
```

#### 5.3 Amending the Last Commit

If you forgot to include a file or want to change the commit message of the most recent commit:

```bash
# After staging any missing changes
git commit --amend
```

This opens your editor to modify the message. If you don’t need to change the message but only add files:

```bash
git commit --amend --no-edit
```

**Caution**: Amending rewrites the commit and changes its hash. If you have already pushed the commit, force‑pushing (`git push --force`) will be required, which can cause problems for collaborators. Avoid amending commits that are already public unless you coordinate with your team.

#### 5.4 Reverting Commits

If you need to undo a commit that has already been pushed, use `git revert`. It creates a new commit that undoes the changes of a specified commit, preserving history.

```bash
git revert HEAD          # Revert the last commit
git revert abc1234       # Revert a specific commit by hash
```

Revert is safe because it does not rewrite history; it only adds a new commit.

#### 5.5 Resetting to a Previous State

`git reset` moves the current branch pointer to a different commit and optionally modifies the staging area and working directory. It is a powerful but potentially destructive command. The three modes are:

- **`--soft`**: Moves HEAD to the specified commit, but leaves the staging area and working directory unchanged. Changes from the undone commits become staged.
- **`--mixed`** (default): Moves HEAD and resets the staging area to match the specified commit, but leaves the working directory unchanged. Changes become unstaged.
- **`--hard`**: Moves HEAD, resets the staging area, and overwrites the working directory to match the specified commit. **Any uncommitted changes are lost forever.**

Examples:

```bash
git reset --soft HEAD~1      # Undo last commit, keep changes staged
git reset --mixed HEAD~1     # Undo last commit, unstage changes (keep in working dir)
git reset --hard HEAD~1      # Completely discard last commit and all changes
```

**Never use `git reset --hard` on commits that have been pushed**, as it rewrites history. If you must, you will need to force‑push, which is dangerous for shared branches.

#### 5.6 Recovering Lost Commits with Reflog

If you accidentally reset or delete a branch, you can often recover using the **reflog**. The reflog records when the tips of branches and other references were updated in your local repository.

```bash
git reflog
```

Find the commit hash you want to recover, then create a branch or reset to it:

```bash
git checkout -b recovered-branch abc1234
# Or
git reset --hard abc1234
```

The reflog is local and not shared, so it is a lifesaver for local mistakes.

#### 5.7 Cleaning Untracked Files

To remove untracked files and directories from your working directory (e.g., build artifacts):

```bash
git clean -n          # Preview what will be removed
git clean -f          # Force removal of untracked files
git clean -fd         # Remove untracked files and directories
```

Use with caution: `git clean` permanently deletes files not under version control.

#### 5.8 Undoing a Merge

If you have merged a branch and want to undo it, you have two options:

- **Revert the merge commit**: `git revert -m 1 <merge-commit>` (the `-m 1` specifies which parent to keep, usually the main branch). This creates a new commit that undoes the merge, but it makes future re‑merging of the same branch complicated.
- **Reset**: If the merge hasn’t been pushed, you can `git reset --hard ORIG_HEAD` (Git sets `ORIG_HEAD` to the previous state before the merge). For a cleaner approach after push, consider reverting.

#### 5.9 Interactive Rebase for History Editing

Sometimes you need to clean up your commit history before merging a feature branch. Interactive rebase allows you to reorder, squash, edit, or drop commits.

```bash
git rebase -i HEAD~3   # Rebase the last three commits
```

An editor opens with a list of commits and commands (pick, reword, squash, etc.). After saving, Git replays the commits according to your instructions.

**Warning**: Rebasing rewrites history. Only rebase commits that have not been pushed to a shared branch.

---

### 6. Advanced Git Concepts

#### 6.1 Git Hooks

Git hooks are scripts that run automatically before or after certain Git events (commit, push, etc.). They are stored in `.git/hooks/` and can enforce policies, run tests, or format code. Example pre‑commit hook to check for debug statements:

```bash
#!/bin/sh
# .git/hooks/pre-commit
if grep -n "debugger;" *.js; then
    echo "Error: debugger statements found. Commit aborted."
    exit 1
fi
```

Make the hook executable: `chmod +x .git/hooks/pre-commit`.

#### 6.2 Submodules

Submodules allow you to include another repository as a subdirectory within your project. Useful for managing dependencies.

```bash
git submodule add https://github.com/user/library.git libs/library
git submodule update --init --recursive
```

#### 6.3 Worktrees

Git worktrees let you have multiple branches checked out simultaneously in different directories, sharing the same repository. This is useful when you need to work on two features without stashing or cloning again.

```bash
git worktree add ../hotfix hotfix-branch
```

#### 6.4 Cherry‑picking

`git cherry-pick` applies a specific commit from one branch to another. Use it to bring a bug fix into multiple branches without merging everything.

```bash
git checkout release
git cherry-pick abc1234
```

#### 6.5 Stashing

`git stash` temporarily shelves changes you have made so you can work on something else, then reapply them later.

```bash
git stash                 # Stash changes (including untracked with -u)
git stash list            # List stashes
git stash pop             # Apply latest stash and remove it
git stash apply           # Apply but keep stash
git stash drop stash@{0}  # Delete a stash
```

---

### 7. Common Scenarios and Solutions

#### 7.1 Accidentally committed to the wrong branch

If you committed to `main` instead of a feature branch:

```bash
# Create the feature branch (it will contain the commit)
git branch feature-xyz
# Reset main to the previous commit
git reset --hard HEAD~1
# Switch to the feature branch
git switch feature-xyz
```

Now the commit lives on the feature branch, and `main` is clean.

#### 7.2 Need to undo a pushed commit that others have pulled

Use `git revert` to create an anti‑commit. This is safe for public history.

```bash
git revert HEAD
git push origin main
```

#### 7.3 Merge conflicts

When merging or pulling, Git may report conflicts. Open the conflicted files, look for `<<<<<<<`, `=======`, `>>>>>>>` markers, resolve the differences, then:

```bash
git add resolved-file.txt
git commit        # Git will create a merge commit automatically
```

#### 7.4 I want to see who changed a line

Use `git blame`:

```bash
git blame file.txt
```

#### 7.5 I want to find when a bug was introduced

Use `git bisect`:

```bash
git bisect start
git bisect bad HEAD          # Current commit is bad
git bisect good v1.0         # Known good commit
# Git checks out a middle commit. Test it, then:
git bisect good   # or bad
# Repeat until the culprit is found.
git bisect reset
```

---

### 8. Best Practices and Tips

- **Commit often**: Frequent commits make it easier to isolate changes and revert if needed.
- **Write descriptive commit messages**: Follow the convention: `<type>(<scope>): <subject>` (e.g., `feat(auth): add login endpoint`). Types include feat, fix, docs, style, refactor, test, chore.
- **Keep your history clean**: Use interactive rebase locally to squash fixup commits before merging a feature branch.
- **Protect main**: Enforce branch protection rules that require pull requests, reviews, and passing CI.
- **Use `.gitignore` effectively**: Ignore IDE files, build outputs, dependency directories (e.g., `node_modules/`), and environment files.
- **Stay up to date**: Regularly pull changes from the main branch into your feature branches to minimise conflicts.
- **Learn Git aliases**: Speed up common commands with aliases in `~/.gitconfig`:

```ini
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --oneline --graph --all --decorate
```

- **Use a graphical tool**: Tools like `gitk`, `git-gui`, or IDE integrations (VS Code, PyCharm) can help visualise the repository.

---

### 9. References and Further Reading

- **Official Git documentation**: [https://git-scm.com/doc](https://git-scm.com/doc)
- **Pro Git Book** (free): [https://git-scm.com/book/en/v2](https://git-scm.com/book/en/v2)
- **GitHub Flow**: [https://guides.github.com/introduction/flow/](https://guides.github.com/introduction/flow/)
- **GitLab Flow**: [https://docs.gitlab.com/ee/topics/gitlab_flow.html](https://docs.gitlab.com/ee/topics/gitlab_flow.html)
- **Conventional Commits**: [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/)
- **Atlassian Git Tutorials**: [https://www.atlassian.com/git/tutorials](https://www.atlassian.com/git/tutorials)

---

### 10. Summary

Version control with Git is an indispensable skill for modern software development. This guide has introduced the core concepts, provided a detailed professional workflow, and equipped you with the tools to recover from mistakes. By adopting a structured approach—using feature branches, pull requests, and continuous integration—you can collaborate effectively and maintain a high‑quality codebase. The ability to undo errors safely (using revert, reset, reflog, etc.) ensures that you can experiment without fear. With practice, these commands and workflows will become second nature, allowing you to focus on building great software.