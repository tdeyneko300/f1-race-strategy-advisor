from pathlib import Path

import fastf1

from fastapi import FastAPI
from typing import List
from typing import Optional
from pydantic import BaseModel

import pandas as pd
from fastapi import HTTPException


CACHE_DIR = Path(__file__).parent / "cache"
fastf1.Cache.enable_cache(str(CACHE_DIR))
DATA_DIR = Path(__file__).parent / "data"
RACES_CSV = DATA_DIR / "races.csv"
LAP_TIMES_CSV = DATA_DIR / "lap_times.csv"
DRIVERS_CSV = DATA_DIR / "drivers.csv"

class DriverFromDataset(BaseModel):
    driver_id: int
    number: str | None = None
    code: str | None = None
    full_name: str

class FastestLapFromDataset(BaseModel):
    lap_time_ms: int
    lap_time: str
    lap: int
    driver: DriverFromDataset

class FastestLapDatasetResponse(BaseModel):
    year: int
    round: int
    race_id: int
    race_name: str
    fastest_lap: FastestLapFromDataset


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

class DriverLite(BaseModel):
    number: str
    abbreviation: str
    team_name: str

class ErrorMessage(BaseModel):
    message: str


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


class FastestLap(BaseModel):
    lap_time: str
    lap_number: Optional[int] = None
    driver: DriverLite

class FastestLapResponse(BaseModel):
    year: int
    round: int
    session: str
    fastest_lap: FastestLap

# @app.get("/fastest-lap", response_model=FastestLapResponse)
# def fastest_lap(year: int = 2024, round: int = 1, session: str = "Q"):
#     s = fastf1.get_session(year, round, session)
#     s.load(telemetry=False, weather=False, laps=True)

#     fl = s.laps.pick_fastest()

#     abbr = str(fl["Driver"])
#     number = str(fl["DriverNumber"])
#     team = str(fl["Team"])
#     lap_time = str(fl["LapTime"])
#     lap_number = int(fl["LapNumber"]) if str(fl.get("LapNumber", "")) not in ("", "nan", "NaT") else None

#     driver = DriverLite(number=number, abbreviation=abbr, team_name=team)

#     return FastestLapResponse(
#         year=year,
#         round=round,
#         session=session,
#         fastest_lap=FastestLap(lap_time=lap_time, lap_number=lap_number, driver=driver),
#     )


def _format_ms(ms: int) -> str:
    # ms -> "M:SS.mmm"
    m, rem = divmod(ms, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{m}:{s:02d}.{milli:03d}"


@app.get(
    "/fastest-lap-dataset",
    response_model=FastestLapDatasetResponse,
    responses={404: {"model": ErrorMessage}},
)
def fastest_lap_dataset(year: int = 2024, round: int = 1):
    if not (RACES_CSV.exists() and LAP_TIMES_CSV.exists() and DRIVERS_CSV.exists()):
        raise HTTPException(status_code=500, detail="Dataset files not found in ./data")

    races = pd.read_csv(RACES_CSV)
    laps = pd.read_csv(LAP_TIMES_CSV)
    drivers = pd.read_csv(DRIVERS_CSV)

    race_row = races[(races["year"] == year) & (races["round"] == round)]
    if race_row.empty:
        raise HTTPException(status_code=404, detail="Race not found for given year/round")

    race_id = int(race_row.iloc[0]["raceId"])
    race_name = str(race_row.iloc[0]["name"])

    laps_race = laps[laps["raceId"] == race_id]
    if laps_race.empty:
        msg = (
            f"Для гонки '{race_name}' ({year}, round={round}) нет данных lap_times в датасете. "
            "В этом наборе lap times обычно доступны примерно с 1996 года."
        )
        raise HTTPException(status_code=404, detail={"message": msg})


    best = laps_race.sort_values("milliseconds", ascending=True).iloc[0]
    driver_id = int(best["driverId"])
    lap_ms = int(best["milliseconds"])
    lap_no = int(best["lap"])

    drow = drivers[drivers["driverId"] == driver_id]
    if drow.empty:
        raise HTTPException(status_code=404, detail="Driver not found in drivers.csv")

    drow = drow.iloc[0]
    forename = str(drow["forename"])
    surname = str(drow["surname"])
    full_name = f"{forename} {surname}"

    number = None if pd.isna(drow["number"]) else str(drow["number"])
    code = None if pd.isna(drow["code"]) else str(drow["code"])

    return FastestLapDatasetResponse(
        year=year,
        round=round,
        race_id=race_id,
        race_name=race_name,
        fastest_lap=FastestLapFromDataset(
            lap_time_ms=lap_ms,
            lap_time=_format_ms(lap_ms),
            lap=lap_no,
            driver=DriverFromDataset(
                driver_id=driver_id,
                number=number,
                code=code,
                full_name=full_name,
            ),
        ),
    )

