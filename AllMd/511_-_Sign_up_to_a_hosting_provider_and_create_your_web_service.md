## Signing Up to a Hosting Provider and Creating a Web Service

This document provides a detailed, step‑by‑step guide to selecting a hosting provider for your Python web application, creating an account, and setting up a new web service. The primary focus is on **Render.com**, a popular platform with a generous free tier, but the concepts apply broadly to other providers. By the end of this guide, you will have a live (though not yet fully functional) web service connected to your GitHub repository, with the necessary start command and a first environment variable configured.

### Introduction to Hosting Providers

Once your application is ready and under version control on GitHub, the next step is to make it publicly accessible on the internet. This is achieved by deploying it to a **hosting provider** – a company that runs servers and provides the infrastructure to serve your application to users.

Many providers offer free tiers suitable for learning, prototyping, and small projects. The table below lists some popular Python‑friendly hosting platforms, their approximate monthly cost for a basic plan, and the plan name. Note that pricing and features can change over time; always refer to the provider’s official website for the most current information.

| Provider                | Approx. Cost / Month | Plan Name          |
|-------------------------|----------------------|--------------------|
| Heroku                  | $5                   | Eco                |
| Render                  | $0                   | Individual         |
| Cyclic                  | $0                   | Free Forever       |
| Glitch                  | $0                   | Starter            |
| Vercel                  | $0                   | Hobby              |
| PythonAnywhere          | $0                   | Beginner           |

For this tutorial, we will use **Render** because it offers a straightforward free tier, integrates seamlessly with GitHub, and provides a PostgreSQL database for free as well. The steps are similar for most other providers, so the knowledge is transferable.

### Prerequisites

Before you begin, ensure you have:

- A **GitHub account** and your project pushed to a GitHub repository (as covered in the previous lesson).
- Your project properly configured with:
  - A `requirements.txt` file containing all dependencies (including `gunicorn`).
  - A `Procfile` (if required by the provider; Render can detect a Python app without it, but it is recommended to have one).
  - Environment variables replaced in your code (using `os.environ.get()`).

### Step 1: Create an Account on Render

