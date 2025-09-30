from fastapi import FastAPI
from .routers.day1 import router as day1_router
from .routers.day2 import router as day2_router
from .routers.day3 import router as day3_router
from .routers.day4 import router as day4_router

app = FastAPI(title="summerschool-2025 API", version="0.1.0")

app.include_router(day1_router)
app.include_router(day2_router)
app.include_router(day3_router)
app.include_router(day4_router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
