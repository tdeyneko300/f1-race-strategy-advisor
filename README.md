# f1-race-strategy-advisor

API-сервис (FastAPI) для работы с данными F1 и выдачи полезных подсказок/метрик (например, быстрый круг), с офлайн-режимом через локальный датасет.

## Overview
Проект поднимает HTTP API (FastAPI) и использует CSV-файлы в папке `data/` как офлайн-источник данных.

## Features
- FastAPI backend.
- Offline-вычисления из локального датасета (папка `data/`).
- Локальный кэш запросов/вычислений (папка `cache/`) — не коммитится.

## Tech stack
- Python
- FastAPI
- Uvicorn

## Project structure
```
├── main.py

├── requirements.txt

├── README.md

├── LICENSE

├── data/ (races.csv, drivers.csv, lap_times.csv, results.csv, constructors.csv)

└── cache/ # локальный кэш (не хранится в репозитории)
```

## Getting started

### Clone
```bash
git clone <REPO_URL>
cd f1-race-strategy-advisor
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
## API docs
После запуска сервера:
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## What problem it solves
Этот сервис помогает быстро получать базовые “инсайты” по F1 (события/гонки, быстрые круги) через HTTP API, чтобы:
- не вручную копаться в CSV;
- быстро интегрировать данные в фронт/бота/аналитику;
- иметь воспроизводимый офлайн-источник данных (папка `data/`).

## API examples

### 1) Список событий (events)
**Зачем:** быстро получить список доступных гонок/событий для выбора параметров в следующих запросах.

Request:
```bash
curl -s "http://127.0.0.1:8000/events"
```

Example response:
```bash
{
  "year": 2024,
  "events": [
    { "round": 1, "raceName": "Bahrain Grand Prix" },
    { "round": 2, "raceName": "Saudi Arabian Grand Prix" }
  ]
}
```
### 2) Быстрый круг по гонке (fastest lap)

Зачем: мгновенно получить fastest lap для выбранной гонки из локального датасета.

Request:
```bash
curl -s "http://127.0.0.1:8000/fastest-lap?year=2024&race=monza"
```

Example response:
```bash
{
  "year": 2024,
  "race": "monza",
  "driver": {
    "id": 1,
    "name": "Max Verstappen"
  },
  "lap_time_ms": 81234
}
```
