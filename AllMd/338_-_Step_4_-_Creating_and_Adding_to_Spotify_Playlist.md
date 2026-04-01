
# Step 4 - Creating and Adding to Spotify Playlist

In this final step, we will bring everything together. We’ll create a new private Spotify playlist named after the user’s chosen date, then add all the successfully found tracks to it. This step also covers batching (because Spotify limits each `add_items` call to 100 tracks), error handling, and finally building a complete command‑line interface (CLI) that runs the whole workflow. Additionally, we will present an optional Flask web interface for those who prefer a browser‑based experience.

By the end of this step, you will have a fully functional **Musical Time Machine** that automatically generates a Billboard Hot 100 playlist for any date you choose.

---

## 4.1 Prerequisites

Make sure you have completed **Steps 1–3** and that the following modules are ready:

- `scraper.py` – contains `fetch_songs(date)` returning a list of song titles (or list of dicts with artist).
- `spotify_client.py` – contains `get_spotify_client()` and `collect_track_uris(sp, song_titles)`.
- A valid `.env` file with your Spotify credentials.

Install any missing dependencies (if not already done):

```bash
pip install requests beautifulsoup4 spotipy python-dotenv
```

---

## 4.2 Creating a Playlist

Spotify’s API endpoint to create a playlist requires the **user ID** and a **name**. The playlist will be private by default unless you specify `public=True`. We’ll keep it private as we only need it for personal use.

In `spotify_client.py`, add the following function:

```python
def create_playlist(sp, name, description=""):
    """
    Create a new private playlist for the authenticated user.
    Returns the playlist ID.
    """
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False,
        description=description
    )
    return playlist["id"]
```

**Explanation**:

- `sp.current_user()` fetches the user’s profile; we extract the `id`.
- `sp.user_playlist_create()` returns a dictionary containing the new playlist’s metadata. We only need the `id` for adding tracks.

---

## 4.3 Adding Tracks to a Playlist

Adding tracks is straightforward with `sp.playlist_add_items(playlist_id, track_uris)`. However, Spotify imposes a limit of **100 tracks per request**. Since we have at most 100 songs, we could send them all at once, but it’s good practice to write a function that batches the URIs in case the list exceeds 100 (for example, if we later expand to multiple charts). We’ll also include a small delay between batches to avoid hitting rate limits.

Add this function to `spotify_client.py`:

```python
def add_tracks_to_playlist(sp, playlist_id, track_uris):
    """
    Add a list of track URIs to a playlist, handling batching (max 100 per request).
    """
    batch_size = 100
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        sp.playlist_add_items(playlist_id, batch)
        print(f"Added batch {i//batch_size + 1}: {len(batch)} tracks")
```

If you want to be extra careful, you could add a `time.sleep(0.5)` after each batch.

---

## 4.4 The Orchestrator – Building the Playlist

Now we need a function that ties all the pieces together:

1. Scrape the Billboard Hot 100 for the given date.
2. Authenticate with Spotify.
3. Search for each song and collect valid URIs.
4. Create a new playlist named after the date.
5. Add the URIs to the playlist.
6. Report success/failure.

Create a new file `playlist_builder.py` (or add this to a main script). We’ll call it `main.py` for the CLI.

### 4.4.1 Full Orchestrator Code

