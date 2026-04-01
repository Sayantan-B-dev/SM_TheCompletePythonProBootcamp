## Pushing Your Local Repository to GitHub

This document provides a comprehensive guide to linking your PyCharm project with GitHub and pushing your local Git repository to a remote repository on GitHub. By following these steps, you will make your code available on GitHub, enabling collaboration, backup, and deployment. The guide covers both the PyCharm graphical interface and the underlying Git commands, ensuring you understand what happens at each stage.

### Prerequisites

Before you begin, ensure you have the following:

- A **GitHub account**. If you do not have one, sign up at [github.com](https://github.com/join).
- **Git installed** on your system and accessible from the command line. PyCharm uses the system Git installation.
- **PyCharm** (Community or Professional edition) with your project open. Your project must already be under local Git version control (i.e., you have initialized a repository and made at least one commit). If you haven’t done so, refer to the previous lesson on adding version control.
- A **stable internet connection** to communicate with GitHub.

### Step 1: Link PyCharm with Your GitHub Account

PyCharm can integrate directly with GitHub, allowing you to perform remote operations without leaving the IDE. The first step is to authenticate PyCharm with your GitHub account.

1. Open PyCharm and go to **File** → **Settings** (on Windows/Linux) or **PyCharm** → **Preferences** (on macOS).
2. In the settings window, use the search bar at the top left and type **github**. This filters the settings to show GitHub-related options.
   - Alternatively, navigate to **Version Control** → **GitHub** manually.
3. In the GitHub settings pane, you will see a list of accounts (initially empty). Click the **+** (plus) sign to add a new account.
4. Choose the authentication method. The two most common are:
   - **Log in via GitHub** – This opens a browser window where you can authorize PyCharm to access your GitHub account. This is the recommended and simplest method.
   - **Use token** – If you prefer, you can generate a personal access token on GitHub and paste it here.
5. If you choose **Log in via GitHub**, a browser window will open asking you to sign in to GitHub (if not already signed in) and authorize the JetBrains IDE. Click **Authorize**.
6. After successful authorization, the browser will display a message that you can close. PyCharm will automatically detect the account and display it in the GitHub settings window.

   You should now see your GitHub username and avatar, confirming the connection.

   **Note:** If you encounter any issues, ensure that your firewall or antivirus is not blocking the connection, and that you are using a supported browser.

### Step 2: Share Your Project on GitHub

With PyCharm linked to your GitHub account, you can now create a remote repository and push your local commits.

1. In the main menu, go to **Git** → **GitHub** → **Share Project on GitHub**.
   - If you do not see the **Git** menu, ensure that your project is under Git version control (VCS → Enable Version Control Integration should already be done). The menu changes from **VCS** to **Git** once a Git repository is detected.

2. A dialog box titled **Share Project on GitHub** will appear. It contains the following fields:
   - **Repository name**: Choose a name for your remote repository. This can be any name, but it is common to use the same name as your project folder. Avoid spaces and special characters; use hyphens or underscores if needed.
   - **Remote**: The name of the remote reference in your local Git configuration. The default is `origin`, which is the conventional name for the primary remote repository.
   - **Description**: (Optional) A short description of your project. This will appear on the GitHub repository page.
   - **Private**: Check this box if you want the repository to be private (visible only to you and collaborators you explicitly add). If unchecked, the repository will be public (visible to everyone). Choose according to your needs.
   - **Remote URL**: PyCharm will show the predicted URL (e.g., `https://github.com/yourusername/repository-name.git`). This is informational.

3. After filling in the details, click the **Share** button.

   PyCharm now performs several actions in the background:
   - It connects to GitHub and creates a new repository with the specified name and visibility.
   - It adds this repository as a remote named `origin` to your local Git configuration.
   - It pushes your current local branch (usually `main` or `master`) to the remote, setting up the upstream tracking branch.

4. A progress dialog may appear, showing the status of the operation. If successful, you will see a confirmation message. If any errors occur (e.g., repository name already exists, network issues), an error message will explain the problem.

### Step 3: Verify the Push on GitHub

To confirm that your code is now on GitHub:

1. Open a web browser and go to [github.com](https://github.com). Sign in if necessary.
2. Navigate to your profile or repositories list. You should see the newly created repository with the name you specified.
3. Click on the repository to view its contents. You will see all the files and folders from your local project, along with your initial commit message.

   The repository page displays the commit history, branch information, and options to clone or download the code.

### What Happened Behind the Scenes (Git Commands)

For those who prefer the command line or want to understand the underlying operations, here are the equivalent Git commands that PyCharm executed:

```bash
# Add the remote repository (if it were created manually)
git remote add origin https://github.com/yourusername/repository-name.git

# Push the current branch to the remote and set upstream
git push -u origin main
```

If the remote repository does not exist, you would need to create it manually on GitHub first, then add the remote and push. PyCharm automates the creation step.

### Troubleshooting Common Issues

- **Authentication Failed**: If PyCharm cannot authenticate, try re-adding your GitHub account in settings. Ensure that your token (if using) has the necessary scopes (`repo` for full control of private repositories, `public_repo` for public repositories).
- **Repository Name Already Exists**: GitHub requires unique repository names within your account. If the name you chose is already taken, you will see an error. Choose a different name.
- **Push Rejected**: If your local repository has commits that are not compatible with the remote (e.g., you accidentally created a repository with a README on GitHub first), you may need to pull and merge. However, when using "Share Project on GitHub", PyCharm creates an empty repository, so this should not happen. If you do encounter a rejection, you can manually resolve it using the command line.
- **Network Issues**: Firewalls or VPNs may block the connection. Check your internet connection and try again.

### Next Steps

With your code now on GitHub, you have a remote backup and a collaboration point. The next logical steps are:

- **Clone the repository** on another machine if needed.
- **Invite collaborators** to your project via the GitHub repository settings.
- **Set up continuous integration / deployment** using GitHub Actions or connect to a hosting platform like Render or Heroku.
- **Continue developing** locally, committing changes, and pushing them regularly to keep the remote up to date.

To push subsequent changes, you can use PyCharm's **Git** → **Push** (or `Ctrl+Shift+K` / `Cmd+Shift+K`) to send your new commits to GitHub.

### Additional Resources

- [GitHub Help: Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [PyCharm Documentation: Using GitHub](https://www.jetbrains.com/help/pycharm/github.html)
- [Git Documentation: git push](https://git-scm.com/docs/git-push)

---

By completing this guide, you have successfully published your project to GitHub, making it accessible from anywhere and ready for the next stages of development and deployment.