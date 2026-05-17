from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.agents.nutrition_agent import analyze_food
from app.agents.meal_planner_agent import generate_meal_plan

from app.database.db import SessionLocal
from app.database.models import MealLog, WaterLog

router = APIRouter()

class FoodRequest(BaseModel):
    meal: str

class WaterRequest(BaseModel):
    litres: int

class BMIRequest(BaseModel):
    weight: float
    height: float
    age: int

class MealPlanRequest(BaseModel):
    goal: str

@router.post("/analyze-food")
def analyze(request: FoodRequest):

    result = analyze_food(request.meal)

    parsed_result = json.loads(result)

    db = SessionLocal()

    meal_log = MealLog(
        meal=request.meal,
        calories=parsed_result["estimated_calories"],
        protein=parsed_result["protein"],
        health_score=parsed_result["health_score"]
    )

    db.add(meal_log)

    db.commit()

    db.refresh(meal_log)

    db.close()

    return parsed_result

@router.get("/meal-history")
def meal_history():

    db = SessionLocal()

    meals = db.query(MealLog).all()

    db.close()

    return meals

@router.get("/daily-summary")
def daily_summary():

    db = SessionLocal()

    meals = db.query(MealLog).all()

    total_calories = 0

    total_protein = 0

    for meal in meals:

        calories = ''.join(filter(str.isdigit, meal.calories))

        protein = ''.join(filter(str.isdigit, meal.protein))

        if calories:
            total_calories += int(calories)

        if protein:
            total_protein += int(protein)

    warning = "Healthy"

    if total_calories > 2500:
        warning = "High calorie intake detected"

    if total_protein < 50:
        warning = "Low protein intake"

    db.close()

    return {
        "daily_calories": total_calories,
        "daily_protein": f"{total_protein}g",
        "meals_logged": len(meals),
        "health_warning": warning
    }

@router.post("/water-intake")
def water_intake(request: WaterRequest):

    db = SessionLocal()

    water = WaterLog(
        litres=request.litres
    )

    db.add(water)

    db.commit()

    db.refresh(water)

    db.close()

    status = "Good hydration"

    if request.litres < 4:
        status = "Drink more water"

    return {
        "water_intake": f"{request.litres} litres",
        "daily_target": "4 litres",
        "status": status
    }

@router.post("/bmi")
def bmi(request: BMIRequest):

    bmi_value = request.weight / ((request.height / 100) ** 2)

    category = "Normal"

    if bmi_value < 18.5:
        category = "Underweight"

    elif bmi_value > 25:
        category = "Overweight"

    return {
        "age": request.age,
        "weight": request.weight,
        "height": request.height,
        "bmi": round(bmi_value, 2),
        "category": category
    }

@router.post("/meal-plan")
def meal_plan(request: MealPlanRequest):

    result = generate_meal_plan(request.goal)

    parsed_result = json.loads(result)

    return parsed_result