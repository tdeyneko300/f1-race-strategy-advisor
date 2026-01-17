# f1-race-strategy-advisor

API-сервис (FastAPI) для работы с данными F1 и выдачи полезных подсказок/метрик (например, быстрый круг), с офлайн-режимом через локальный датасет.

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
├── data/ # локальный датасет (не хранится в репозитории)
└── cache/ # локальный кэш (не хранится в репозитории)

## Getting started

### 1) Clone
```bash
git clone <REPO_URL>
cd f1-race-strategy-advisor
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