```python
# main.py (or playlist_builder.py)
import sys
import logging
from scraper import fetch_songs
from spotify_client import get_spotify_client, collect_track_uris, create_playlist, add_tracks_to_playlist

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_playlist(date):
    """
    Main workflow: scrape -> authenticate -> search -> create playlist -> add tracks.
    Returns True if playlist was created successfully, False otherwise.
    """
    # Step 1: Scrape Billboard
    logging.info(f"Scraping Billboard Hot 100 for {date}...")
    try:
        songs = fetch_songs(date)
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return False

    if not songs:
        logging.error("No songs found. Check the date format or Billboard's HTML structure.")
        return False

    logging.info(f"Found {len(songs)} songs.")

    # Step 2: Authenticate with Spotify
    logging.info("Authenticating with Spotify...")
    try:
        sp = get_spotify_client()
    except Exception as e:
        logging.error(f"Spotify authentication failed: {e}")
        return False

    # Step 3: Search for tracks
    logging.info("Searching for tracks on Spotify...")
    track_uris = collect_track_uris(sp, songs)   # returns list of URIs
    if not track_uris:
        logging.error("No tracks could be found on Spotify. Aborting.")
        return False

    logging.info(f"Found {len(track_uris)} tracks on Spotify.")

    # Step 4: Create playlist
    playlist_name = f"Billboard Hot 100 - {date}"
    playlist_description = f"Top 100 songs from Billboard Hot 100 on {date}."
    logging.info(f"Creating playlist: {playlist_name}")
    try:
        playlist_id = create_playlist(sp, playlist_name, playlist_description)
    except Exception as e:
        logging.error(f"Playlist creation failed: {e}")
        return False

    # Step 5: Add tracks
    logging.info("Adding tracks to playlist...")
    try:
        add_tracks_to_playlist(sp, playlist_id, track_uris)
    except Exception as e:
        logging.error(f"Adding tracks failed: {e}")
        return False

    # Success
    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    logging.info(f"✅ Playlist created successfully: {playlist_url}")
    return True

if __name__ == "__main__":
    # Simple CLI: read date from command line argument or prompt
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = input("Enter date (YYYY-MM-DD): ").strip()

    success = build_playlist(date)
    sys.exit(0 if success else 1)
```

**Notes**:

- We use `logging` instead of `print` for better control.
- Error handling is added at each step; the function returns `False` on failure.
- The playlist URL is printed so the user can click and open it.

---

## 4.5 Complete File and Folder Structure

Here is the full project structure after implementing all steps, including the optional Flask web app (which we’ll describe later).

```
musical_time_machine/
│
├── .env.example              # Template for environment variables
├── .gitignore                # Ignore .env, token.txt, __pycache__, etc.
├── requirements.txt          # All Python dependencies
├── README.md                 # Project description and usage
│
├── scraper.py                # Billboard scraping logic
├── spotify_client.py         # Spotify authentication and API calls
├── playlist_builder.py       # Orchestrator (can be main.py instead)
├── cli.py                    # Command-line entry point (optional, could be main.py)
├── utils.py                  # Helper functions (date validation, logging setup)
│
├── web/                      # Optional Flask web application
│   ├── __init__.py
│   ├── app.py                # Flask routes
│   ├── templates/
│   │   └── index.html        # Simple form for date input
│   └── static/                # CSS, JS (optional)
│
└── tests/                    # Unit tests
    ├── test_scraper.py
    ├── test_spotify_client.py
    └── test_playlist_builder.py
```

### 4.5.1 File Contents

Below are the complete contents of each essential file.

#### `.env.example`

```ini
# Spotify API credentials – replace with your own
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

#### `requirements.txt`

```
requests==2.31.0
beautifulsoup4==4.12.2
spotipy==2.23.0
python-dotenv==1.0.0
flask==2.3.3          # optional, for web UI
pytest==7.4.0         # optional, for testing
```

#### `scraper.py` (with artist extraction – enhanced version)

```python
import requests
from bs4 import BeautifulSoup

def fetch_songs(date):
    """
    Scrapes Billboard Hot 100 for the given date.
    Returns a list of dictionaries with 'title' and 'artist'.
    """
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # Selectors – update if Billboard changes their markup
    title_elements = soup.select("h3.c-title.a-no-trucate")
    artist_elements = soup.select("span.c-label.a-no-trucate")

    # Ensure we have the same number of titles and artists
    # Sometimes the first few elements are not songs (e.g., weekly recap)
    # We'll zip them and take the first 100 pairs.
    songs = []
    for title_elem, artist_elem in zip(title_elements, artist_elements):
        title = title_elem.get_text(strip=True)
        artist = artist_elem.get_text(strip=True)
        if title and artist:
            songs.append({"title": title, "artist": artist})
        if len(songs) == 100:
            break

    return songs
