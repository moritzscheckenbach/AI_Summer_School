from fastapi import FastAPI
from .routers.day1 import router as day1_router

app = FastAPI(title="summerschool-2025 API", version="0.1.0")

app.include_router(day1_router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
