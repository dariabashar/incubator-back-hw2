from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from src.assistant.api import router as assistant_router
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_db

app = FastAPI()

app.include_router(assistant_router, tags=["assistant"])
app.mount("/static", StaticFiles(directory="src/static"),name="static")
    
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("src/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def check_health(db: AsyncSession = Depends(get_async_db)):
    try:
        await db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Database connection failed"
        )

    return {"status": "ok", "database": "connected"}