```

#### `spotify_client.py`

```python
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    """Returns an authenticated Spotipy client."""
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    if not all([client_id, client_secret, redirect_uri]):
        raise EnvironmentError("Missing Spotify credentials in .env file")

    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path="token.txt",
        show_dialog=True
    ))
    return sp

def search_track(sp, track_name, artist_name=None):
    """
    Search for a track, optionally including artist name for better precision.
    Returns URI if found, else None.
    """
    query = f"track:{track_name}"
    if artist_name:
        query += f" artist:{artist_name}"

    results = sp.search(q=query, type='track', limit=1)
    items = results['tracks']['items']
    if items:
        return items[0]['uri']
    return None

def collect_track_uris(sp, songs):
    """
    songs: list of dicts with 'title' and 'artist' (or just strings if artist not available)
    Returns list of URIs and prints warnings for not found.
    """
    track_uris = []
    not_found = []

    for song in songs:
        if isinstance(song, dict):
            title = song['title']
            artist = song.get('artist')
        else:
            title = song
            artist = None

        uri = search_track(sp, title, artist)
        if uri:
            track_uris.append(uri)
        else:
            not_found.append(f"{title} - {artist}" if artist else title)
            print(f"⚠️  Could not find: {title}" + (f" by {artist}" if artist else ""))

        time.sleep(0.1)  # be polite to the API

    if not_found:
        print(f"\nTotal songs not found: {len(not_found)}")
    return track_uris

def create_playlist(sp, name, description=""):
    """Create a private playlist and return its ID."""
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=False,
        description=description
    )
    return playlist["id"]

def add_tracks_to_playlist(sp, playlist_id, track_uris):
    """Add tracks in batches of 100."""
    batch_size = 100
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i+batch_size]
        sp.playlist_add_items(playlist_id, batch)
        print(f"Added batch {i//batch_size + 1}: {len(batch)} tracks")
