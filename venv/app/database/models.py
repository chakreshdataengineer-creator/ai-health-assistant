from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MealLog(Base):

    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)

    meal = Column(String)

    calories = Column(String)

    protein = Column(String)

    health_score = Column(String)

class WaterLog(Base):

    __tablename__ = "water_logs"

    id = Column(Integer, primary_key=True, index=True)

    litres = Column(Integer)