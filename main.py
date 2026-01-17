from pathlib import Path

import fastf1
from fastapi import FastAPI

from typing import List
from pydantic import BaseModel


CACHE_DIR = Path(__file__).parent / "cache"
fastf1.Cache.enable_cache(str(CACHE_DIR))


class Driver(BaseModel):
    number: str
    abbreviation: str
    full_name: str
    team_name: str


class DriversResponse(BaseModel):
    year: int
    round: int
    session: str
    drivers: List[Driver]

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

@app.get("/drivers", response_model=DriversResponse)
def drivers(year: int = 2024, round: int = 1, session: str = "R"):
    s = fastf1.get_session(year, round, session)
    s.load(telemetry=False, laps=False, weather=False)

    df = s.results[["DriverNumber", "Abbreviation", "FullName", "TeamName"]]

    drivers_out = [
        Driver(
            number=str(row["DriverNumber"]),
            abbreviation=str(row["Abbreviation"]),
            full_name=str(row["FullName"]),
            team_name=str(row["TeamName"]),
        )
        for _, row in df.iterrows()
    ]

    return DriversResponse(
        year=year,
        round=round,
        session=session,
        drivers=drivers_out,
    )


