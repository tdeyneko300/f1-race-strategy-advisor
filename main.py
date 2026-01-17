from fastapi import FastAPI

app = FastAPI(title="F1 Race Strategy Advisor")

@app.get("/health")
def health():
    return {"status": "ok"}
