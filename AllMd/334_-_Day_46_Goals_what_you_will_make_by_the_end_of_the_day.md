
# Musical Time Machine – Software Engineering Plan

## 1. Overview
The Musical Time Machine is an automated tool that allows a user to generate a Spotify playlist containing the Billboard Hot 100 top songs from any given date. The system scrapes historical chart data from the Billboard website, authenticates with the Spotify API, searches for each track, and creates a private playlist in the user’s Spotify account. This project demonstrates the integration of web scraping, OAuth authentication, and third‑party API consumption in a robust Python application.

## 2. Objectives
- Build a command‑line interface (CLI) that accepts a user‑supplied date.
- Scrape the Billboard Hot 100 chart for that date using BeautifulSoup.
- Securely authenticate with Spotify using OAuth 2.0 (via Spotipy).
- Search Spotify for each scraped song title and obtain its unique URI.
- Create a new private Spotify playlist titled “YYYY-MM-DD Billboard 100”.
- Add all successfully found tracks to the playlist.
- Gracefully handle missing songs and API errors.
- (Optional) Expose the same functionality via a Flask web application.

## 3. Technology Stack
| Component         | Technology / Library                | Purpose                                          |
| ----------------- | ----------------------------------- | ------------------------------------------------ |
| Language          | Python 3.10+                        | Core programming language                        |
| Web Scraping      | BeautifulSoup 4 + requests           | Parse static Billboard HTML                       |
| Spotify API       | Spotipy                              | Pythonic wrapper for Spotify Web API              |
| Authentication    | OAuth 2.0 (Spotipy handles flow)     | Secure user authorization                          |
| Environment Mgmt  | python-dotenv                        | Load secrets from `.env` file                     |
| Dependency Mgmt   | pip + requirements.txt               | Manage Python packages                            |
| Version Control   | Git + GitHub                         | Source code management                            |
| (Optional) Web UI | Flask + Bootstrap                    | Provide browser‑based interface                    |
| Testing           | pytest                               | Unit and integration tests                        |
| Logging           | Python logging module                | Debug and runtime information                     |

## 4. Environment Setup
### 4.1 Prerequisites
- Python 3.10 or higher installed.
- A Spotify account (free or premium).
- A registered Spotify App in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

### 4.2 Local Development Environment
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/musical-time-machine.git
   cd musical-time-machine
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables**:
   Create a `.env` file in the project root with the following:
   ```ini
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
   ```
   (The redirect URI must match the one configured in your Spotify app.)

## 5. Workflow / Development Phases
The development is broken into iterative phases, each delivering a functional increment.

### Phase 1: Billboard Scraper
- **Goal**: Extract top 100 song titles from a given date.
- **Tasks**:
  1. Study the Billboard URL structure: `https://www.billboard.com/charts/hot-100/YYYY-MM-DD/`.
  2. Use `requests` to fetch the page and `BeautifulSoup` to parse the HTML.
  3. Identify the correct CSS selectors for song titles (and optionally artists).
  4. Return a clean list of strings.
- **Acceptance Criteria**: Running the scraper with a date returns 100 song titles (or fewer if page changes, but handle gracefully).

### Phase 2: Spotify Authentication
- **Goal**: Obtain a user access token with required scopes (`playlist-modify-private`).
- **Tasks**:
  1. Configure Spotipy with client ID, secret, and redirect URI.
  2. Implement the OAuth flow: open browser for user authorization, capture the callback.
  3. Store the token (Spotipy handles caching).
- **Acceptance Criteria**: Script can authenticate and print token validity.

### Phase 3: Search Spotify for Tracks
- **Goal**: Given a list of song titles, retrieve Spotify URIs.
- **Tasks**:
  1. For each title, call `sp.search(q=song, type='track', limit=1)`.
  2. Extract the URI from the first result.
  3. If no result, log a warning and skip.
- **Acceptance Criteria**: For a known test song (e.g., “Blinding Lights”), returns a valid URI.

### Phase 4: Playlist Creation and Population
- **Goal**: Create a playlist and add tracks.
- **Tasks**:
  1. Use `sp.user_playlist_create()` with the user ID and a name (the date).
  2. Use `sp.playlist_add_items()` to add the list of URIs (in batches of 100 max).
- **Acceptance Criteria**: After execution, a new private playlist appears in the user’s Spotify account with the scraped songs.

### Phase 5: Integration & CLI
- **Goal**: Combine all phases into a single script with user input.
- **Tasks**:
  1. Prompt user for a date (with validation).
  2. Chain the steps: scrape → authenticate → search → create → add.
  3. Add logging to show progress.
