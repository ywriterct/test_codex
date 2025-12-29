# test_codex

Quiet Routes Navigator: a small API that scores subway routes using live GTFS-RT
vehicle positions to highlight quieter options.

## Quick start

### 1) Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure MTA access
Provide your MTA API key (required for live data) and optionally the feed URL.
The same developer key used for subway or bus trackers works with the GTFS-RT
vehicle feed.
```bash
export MTA_API_KEY="your-mta-key"
export MTA_FEED_URL="https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"
export MTA_API_KEY_HEADER="x-api-key"
```

### 3) Run the API
```bash
uvicorn app.main:app --reload
```

### 4) Query quiet routes
```bash
curl "http://127.0.0.1:8000/quiet-routes?origin=Prospect+Park&destination=Times+Square"
```

## How it works
- Pulls the live GTFS-RT feed for vehicle positions.
- Counts active vehicles per route.
- Scores routes with fewer vehicles as quieter (higher quiet score).

## Response shape
The API returns suggestions, warnings if live data is unavailable, and the feed
timestamp. If `MTA_API_KEY` is missing the response includes an empty list with
a warning.

Each suggestion includes a `trip_planner_url` that opens the MTA trip planner
with your origin and destination so you can get turn-by-turn instructions until
native routing is implemented.
