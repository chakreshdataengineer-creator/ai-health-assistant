from fastapi import FastAPI

from app.api.food_api import router

from app.database.db import engine
from app.database.models import Base

from app.reminders.water_reminder import scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Health AI Agent Running"}