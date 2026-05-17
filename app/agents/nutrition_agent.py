import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_food(food_input):

    prompt = f"""
    You are an advanced AI nutrition assistant.

    Analyze this meal:
    {food_input}

    Return ONLY valid JSON in this format:

    {{
        "estimated_calories": "",
        "protein": "",
        "carbohydrates": "",
        "fat": "",
        "health_score": "",
        "health_warnings": [],
        "suggestions": []
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