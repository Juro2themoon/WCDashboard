# FIFA World Cup 2026 Dashboard

A self-updating football dashboard built with Python that retrieves FIFA World Cup 2026 match data from an external API, processes and validates the data, maintains persistent application state, detects changes, and generates a self-contained HTML dashboard.

The project was developed incrementally to practise real-world software engineering concepts including API integration, data processing, state management, validation, logging, HTML generation and error handling.

## Features

* Fetches World Cup match data from an external API
* Parses and validates incoming JSON data
* Extracts relevant match information including:

  * Teams
  * Kick-off time
  * Match status
  * Score
  * Venue
* Maintains persistent match state between updates
* Generates dynamic HTML match cards
* Detects changes between dashboard updates
* Saves and loads generated HTML state information
* Includes structured logging for monitoring and debugging
* Uses environment variables to securely provide API credentials
* Generates a self-contained dashboard without a web framework or database

## Technologies

* **Python 3**
* **REST APIs**
* **JSON**
* **HTML5**
* **CSS3**
* **Git / GitHub**

The project uses Python's standard library wherever possible and does not rely on a Python web framework.

## Architecture

The dashboard follows a simple data-processing pipeline:

```text
External Football API
        ↓
   Fetch match data
        ↓
     JSON response
        ↓
   Parse & validate
        ↓
   Process match data
        ↓
   Save application state
        ↓
   Detect changes
        ↓
   Generate HTML
        ↓
   FIFA World Cup Dashboard
```

This separation allows the data retrieval, processing, state management and presentation logic to be developed and tested independently.

## Project Structure

```text
WCDashboard/
│
├── scripts/
│   └── update_dashboard.py
│
├── state/
│   └── state.json
│
├── logs/
│   └── update.log
│
├── index.html
├── README.md
└── ...
```

### `scripts/`

Contains the main Python application responsible for retrieving, processing and updating the dashboard.

### `state/`

Stores persistent application state so information can be retained between dashboard updates.

### `logs/`

Contains application logs used to monitor execution and diagnose problems.

### `index.html`

The generated dashboard displayed in a web browser.

## How It Works

### 1. Fetch

The application sends a request to the football data API and retrieves the latest available World Cup match information.

### 2. Parse

The JSON response is parsed into Python data structures and the relevant match information is extracted.

### 3. Validate

Incoming match data is checked before being used by the dashboard. This helps prevent incomplete or unexpected API responses from causing failures further through the application.

### 4. Save State

Processed match information is stored locally so the application can compare data across updates.

### 5. Detect Changes

The application compares current information with previously stored state to identify changes in match information.

### 6. Generate Dashboard

The processed data is used to dynamically generate HTML match cards containing the latest match information.

## Running the Project

### Requirements

* Python 3.x
* An API key for the football data provider used by the project

### 1. Clone the repository

```bash
git clone https://github.com/Juro2themoon/WCDashboard.git
cd WCDashboard
```

### 2. Configure the API key

The application reads the API key from an environment variable.

On macOS/Linux:

```bash
export API_FOOTBALL_KEY="your_api_key_here"
```

On Windows PowerShell:

```powershell
$env:API_FOOTBALL_KEY="your_api_key_here"
```

Do not commit API keys or other credentials to the repository.

### 3. Run the dashboard updater

```bash
python3 scripts/update_dashboard.py
```

The script retrieves the latest data, processes the matches and updates the generated dashboard.

### 4. Open the dashboard

Open `index.html` in a web browser to view the generated dashboard.

## Engineering Challenges

During development, several practical software engineering problems were encountered and resolved, including:

* Handling nested JSON responses from an external API
* Validating incoming match data
* Managing persistent application state
* Separating data processing from HTML generation
* Handling missing or unexpected API fields
* Maintaining reliable file paths across the project
* Implementing structured application logging
* Detecting changes between successive API responses
* Preventing unnecessary dashboard updates when the generated content has not changed

These challenges helped develop practical experience beyond simply consuming an API and displaying its response.

## Development Process

The project was developed incrementally, with functionality introduced and tested in stages.

The development process included:

1. Project structure and initial application setup
2. API data retrieval
3. JSON parsing
4. Match extraction and validation
5. Persistent state management
6. Dynamic HTML generation
7. Match card generation
8. CSS styling
9. Change detection
10. HTML hash saving and loading
11. Debugging and refinement

## Why I Built This

I was watching the world cup and thought, "i would like to see what world cup fixtures are on today" and then i dawned on me... I can make that!
I also wanted to develop some practical experience building an application using an external APi. I wanted to understand the underlying processes involved instead of using a framework.

Unfortunately i was a bit slow with the development of my app and i only implemented a few features before the world cup had ended. Fortunately i am satrting a new project, a Premier league Dashboard. i will use this project to refine my skills and add all my preferred features e.g league table and stats.

included concepts:

**API integration → data processing → state management → change detection → HTML generation**

## Author

**Juro2themoon**

GitHub:
https://github.com/Juro2themoon