- **Acceptance Criteria**: End‑to‑end run successfully creates a playlist.

### Phase 6 (Optional): Flask Web Application
- **Goal**: Provide a web interface.
- **Tasks**:
  1. Set up a Flask app with a simple form for date input.
  2. Store the Spotify token in session (using Flask‑Session).
  3. Trigger the playlist creation workflow as a background task (to avoid timeout).
  4. Display success/error messages.
- **Acceptance Criteria**: User can enter a date via browser and receive a confirmation.

## 6. Detailed Design
### 6.1 Module Structure
```
musical_time_machine/
├── scraper.py          # Billboard scraping logic
├── spotify_client.py   # Spotify authentication & API calls
├── playlist_builder.py # Orchestrates the whole process
├── cli.py              # Command‑line entry point
├── web.py              # Flask application (optional)
├── config.py           # Load environment variables
├── utils.py            # Helper functions (logging, date validation)
├── tests/              # Unit tests
└── requirements.txt
```

### 6.2 Key Functions
- `scraper.fetch_songs(date: str) -> List[str]`
- `spotify_client.get_spotify_connection() -> spotipy.Spotify`
- `spotify_client.search_track(track_name: str) -> Optional[str]`
- `spotify_client.create_playlist(name: str) -> str` (returns playlist ID)
- `spotify_client.add_tracks_to_playlist(playlist_id: str, track_uris: List[str])`
- `playlist_builder.build_playlist(date: str) -> bool`

### 6.3 Data Flow
```
User inputs date → Scraper fetches HTML → Extract song titles → 
Authenticate with Spotify → For each title: search Spotify → Collect URIs → 
Create playlist → Add URIs → Confirmation to user
```

### 6.4 Error Handling
- **Scraping**: If Billboard page changes structure, raise a clear error and suggest updating selectors.
- **Authentication**: If token refresh fails, prompt user to re‑authenticate.
- **Search**: Log songs not found; continue with remainder.
- **API Rate Limits**: Spotipy handles retries; we add delays if necessary.
- **Network Issues**: Retry with exponential backoff.

## 7. Testing Strategy
- **Unit Tests**: Test each module in isolation with mocked dependencies (e.g., mock requests for scraper, mock Spotipy for API calls).
- **Integration Tests**: Run against a test Spotify account (using a dedicated test playlist) to verify end‑to‑end flow.
- **Manual Testing**: For various dates (e.g., current week, past decade, edge cases like 1960s).
- **Continuous Integration**: Use GitHub Actions to run tests on every push.

## 8. Deployment Considerations
- **CLI Tool**: Users run locally – deployment is not required.
- **Flask Web App**: If built, deploy to a platform like Heroku, PythonAnywhere, or a VPS. Must handle:
  - Long‑running requests (use background tasks with Celery or threading).
  - Secure storage of user tokens (database or encrypted session).
  - Domain and HTTPS for OAuth redirect URI.

## 9. Timeline & Milestones
| Milestone                    | Estimated Effort | Dependencies          |
| ---------------------------- | ---------------- | --------------------- |
| Phase 1: Scraper             | 1 day            | None                  |
| Phase 2: Authentication       | 1 day            | Spotify App setup     |
| Phase 3: Track Search        | 1 day            | Phase 2               |
| Phase 4: Playlist Creation   | 1 day            | Phase 3               |
| Phase 5: Integration & CLI   | 1 day            | Phases 1‑4            |
| Phase 6: Flask Web UI        | 2 days           | Phase 5               |
| Testing & Documentation      | 1 day            | All phases            |

Total: ~7 days (including optional web UI).

## 10. Risks and Mitigations
| Risk                                      | Mitigation                                          |
| ----------------------------------------- | --------------------------------------------------- |
| Billboard website changes HTML structure | Use robust selectors; add a fallback; monitor frequently. |
| Spotify API rate limits                   | Implement request throttling; use Spotipy’s built‑in retries. |
| OAuth token expiration                    | Spotipy auto‑refreshes if a refresh token is available. |
| Missing songs on Spotify                  | Log and skip; optionally try alternative search queries (e.g., include artist). |
| User inputs invalid date                  | Validate format; if scraping fails, prompt again.   |

## 11. Conclusion
The Musical Time Machine project combines essential real‑world skills: web scraping, API integration, authentication, and application design. By following this plan, a developer can build a reliable tool that delivers a personalised nostalgia trip through music. The modular architecture allows easy maintenance and future enhancements (e.g., supporting other charts, collaborative playlists). With careful attention to error handling and testing, the final product will be both fun and robust.
