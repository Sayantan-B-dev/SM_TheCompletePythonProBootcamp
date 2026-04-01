
# Step 2 - Authentication with Spotify

Before we can create playlists or search for tracks, we need to connect our Python application to your Spotify account. This step covers setting up a Spotify Developer application and implementing the OAuth authentication flow using the Spotipy library.

## 2.1 Prerequisites

- A **Spotify account** (free or premium).
- A registered application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
- The **Spotipy** library installed.

## 2.2 Register a Spotify App

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click **“Create App”**.
3. Fill in the details:
   - **App name**: `Musical Time Machine`
   - **App description**: `Create playlists from Billboard Hot 100 charts`
   - **Website** (optional): can be left blank or use `http://localhost`
   - **Redirect URI**: You must add at least one redirect URI. For local development, use:
     ```
     http://localhost:8888/callback
     ```
     (This is where Spotify will send the user after they authorize your app.)
4. Check the agreement box and click **“Save”**.
5. After creation, you’ll see your **Client ID** and **Client Secret** on the app’s dashboard. Keep these secret – they are your app’s credentials.

## 2.3 Set Up Environment Variables

We will store the credentials in a `.env` file to keep them out of the source code. Create a `.env` file in your project root:

```ini
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

Install `python-dotenv` to load these variables:

```bash
pip install python-dotenv
```

## 2.4 Install Spotipy

Spotipy is a lightweight Python library for the Spotify Web API.

```bash
pip install spotipy
```

## 2.5 Understanding the OAuth Flow

Spotify uses **OAuth 2.0** to grant permissions. Our application will request the following **scope**:

- `playlist-modify-private` – to create private playlists and add tracks to them.

The flow works like this:

1. Our app opens a browser window asking the user to log in to Spotify and grant the requested permissions.
2. After approval, Spotify redirects the user to our redirect URI with a **code** in the URL.
3. Our app exchanges that code for an **access token** (and a refresh token).
4. We use the access token to make API calls on behalf of the user.

Spotipy handles most of this complexity for us.

## 2.6 Implement Authentication

Create a new file `spotify_client.py`. We’ll write a function that returns an authenticated Spotipy client.

```python
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_spotify_client():
    """
    Creates and returns a Spotipy client authenticated with the user's credentials.
    The token is cached automatically by Spotipy.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise EnvironmentError("Missing Spotify credentials in .env file")

    # Define the required permissions
    scope = "playlist-modify-private"

    # Create OAuth object and get token
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path="token.txt",          # Caches the token locally
        show_dialog=True                  # Forces login each time (optional)
    ))

    return sp
```

**Explanation:**

- `SpotifyOAuth` handles the entire authorization flow.
- `cache_path` stores the token so you don’t have to log in every time you run the script.
- `show_dialog=True` is useful during development to test the flow repeatedly; you may remove it for production.

## 2.7 Test the Authentication

Add a test block to `spotify_client.py` to verify that authentication works:

```python
if __name__ == "__main__":
    sp = get_spotify_client()
    # Get the current user's information
    user = sp.current_user()
    print(f"Authenticated as: {user['display_name']} ({user['id']})")
```

Run the script:

```bash
python spotify_client.py
```

The first time you run it, a browser window will open asking you to log in and authorize the app. After granting permission, you’ll be redirected to a local URL that may show an error (because our app isn’t actually running a web server). That’s fine – Spotipy captures the code from the URL and exchanges it for a token. You should then see your Spotify display name printed in the terminal.

## 2.8 What We’ve Accomplished

- ✅ Created a Spotify App and obtained client credentials.
- ✅ Set up environment variables for secure storage.
- ✅ Implemented OAuth authentication using Spotipy.
- ✅ Successfully obtained an access token and verified it by fetching the current user.

Now we have a working connection to the Spotify API. In the next step, we’ll use this client to search for the songs we scraped from Billboard.

