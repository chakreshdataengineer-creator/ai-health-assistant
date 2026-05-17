import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_meal_plan(goal):

    prompt = f"""
    You are an advanced AI nutrition planner and health coach.

    Create a healthy one-day Indian meal plan for this goal:
    {goal}

    Return ONLY valid JSON in this format:

    {{
        "goal": "",
        "total_calories": "",
        "breakfast": {{
            "meal": "",
            "calories": ""
        }},
        "lunch": {{
            "meal": "",
            "calories": ""
        }},
        "dinner": {{
            "meal": "",
            "calories": ""
        }},
        "snacks": {{
            "meal": "",
            "calories": ""
        }},
        "water_intake": "4 litres/day",
        "health_tip": ""
    }}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content