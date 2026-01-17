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
├── main.py

├── requirements.txt

├── README.md

├── LICENSE

├── data/ (races.csv, drivers.csv, lap_times.csv, results.csv, constructors.csv)

└── cache/ # локальный кэш (не хранится в репозитории)

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


##№ API docs
После запуска сервера открой:
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
