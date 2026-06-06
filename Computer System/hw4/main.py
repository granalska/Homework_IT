import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session
from conf.db import get_db

app = FastAPI()

BASE_DIR = Path(__file__).parent
directory = BASE_DIR.joinpath("static")
app.mount("/static", StaticFiles(directory = directory), name = "static")
templates = Jinja2Templates(directory = BASE_DIR / "templates")

@app.get("/", response_class = HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse(request = request, name = "index.html", context = {"request": request, "our": "Домашня робота №4"})

@app.get("/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail = "Помилка підключення до бази даних")
        return {"message": "Ласкаво прошу to FastAPI"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail = "Невірно налаштована база даних")

if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = int(os.environ.get("PORT", 8000)), log_level = "info", reload = True)
