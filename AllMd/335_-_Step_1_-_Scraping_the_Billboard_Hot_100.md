
# Step 1 - Scraping the Billboard Hot 100

In this first step, we’ll build the web scraper that fetches the top 100 song titles from the Billboard Hot 100 chart for any given date.

## 1.1 Understand the Billboard URL structure

Billboard publishes the Hot 100 chart weekly. The URL pattern is:

```
https://www.billboard.com/charts/hot-100/YYYY-MM-DD/
```

For example, the chart for **1999-06-12** can be found at:  
[https://www.billboard.com/charts/hot-100/1999-06-12/](https://www.billboard.com/charts/hot-100/1999-06-12/)

Our scraper will take a date string from the user, insert it into this URL, and download the HTML.

## 1.2 Tools we need

- **`requests`** – to download the webpage.
- **`BeautifulSoup`** (from `bs4`) – to parse the HTML and extract data.

Install them if you haven’t already:

```bash
pip install requests beautifulsoup4
```

## 1.3 Inspect the Billboard page

Open the example URL in your browser and use **Developer Tools** (right‑click → Inspect) to examine the HTML structure. We need to find a reliable CSS selector that targets all song titles on the page.

As of early 2025, the song titles are contained in an `<h3>` tag with the class `c-title` and an additional class `a-no-trucate`. A good selector is:

```css
h3.c-title.a-no-trucate
```

Alternatively, you could use:

```css
#title-of-a-story
```

But the safest approach is to look for elements that hold the title text. The exact selector may change over time; we’ll write our code so that it’s easy to update.

## 1.4 Write the scraper function

Create a new file named `scraper.py`. We’ll define a function `fetch_songs(date)` that:

1. Builds the URL from the date.
2. Sends a GET request with a `User-Agent` header to mimic a browser (some sites block scripts without it).
3. Parses the HTML with BeautifulSoup.
4. Finds all elements matching our selector.
5. Extracts the text and cleans it (removing extra whitespace).
6. Returns a list of song titles.

```python
import requests
from bs4 import BeautifulSoup

def fetch_songs(date):
    """
    Scrapes the Billboard Hot 100 chart for the given date and returns a list of song titles.
    :param date: string in format 'YYYY-MM-DD'
    :return: list of strings (top 100 song titles)
    """
    url = f"https://www.billboard.com/charts/hot-100/{date}/"
    
    # Headers to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # This selector targets the song titles. Update if Billboard changes their markup.
    title_elements = soup.select("h3.c-title.a-no-trucate")
    
    # Extract text from each element
    song_titles = []
    for element in title_elements:
        title = element.get_text(strip=True)
        if title:  # Avoid empty strings
            song_titles.append(title)
    
    return song_titles
```

## 1.5 Test the scraper

Add a simple test block at the bottom of `scraper.py` to see if it works:

```python
if __name__ == "__main__":
    test_date = "1999-06-12"
    titles = fetch_songs(test_date)
    print(f"Found {len(titles)} songs for {test_date}")
    for i, title in enumerate(titles[:10], 1):
        print(f"{i}. {title}")
```

Run the script:

```bash
python scraper.py
```

You should see the top 10 songs from that week. If the list is empty or the count is less than 100, the selector may need adjustment. Billboard sometimes changes their class names, so be prepared to update the selector.

## 1.6 Handling errors and edge cases

- **Invalid date**: If the date is malformed or no chart exists, the page might still load but contain no song elements. Our function would return an empty list. We can handle that later in the main program.
- **Network issues**: `requests.get()` may raise exceptions; we should catch them in the calling code.
- **Billboard changes**: To make the scraper robust, consider adding a fallback selector or logging a warning if the number of songs is below 100.

## 1.7 What we’ve accomplished

- ✅ We can retrieve the Billboard Hot 100 for any historical date.
- ✅ We have a reusable function that returns a clean list of song titles.

Now we’re ready to move on to **Step 2 – Authentication with Spotify**, where we’ll set up our Spotify developer app and learn how to get permission to modify playlists.