1. Open your browser and go to [render.com](https://render.com).
2. Click the **Sign Up** button (usually located in the top‑right corner).
3. You will be presented with several sign‑up options: using Google, GitHub, GitLab, or email. **Choosing GitHub is the most convenient** because it allows Render to automatically access your repositories later.
   - Click **Sign up with GitHub**.
   - If you are not already logged into GitHub, you will be prompted to sign in.
   - GitHub will ask you to authorize Render to access your account. Review the permissions (Render needs access to your public and private repositories if you plan to deploy private repos) and click **Authorize**.
4. After authorization, Render may ask for some additional information, such as your name and a confirmation email. Follow the on‑screen instructions to verify your email address.
5. Once your email is confirmed, you will be logged into the Render Dashboard. This is your central hub for managing all your Render services.

**Note:** If you prefer to sign up with email, you can do so, but you will need to manually connect your GitHub account later to access your repositories.

### Step 2: Create a New Web Service

With your Render account ready, you can now create a web service that will host your application.

1. From the Render Dashboard, click the **New +** button (usually at the top‑right) and select **Web Service** from the dropdown menu.
2. Render will ask you to connect a repository. If you signed up with GitHub, you should see your GitHub account listed. Click **Connect** next to your GitHub account. If you don’t see your repositories, you may need to configure GitHub integration by clicking the **Configure account** link and granting access to the specific repositories.
3. After connecting, a list of your GitHub repositories appears. Find the repository that contains your blog project (the one you pushed to GitHub) and click the **Connect** button next to it.

### Step 3: Configure the Web Service

Once you connect your repository, Render displays a configuration page where you can customise how your application will be built and run. The default settings are often sufficient, but you need to make a few adjustments.

- **Name**: Choose a unique name for your web service. This name will become part of your default Render URL (e.g., `https://your-app-name.onrender.com`). Pick something descriptive, like `my-blog-app`.
- **Region**: Select the geographic region closest to your target audience. For most users, the default (e.g., `Frankfurt (EU Central)`) is fine. This affects latency.
- **Branch**: Choose the branch you want to deploy. Typically, this is `main` or `master`.
- **Root Directory**: Leave this blank unless your application is in a subdirectory.
- **Runtime**: Render usually auto‑detects Python. If not, select `Python 3` (or the appropriate version).
- **Build Command**: Render will automatically set this to `pip install -r requirements.txt`. This is correct; you do not need to change it.
- **Start Command**: **This is a critical field.** By default, Render might try to run your app with `gunicorn <your-app>:app` but it may not guess correctly. You must explicitly set it to:

  ```
  gunicorn main:app
  ```

  Replace `main` with the name of your Python file (without `.py`) that contains the Flask application object. For example, if your app is in `blog.py` and the Flask instance is named `application`, you would write `gunicorn blog:application`. If you have a `Procfile`, Render will respect it, but setting the start command explicitly overrides the `Procfile` and ensures clarity.

- **Advanced Settings**: Click the **Advanced** button (below the start command field) to expand additional options. This is where you will add environment variables.

### Step 4: Add Environment Variables

Your application relies on environment variables for sensitive configuration (e.g., `FLASK_KEY`, `DB_URI`). In Render, you set these as **environment variables** in the Advanced section.

1. In the **Advanced** section, click **Add Environment Variable**.
2. For each variable your application needs, enter the **Key** and **Value**:
   - **Key**: `FLASK_KEY`
   - **Value**: A long, random secret string (you can generate one using Python: `import secrets; print(secrets.token_urlsafe(32))`). This should match the key you used in `os.environ.get('FLASK_KEY')`.
3. Add any other variables that do not depend on the database (which will be set up later). For example, if you have email credentials, you can add `MAIL_USERNAME` and `MAIL_PASSWORD` now.
4. **Do not add `DB_URI` yet** – you will obtain that after creating a PostgreSQL database in the next step. The application will fail to start if `DB_URI` is missing, but that is expected at this stage.

You can add multiple variables by clicking **Add Environment Variable** repeatedly.

### Step 5: Create the Web Service

After filling in the configuration, scroll to the bottom of the page and click **Create Web Service**.

Render will immediately start the deployment process. You will be redirected to the web service dashboard, where you can watch the live build logs. The process includes:

- Pulling your code from GitHub.
- Setting up a Docker container (or a lightweight environment) with the specified Python version.
- Running `pip install -r requirements.txt` to install dependencies.
- Starting your application with the command you provided (e.g., `gunicorn main:app`).

Because we have not yet set up the database and the `DB_URI` environment variable, the application will likely fail to start or show errors related to the database connection. This is **normal** at this point. The purpose of this step is to create the service and verify that the build process works. In the next lesson, you will create a PostgreSQL database and add its connection string as an environment variable, after which your application will run successfully.

### What Happens Next?

Once the web service is created, you will see a URL like `https://your-app-name.onrender.com`. Visiting this URL now will probably show an error page (e.g., “Application error” or a database connection issue). Do not worry – this is expected.

From the Render dashboard, you can:

- **View logs**: Click on the **Logs** tab to see the output of your application. This is invaluable for debugging.
- **Edit environment variables**: Go to the **Environment** tab to add, modify, or delete environment variables. Changes require a manual deploy or an automatic redeploy (depending on your settings).
- **Trigger manual deploys**: If you push new code to GitHub, Render can automatically redeploy (this is the default). You can also manually deploy from the dashboard.

### Additional Considerations

#### Custom Domain

Render allows you to add a custom domain (e.g., `www.yourdomain.com`) from the **Settings** tab. You will need to own the domain and update its DNS records as instructed by Render. This is typically done after your application is fully functional.

#### Automatic Deploys

By default, Render automatically deploys your service whenever you push changes to the connected branch. You can disable this behaviour in the settings if you prefer manual control.

#### Scaling and Free Tier Limits

The free tier on Render includes 750 hours of uptime per month (enough for a single service to run 24/7), 512 MB of RAM, and a shared CPU. If your service receives no traffic for a period (usually 15 minutes), it may spin down to save resources; the next request will wake it up, causing a slight delay. This is normal for free tiers.

#### Other Providers

Although this guide focuses on Render, the general workflow is similar for other providers:

- Heroku: Create an app, connect GitHub, set environment variables via `heroku config:set`, and deploy.
- PythonAnywhere: Set up a web app via the dashboard, configure the WSGI file, and set environment variables (though the free plan has limited options).
- Cyclic: Similar to Render, with a focus on simplicity.

Always consult the provider’s official documentation for the most accurate and up‑to‑date instructions.

### Conclusion

You have now successfully:

- Signed up for a Render account.
- Created a new web service linked to your GitHub repository.
- Configured the start command to use Gunicorn.
- Added a first environment variable (`FLASK_KEY`).
- Initiated the deployment process.

Your web service is now provisioned and ready for the next step: adding a PostgreSQL database and the corresponding `DB_URI` environment variable. After that, your application will be fully functional and publicly accessible. The logs and dashboard provide all the tools you need to monitor and manage your deployed application.

Proceed to the next lesson to set up your database and complete the deployment.