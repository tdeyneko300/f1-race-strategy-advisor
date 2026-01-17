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

@app.get("/drivers")
def drivers(year: int = 2024, round: int = 1, session: str = "R"):
    s = fastf1.get_session(year, round, session)
    s.load(telemetry=False, laps=False, weather=False)

    # Берём результаты сессии — там есть имена и команды
    df = s.results[["DriverNumber", "Abbreviation", "FullName", "TeamName"]]

    drivers_out = df.to_dict(orient="records")

    return {
        "year": year,
        "round": round,
        "session": session,
        "drivers": drivers_out
    }