```

#### `playlist_builder.py` (or `main.py`)

```python
import sys
import logging
from scraper import fetch_songs
from spotify_client import get_spotify_client, collect_track_uris, create_playlist, add_tracks_to_playlist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_playlist(date):
    """Main workflow."""
    logging.info(f"Scraping Billboard Hot 100 for {date}...")
    try:
        songs = fetch_songs(date)
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return False

    if not songs:
        logging.error("No songs found. Check the date format or Billboard's HTML structure.")
        return False

    logging.info(f"Found {len(songs)} songs.")

    logging.info("Authenticating with Spotify...")
    try:
        sp = get_spotify_client()
    except Exception as e:
        logging.error(f"Spotify authentication failed: {e}")
        return False

    logging.info("Searching for tracks on Spotify...")
    track_uris = collect_track_uris(sp, songs)
    if not track_uris:
        logging.error("No tracks could be found on Spotify. Aborting.")
        return False

    logging.info(f"Found {len(track_uris)} tracks on Spotify.")

    playlist_name = f"Billboard Hot 100 - {date}"
    playlist_description = f"Top 100 songs from Billboard Hot 100 on {date}."
    logging.info(f"Creating playlist: {playlist_name}")
    try:
        playlist_id = create_playlist(sp, playlist_name, playlist_description)
    except Exception as e:
        logging.error(f"Playlist creation failed: {e}")
        return False

    logging.info("Adding tracks to playlist...")
    try:
        add_tracks_to_playlist(sp, playlist_id, track_uris)
    except Exception as e:
        logging.error(f"Adding tracks failed: {e}")
        return False

    playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
    logging.info(f"✅ Playlist created successfully: {playlist_url}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = input("Enter date (YYYY-MM-DD): ").strip()

    success = build_playlist(date)
    sys.exit(0 if success else 1)
```

#### `utils.py` (optional – date validation)

```python
import re
from datetime import datetime

def validate_date(date_str):
    """Check if date is in YYYY-MM-DD format and is a real date."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
```

You can integrate this validation into `build_playlist` or the CLI.

#### `cli.py` (alternative entry point)

This can be a thin wrapper around `playlist_builder.build_playlist` with argument parsing.

```python
import argparse
from playlist_builder import build_playlist
from utils import validate_date

def main():
    parser = argparse.ArgumentParser(description="Create a Spotify playlist from Billboard Hot 100 chart.")
    parser.add_argument("date", help="Date in YYYY-MM-DD format")
    args = parser.parse_args()

    if not validate_date(args.date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return 1

    success = build_playlist(args.date)
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
```

#### `web/app.py` (Flask web application)

If you choose to build the optional web interface, here’s a basic implementation using Flask. It stores the Spotify token in the session and runs the playlist building in a background thread to avoid timeout. For simplicity, this example runs synchronously (may timeout for long operations). A production version would use a task queue.

```python
import os
import threading
from flask import Flask, render_template, request, session, redirect, url_for, flash
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from playlist_builder import build_playlist  # but we need to modify to work with web

app = Flask(__name__)
app.secret_key = os.urandom(24)  # replace with a fixed key in production

# Spotify OAuth setup (same as before, but we'll manage the token in session)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def get_spotify_client_web():
    """Get Spotipy client using session-based token cache."""
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True
    )
    if request.args.get("code"):
        # Step 2: being redirected from Spotify auth page
        auth_manager.get_access_token(request.args["code"])
        return spotipy.Spotify(auth_manager=auth_manager)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1: display sign in link
        auth_url = auth_manager.get_authorize_url()
        return None, auth_url

    return spotipy.Spotify(auth_manager=auth_manager), None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    date = request.form['date']
    # Validate date...

    # Get authenticated client
    sp_or_url = get_spotify_client_web()
    if isinstance(sp_or_url, tuple):
        sp, auth_url = sp_or_url
        if auth_url:
            return redirect(auth_url)
    else:
        sp = sp_or_url

    # Now run the playlist building (this may take a while)
    # For simplicity, we run synchronously; consider using a background task.
    try:
        # We need to adapt build_playlist to accept an existing sp client
        # and possibly run asynchronously.
        # For this example, we'll just call a modified version.
        from scraper import fetch_songs
        from spotify_client import collect_track_uris, create_playlist, add_tracks_to_playlist

        songs = fetch_songs(date)
        track_uris = collect_track_uris(sp, songs)
        playlist_id = create_playlist(sp, f"Billboard Hot 100 - {date}")
        add_tracks_to_playlist(sp, playlist_id, track_uris)
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
        flash(f"Playlist created! <a href='{playlist_url}' target='_blank'>Open in Spotify</a>", "success")
    except Exception as e:
        flash(f"Error: {e}", "error")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

**Note**: The above web code is simplified and may need adjustments (e.g., handling token refresh, background tasks). It serves as a starting point.

#### `web/templates/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Musical Time Machine</title>
</head>
<body>
    <h1>Musical Time Machine</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="{{ category }}">{{ message|safe }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <form action="/create" method="post">
        <label for="date">Enter a date (YYYY-MM-DD):</label>
        <input type="text" id="date" name="date" placeholder="1999-06-12" required>
        <button type="submit">Create Playlist</button>
    </form>
</body>
</html>
```

#### `tests/test_scraper.py` (example unit test)

```python
import pytest
from scraper import fetch_songs

def test_fetch_songs_valid_date():
    songs = fetch_songs("1999-06-12")
    assert len(songs) == 100
    assert all("title" in song and "artist" in song for song in songs)

def test_fetch_songs_invalid_date():
    with pytest.raises(Exception):
        fetch_songs("invalid-date")
```

---

## 4.6 Function Flow

Below is a textual representation of the program’s control flow.

1. **User provides a date** (via CLI argument or prompt).
2. **`build_playlist(date)`** is called.
3. **Scraping**:
   - `scraper.fetch_songs(date)` constructs the Billboard URL, sends a GET request, parses HTML, extracts title and artist, and returns a list of dictionaries.
4. **Authentication**:
   - `spotify_client.get_spotify_client()` loads credentials, sets up OAuth, returns an authenticated Spotipy client. If no cached token exists, the user is prompted to authorize via browser (Spotipy handles this automatically).
5. **Track Search**:
   - `spotify_client.collect_track_uris(sp, songs)` iterates over each song.
   - For each song, `search_track(sp, title, artist)` performs a Spotify search and returns a URI if found.
   - URIs are collected; not‑found songs are logged.
6. **Playlist Creation**:
   - `spotify_client.create_playlist(sp, name, description)` gets the user’s ID and creates a private playlist, returning its ID.
7. **Add Tracks**:
   - `spotify_client.add_tracks_to_playlist(sp, playlist_id, track_uris)` splits the URIs into batches of 100 and calls `sp.playlist_add_items()` for each batch.
8. **Success**:
   - A playlist URL is constructed and logged/printed.

All steps include error handling that aborts the process and returns `False` if any critical failure occurs.

---

## 4.7 Running the CLI

1. Make sure your `.env` file is set up correctly.
2. Run the script:
   ```bash
   python playlist_builder.py 1999-06-12
   ```
   or without argument (it will prompt):
   ```bash
   python playlist_builder.py
   ```
3. On first run, a browser window will open asking you to authorize the app. After authorizing, you will be redirected to a local URL that may show an error (this is normal – Spotipy captures the code from the URL).
4. The script will then scrape, search, and create the playlist. You’ll see log messages and finally the playlist URL.
5. Open the URL in Spotify (desktop or web) to enjoy your new playlist!

---

## 4.8 Optional: Running the Flask Web App

1. Install Flask if you haven’t: `pip install flask`.
2. Set the same environment variables (`.env`).
3. Run the Flask app:
   ```bash
   python web/app.py
   ```
4. Visit `http://localhost:5000` in your browser.
5. Enter a date and click “Create Playlist”. If not authenticated, you’ll be redirected to Spotify to log in and authorize.
6. After authorization, the playlist creation will run (this may take a few seconds) and you’ll see a success message with a link to the playlist.

**Important**: The synchronous version may timeout if the playlist creation takes too long (e.g., more than 30 seconds). For a production web app, consider using a background task queue (Celery, Redis Queue) and polling for results.

---

## 4.9 Testing and Quality Assurance

- **Unit tests** should cover each module independently, mocking external calls (requests, Spotipy).
- **Integration tests** can be run against a test Spotify account with a dedicated test playlist that you delete after testing.
- **Manual testing** with various dates (including edge cases like very old charts that may have fewer than 100 songs or different HTML structures) ensures robustness.

Example pytest command:
```bash
pytest tests/
```

---

## 4.10 What We’ve Accomplished

- ✅ Created a private Spotify playlist with a descriptive name.
- ✅ Added tracks in batches, handling Spotify’s API limits.
- ✅ Integrated all previous steps into a seamless workflow.
- ✅ Built a user‑friendly CLI.
- ✅ (Optional) Created a basic web interface using Flask.
- ✅ Established a complete, well‑structured project with documentation and tests.

---

## 4.11 Next Steps & Enhancements

- **Improve search accuracy**: Use the artist name in the search query (already implemented in the enhanced scraper).
- **Handle missing tracks**: Optionally search for a different version (e.g., remastered) or prompt the user.
- **Support other charts**: Extend the scraper to work with other Billboard charts (e.g., Country, Rock).
- **Collaborative playlists**: Allow users to make the playlist public or collaborative.
- **Deploy the Flask app** to a cloud platform (Heroku, PythonAnywhere) and set up a proper task queue.
- **Add a progress bar** during search and addition for a better CLI experience.

Congratulations – you have built a complete **Musical Time Machine**! 🎉

