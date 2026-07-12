import os
import json
import logging
from pathlib import Path
import urllib.request
from datetime import datetime, timezone

BASE_DIR = Path(__file__).parent

CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
STATE_DIR = BASE_DIR / "state"
BACKUP_DIR = BASE_DIR / "backups"

STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = LOG_DIR / "update.log"
INDEX_FILE = BASE_DIR / "index.html"

def ensure_directories():

    directories = [
        CACHE_DIR,
        LOG_DIR,
        STATE_DIR,
        BACKUP_DIR
    ]

    for directory in directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

def initialize_state():

    state_file = STATE_FILE
    if not state_file.exists():
        initial_state = {
            "last_updated": None,
            "data": {}
        }
        with open(state_file, 'w') as f:
            json.dump(initial_state, f, indent=4)
        print(f"Initialized state file: {state_file}")
    else:
        print(f"State file already exists: {state_file}")

def initialize_log():

    log_file = LOG_FILE
    if not log_file.exists():
        log_file.touch()
        print(f"Created log file: {log_file}")
    else:
        print(f"Log file already exists: {log_file}")

    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
def generate_html():

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>World Cup Dashboard</title>
    </head>
    <body>
        <header>
            <h1>World Cup Dashboard</h1>
        </header>
        <main>
            <section id="data-section">
                <h2>Data Overview</h2>
                <div id="data-container">
                    <!-- Data will be dynamically inserted here -->
                </div>
            </section>
            <section id="update-section">
                <h2>Update Data</h2>
                <button id="update-button">Update Now</button>
            </section>
        </main>
        <footer>
            <p>&copy; 2026 World Cup Dashboard</p>
        </footer>
    </body>
    </html>
    """

    return html

def write_html(html):

        html_file = INDEX_FILE
        with open(html_file, 'w') as f:
                f.write(html)
        print(f"Generated HTML file: {html_file}")


ESPN_URL = (
     "https://site.api.espn.com/apis/site/v2/sports/"
    "soccer/fifa.world/scoreboard"
)


def fetch_matches():
     
    try:
          with urllib.request.urlopen(ESPN_URL, timeout=10) as response:
               return json.load(response)

    except Exception as error:
        logging.exception("Failed to fetch match data: %s", error)
        return None        
    
def parse_matches(data):
    matches = []
    events = data.get("events", [])

    for event in events:

        competition = event.get("competitions", [{}])[0]

        competitors = competition.get("competitors", [])

        home = {}
        away = {}

        for competitor in competitors:

            if competitor.get("homeAway") == "home":
                home = competitor

            elif competitor.get("homeAway") == "away":
                away = competitor

        match = {
            "id": event.get("id"),
            "kickoff": event.get("date"),
            "status": competition.get("status", {})
                        .get("type", {})
                        .get("description"),

            "venue": competition.get("venue", {})
                        .get("fullName"),

            "home_team": home.get("team", {})
                     .get("displayName"),

            "away_team": away.get("team", {})
                     .get("displayName"),

            "home_score": home.get("score"),

            "away_score": away.get("score"),
        }

        required_fields = [
            "id",
            "kickoff",
            "home_team",
            "away_team"
        ]

        missing = [
            field for field in required_fields if not match.get(field)
        ]

        if missing:
            logging.warning(
                "Skipping incomplete match. Missing fields: %s",
                ", ".join(missing)
            
            )
            continue

        matches.append(match)

    return matches

def save_state(matches):

    state = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "data": matches
        }
    
    with STATE_FILE.open('w') as file:
        json.dump(state, file, indent=4)

    logging.info("Saved %d matches to state file.", len(matches))

def load_state():

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    
    except FileNotFoundError:
        logging.warning("State file not found. Returning empty state.")
        return {"last_updated": None, "data": []}
    
    except json.JSONDecodeError:
        logging.error("State file is corrupted. Returning empty state.")
        return {"last_updated": None, "data": []}

def main():

    ensure_directories()

    initialize_state()

    initialize_log()

    matches = fetch_matches()

    if matches:
        print("Download successful!")

        parsed_matches = parse_matches(matches)

        save_state(parsed_matches)

        state = load_state()

        print(state)

        print("\nParsed matches:")

        for match in parsed_matches:
            print(match)
    else:
        print("Failed to download data.")


    logging.info("Dashboard started successfully.")

    html = generate_html()

    logging.info("HTML file created successfully.")

    write_html(html)

    print("Dashboard generated successfully.") 

if __name__ == "__main__":
    main()