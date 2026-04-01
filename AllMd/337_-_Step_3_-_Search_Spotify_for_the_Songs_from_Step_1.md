
# Step 3 - Search Spotify for the Songs from Step 1

Now that we have a working Spotify connection and a list of song titles from Billboard, we need to find each track’s unique identifier (URI) on Spotify. This step focuses on searching Spotify for each song and collecting the URIs that we’ll later add to a playlist.

## 3.1 Search Strategy

Spotify’s search API allows us to look for tracks by name. The simplest approach is to pass the song title as a query and take the first result. However, this can sometimes return the wrong song (e.g., a cover version or a different track with the same name). To improve accuracy, we can include the artist’s name if we have it.

**Note:** Our current scraper from Step 1 only extracts song titles. If you want more precise matches, consider modifying the scraper to also grab the artist names. We’ll discuss that as an optional enhancement later. For now, we’ll search using only the title.

## 3.2 Update the Scraper (Optional but Recommended)

If you’d like to include artists, update your `scraper.py` to extract both title and artist. The Billboard page typically lists the artist in a separate element. For example, the artist might be in a `<span>` with class `c-label`. Here’s a quick modification:

```python
# In scraper.py, inside fetch_songs:
title_elements = soup.select("h3.c-title.a-no-trucate")
artist_elements = soup.select("span.c-label.a-no-trucate")  # example selector

songs = []
for title_elem, artist_elem in zip(title_elements, artist_elements):
    title = title_elem.get_text(strip=True)
    artist = artist_elem.get_text(strip=True)
    songs.append({"title": title, "artist": artist})
```

If you do this, you’ll have a list of dictionaries instead of just strings. For the rest of this guide, we’ll assume we have only the titles, but we’ll note where you can adapt the code to use artists.

## 3.3 Implement the Search Function

In `spotify_client.py`, we’ll add a function `search_track(sp, track_name)` that:

- Calls `sp.search()` with the query.
- Extracts the first track’s URI from the response.
- Returns `None` if no track is found.

```python
def search_track(sp, track_name):
    """
    Search for a track by name and return its Spotify URI.
    If multiple results, the first one is returned.
    Returns None if no track is found.
    """
    results = sp.search(q=track_name, type='track', limit=1)
    items = results['tracks']['items']
    if items:
        return items[0]['uri']
    else:
        return None
```

**Parameters explained:**

- `q=track_name` – the search query.
- `type='track'` – we only want tracks.
- `limit=1` – we only need the top result.

## 3.4 Process the List of Songs

Now we need to loop over all song titles from the scraper, call `search_track()` for each, and collect the URIs. We’ll also keep track of songs that couldn’t be found.

Create a new function (maybe in a separate module `playlist_builder.py` or in `spotify_client.py`) that does this:

```python
def collect_track_uris(sp, song_titles):
    """
    Given a list of song titles, search Spotify for each and return a list of valid URIs.
    Prints a warning for any song not found.
    """
    track_uris = []
    not_found = []

    for title in song_titles:
        uri = search_track(sp, title)
        if uri:
            track_uris.append(uri)
        else:
            not_found.append(title)
            print(f"⚠️  Could not find: {title}")

    if not_found:
        print(f"\nTotal songs not found: {len(not_found)}")
    return track_uris
```

If you have artist information, you can improve the query:

```python
query = f"track:{title} artist:{artist}"   # More specific search
```

## 3.5 Rate Limiting and Batching

Spotify API has rate limits, but for a single user searching 100 songs, you’re unlikely to hit them. However, if you plan to run many searches in quick succession, you might want to add a small delay between requests. You can do this with `time.sleep(0.1)`.

If you’re using Spotipy, it handles retries automatically, but adding a tiny sleep is polite:

```python
import time

for title in song_titles:
    uri = search_track(sp, title)
    # ... 
    time.sleep(0.1)   # 100ms delay
```

## 3.6 Testing the Search

Let’s test our search function with a small list. Create a temporary test script or add a `if __name__ == "__main__"` block to `spotify_client.py`:

```python
if __name__ == "__main__":
    from scraper import fetch_songs   # if we need sample titles

    sp = get_spotify_client()
    
    # Test with a known song
    test_title = "Blinding Lights"
    uri = search_track(sp, test_title)
    print(f"URI for '{test_title}': {uri}")
    
    # Test with a list of titles (maybe from scraper)
    test_titles = ["Believer", "Shape of You", "This non-existent song"]
    uris = collect_track_uris(sp, test_titles)
    print(f"Found {len(uris)} out of {len(test_titles)}")
```

Run it and verify that the URIs are correctly returned. You should see output like:

```
URI for 'Blinding Lights': spotify:track:0VjIjW4GlUZAMYd2vXMi3b
⚠️  Could not find: This non-existent song
Found 2 out of 3
```

## 3.7 What We’ve Accomplished

- ✅ Implemented a function to search for a track by name.
- ✅ Processed a list of song titles to collect Spotify URIs.
- ✅ Handled missing songs gracefully.
- ✅ (Optional) Added a small delay to be respectful of rate limits.

Now we have a list of URIs that represent the actual songs on Spotify. In the next step, we’ll create a new playlist and add these tracks to it.
