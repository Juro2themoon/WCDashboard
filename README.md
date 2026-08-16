# FIFA World Cup 2026 Dashboard

A Python-based football dashboard that retrieves FIFA World Cup 2026 match data from the ESPN API, processes and validates the response, stores the data locally, and generates a self-contained HTML dashboard.

The project was built to develop practical experience with **REST APIs, JSON processing, data validation, persistent state, caching, backups, logging, hashing, and dynamic HTML generation** using Python's standard library.

## Why I Built This

I was watching the world cup and thought, "i would like to see what world cup fixtures are on today" and then i dawned on me... I can make that!
I also wanted to develop some practical experience building an application using an external APi. I wanted to understand the underlying processes involved instead of using a framework.

Unfortunately the world cup came to an end before i could implement every feature that i wanted to. Fortunately i am satrting a new project,and i decided to use this project as a foundation for it: *A Premier league Dashboard* . i will use this project to refine my skills and add all my preferred features e.g league table and stats.

## Features

* Retrieves World Cup match data from the ESPN API
* Parses nested JSON API responses
* Extracts:

  * Match ID
  * Teams
  * Kick-off time
  * Match status
  * Score
  * Venue
* Validates required match fields before storing data
* Persists processed match data in a JSON state file
* Caches the latest successful API response
* Falls back to cached data if the API request fails
* Creates backups of the previous application state
* Generates dynamic HTML match cards
* Calculates a hash of the generated HTML
* Compares the generated HTML hash with the previous hash
* Avoids rewriting the dashboard when the generated HTML has not changed
* Logs application events and errors
* Handles API failures and corrupted state/cache files
* Uses Python's standard library without a web framework or database

## Architecture

The application follows a simple data-processing pipeline:

```text
                    ESPN API
                       │
                       ▼
                Fetch match data
                       │
              ┌────────┴────────┐
              │                 │
           Success            Failure
              │                 │
              ▼                 ▼
        Save API cache      Load API cache
              │                 │
              └────────┬────────┘
                       ▼
                 Parse JSON
                       │
                       ▼
              Validate match data
                       │
                       ▼
               Backup old state
                       │
                       ▼
                Save new state
                       │
                       ▼
                Generate HTML
                       │
                       ▼
              Calculate HTML hash
                       │
                       ▼
             Compare previous hash
                       │
                ┌──────┴──────┐
                │             │
             Changed       Unchanged
                │             │
                ▼             ▼
          Write HTML       No update
                │
                ▼
        World Cup Dashboard
```

## Project Structure

```text
WCDashboard/
│
├── backups/
├── cache/
├── logs/
│   └── update.log
├── state/
│   ├── state.json
│   └── html_hash
│
├── .gitignore
├── README.md
├── index.html
└── update_dashboard.py
```

### `update_dashboard.py`

The main application responsible for:

* Creating required directories
* Initialising application state
* Configuring logging
* Fetching API data
* Caching successful API responses
* Loading cached data when the API is unavailable
* Parsing match information
* Validating required fields
* Backing up previous application state
* Saving and loading application state
* Generating HTML
* Calculating and comparing the generated HTML hash

### `state/`

Contains persistent application state.

`state.json` stores the latest processed match data and the timestamp of the most recent update.

`html_hash` stores the hash of the most recently generated HTML.

### `cache/`

Contains the latest successful response retrieved from the ESPN API.

If a future API request fails, the application can use this cached response instead of failing immediately.

### `backups/`

Contains backups of the previous `state.json` before new state is written.

### `logs/`

Contains application logs used to monitor execution and diagnose errors.

### `index.html`

The generated dashboard containing the processed World Cup match data.

## Data Processing

The application retrieves match information from the ESPN World Cup scoreboard endpoint.

The raw API response contains nested event, competition and competitor objects. The application extracts the relevant fields and converts them into a simplified match structure.

Example:

```json
{
    "id": "760506",
    "kickoff": "2026-07-06T19:00Z",
    "status": "Scheduled",
    "venue": "AT&T Stadium",
    "home_team": "Portugal",
    "away_team": "Spain",
    "home_score": null,
    "away_score": null
}
```

Before a match is stored, required fields are validated. Matches missing an ID, kick-off time or team information are skipped and recorded in the application log.

## Error Handling

