from pathlib import Path

import fastf1
from fastapi import FastAPI

CACHE_DIR = Path(__file__).parent / "cache"
fastf1.Cache.enable_cache(str(CACHE_DIR))

app = FastAPI(title="F1 Race Strategy Advisor")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/events")
def events(year: int = 2024):
    schedule = fastf1.get_event_schedule(year)
    cols = ["RoundNumber", "EventName", "Country", "Location"]
    result = schedule[cols].to_dict(orient="records")
    return {"year": year, "events": result}
