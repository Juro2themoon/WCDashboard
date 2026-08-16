import os
import json
import logging
from pathlib import Path
import urllib.request
from datetime import datetime, timezone
import hashlib

BASE_DIR = Path(__file__).parent

CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
STATE_DIR = BASE_DIR / "state"
BACKUP_DIR = BASE_DIR / "backups"

STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = LOG_DIR / "update.log"
INDEX_FILE = BASE_DIR / "index.html"
CACHE_FILE = CACHE_DIR / "latest_response.json"


HTML_HASH_FILE = BASE_DIR / "state" / "html_hash"

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
            logging.info(f"Created directory: {directory}")
        else:
            logging.info(f"Directory already exists: {directory}")

def initialize_state():

    state_file = STATE_FILE
    if not state_file.exists():
        initial_state = {
            "last_updated": None,
            "data": {}
        }
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(initial_state, f, indent=4)
        logging.info(f"Initialized state file: {state_file}")
    else:
        logging.info(f"State file already exists: {state_file}")

def initialize_log():

    log_file = LOG_FILE
    if not log_file.exists():
        log_file.touch()
        logging.info(f"Created log file: {log_file}")
    else:
        logging.info(f"Log file already exists: {log_file}")

    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def generate_match_card(match):
    return f"""
    <div class="match-card">

        <div class="teams">
            <span>{match.get("home_team", "Unknown")}</span>

            <strong class="score">
                {match.get("home_score", "-")} - {match.get("away_score", "-")}
            </strong>

            <span>{match.get("away_team", "Unknown")}</span>
        </div>

        <div class="details">
            <p><strong>Status:</strong> {match.get("status", "Unknown")}</p>
            <p><strong>Kickoff:</strong> {match.get("kickoff", "Unknown")}</p>
            <p><strong>Venue:</strong> {match.get("venue", "Unknown")}</p>
        </div>

    </div>
    """

def generate_html(matches):

    match_cards = ""

    for match in matches:
        match_cards += generate_match_card(match)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>World Cup Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}

            header {{
                text-align: center;
                margin-bottom: 30px;
            }}

            #data-container {{
                max-width: 800px;
                margin: 0 auto;
            }}

            .match-card {{
                background: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            }}

            .match-card h2 {{
                margin-top: 0;
            }}

            .teams {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 22px;
                margin-bottom: 20px;
            }}

            .score {{
                font-size: 30px;
            }}

            .details p {{
                margin: 6px 0;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>World Cup Dashboard</h1>
        </header>
        <main>
            <section id="data-section">
                <h2>Data Overview</h2>
                <div id="data-container">

                    {match_cards}

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
        with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
        logging.info(f"Generated HTML file: {html_file}")


def calculate_html_hash(html):
    return hashlib.sha256(html.encode("utf-8")).hexdigest()


def load_html_hash():

    try:
        return HTML_HASH_FILE.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        return None


def save_html_hash(html_hash):
    HTML_HASH_FILE.write_text(html_hash, encoding="utf-8")


def html_has_changed(new_html_hash):

    previous_hash = load_html_hash()

    if previous_hash is None:
        logging.info("No previous HTML hash found. HTML will be generated.")
        return True

    if previous_hash != new_html_hash:
        logging.info("HTML content has changed.")
        return True

    logging.info("HTML content has not changed.")
    return False
    


ESPN_URL = (
     "https://site.api.espn.com/apis/site/v2/sports/"
    "soccer/fifa.world/scoreboard"
)

def save_cache(data):

    with CACHE_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    logging.info("Saved API response to cache.")


def load_cache():

    try:

        with CACHE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        logging.info("Loaded data from cache.")

        return data

    except FileNotFoundError:

        logging.warning("Cache file not found.")

        return None

    except json.JSONDecodeError:

        logging.error("Cache file is corrupted.")

        return None



def fetch_matches():
     
    try:
        with urllib.request.urlopen(ESPN_URL, timeout=10) as response:

            data = json.load(response)

        save_cache(data)

        logging.info("Successfully fetched fresh match data.")

        return data

    except Exception as error:

        logging.exception("Failed to fetch match data: %s", error)

        logging.info("Attempting to load cached API response.")

        cached_data = load_cache()

        if cached_data is not None:

            logging.info("Using cached API response.")

            return cached_data

        logging.error("No cached data available.")

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

    backup_state()

    state = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "data": matches
        }
    
    with STATE_FILE.open('w', encoding='utf-8') as file:
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

def backup_state():

    if not STATE_FILE.exists():

        logging.info("No existing state file to backup.")

        return

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    backup_file = BACKUP_DIR / f"state_{timestamp}.json"

    with STATE_FILE.open("r", encoding="utf-8") as source:

        data = source.read()

    with backup_file.open("w", encoding="utf-8") as destination:

        destination.write(data)

    logging.info("Created state backup: %s", backup_file)

def main():

    ensure_directories()

    initialize_state()

    initialize_log()

    matches = fetch_matches()

    if matches:

        parsed_matches = parse_matches(matches)

        save_state(parsed_matches)

        state = load_state()

    else:
        logging.error("No match data available. Using last known state.")

        state = load_state()


    logging.info("Dashboard started successfully.")

    html = generate_html(state["data"])

    new_html_hash = calculate_html_hash(html)

    if html_has_changed(new_html_hash):

        write_html(html)

        save_html_hash(new_html_hash)

        logging.info("Dashboard HTML updated.")

        logging.info("Dashboard generated successfully.")

    else:

        logging.info("Dashboard HTML unchanged. No update required.")

        logging.info("Dashboard unchanged. No update required.")

if __name__ == "__main__":
    main()