The application includes handling for several failure scenarios.

### API failures

API requests use a timeout and exceptions are logged using Python's `logging` module.

If the API request fails, the application attempts to load the most recent successful response from the local cache.

### Missing cache

If no cached API response exists, the application falls back to the most recently stored application state.

### Missing state

If the state file does not exist, the application returns an empty state rather than terminating.

### Corrupted state or cache

If either the state file or cache contains invalid JSON, the application logs the error and returns an empty result.

### Incomplete API data

Matches missing required information are skipped rather than being added to the dashboard.

## Caching and Backups

The application uses two simple reliability mechanisms.

### API Response Cache

After a successful API request, the raw response is saved to:

```text
cache/latest_response.json
```

If a subsequent API request fails, this cached response can be loaded and processed instead.

### State Backups

Before `state.json` is overwritten, the existing state is copied into the `backups/` directory with a UTC timestamp.

Example:

```text
backups/
├── state_20260816_201530.json
└── state_20260816_202030.json
```

This provides a simple recovery mechanism if the current state becomes corrupted or needs to be inspected.

## HTML Generation

The dashboard is generated directly from the processed Python data.

Each match is converted into an HTML card displaying:

* Home team
* Away team
* Score
* Match status
* Kick-off time
* Venue

The generated HTML includes its own CSS, making the resulting `index.html` self-contained and capable of being opened directly in a browser.

## HTML Hashing

After generating the dashboard HTML, the application calculates a hash of the generated content.

The hash is stored locally in:

```text
state/html_hash
```

On subsequent runs, the newly generated hash is compared against the previously stored hash.

If the hashes are identical, the application does not rewrite `index.html`.

If they differ, the dashboard is regenerated and the new hash is saved.

This prevents unnecessary writes when the generated dashboard has not changed.

## Technologies

### Language

* Python 3

### Data

* REST API
* JSON

### Web

* HTML5
* CSS3

### Python Standard Library

* `urllib`
* `json`
* `logging`
* `pathlib`
* `datetime`
* `hashlib`
* `os`

### Version Control

* Git
* GitHub

## Running the Project

### Requirements

* Python 3.x
* Internet connection

The implementation uses the public ESPN API endpoint and does not require a separate API key.

### Clone the repository

```bash
git clone https://github.com/Juro2themoon/WCDashboard.git
cd WCDashboard
```

### Run the application

```bash
python3 update_dashboard.py
```

The application will:

1. Create the required directories
2. Initialise the state file if necessary
3. Configure logging
4. Retrieve World Cup match data
5. Cache a successful API response
6. Parse and validate the response
7. Back up the previous state
8. Save the processed match data
9. Generate the dashboard HTML
10. Calculate and compare the HTML hash
11. Update `index.html` only when the generated content has changed

### View the dashboard

Open the generated `index.html` file in a web browser.

## Development Journey

The project was developed incrementally, with functionality added through multiple stages.

Major development steps included:

1. Initial project structure
2. API integration
3. JSON response parsing
4. Match extraction
5. Data validation
6. Persistent state management
7. State loading and error handling
8. Dynamic HTML generation
9. Match card development
10. CSS styling
11. HTML hashing
12. API response caching
13. State backups
14. HTML change detection
15. Continued debugging and refinement

The Git history documents the progression of the application from a basic API data fetcher into a structured data-processing and dashboard application.

## Future Improvements

As the World Cup has now finished, this project is considered complete.

Potential improvements that were considered but are being carried forward into future projects include:

* Automated scheduled updates
* More detailed match statistics
* Tournament and group standings
* Improved mobile responsiveness
* Automated testing
* More advanced API retry mechanisms
* More sophisticated data visualisation

These features will instead be explored in the **Premier League 2026/27 Dashboard**, which builds on the foundations developed in this project.

## Purpose

This project forms part of my software engineering portfolio and was built to gain practical experience developing a complete data-driven application.

The main focus was understanding the flow from an external data source to a user-facing application:

**API → JSON → Validation → State → Processing → HTML → Dashboard**

The project deliberately avoids a web framework and database so that the underlying processes involved in data retrieval, processing, persistence, caching and presentation could be implemented directly in Python.

## Author

**Juro2themoon**

GitHub: https://github.com/Juro2themoon
