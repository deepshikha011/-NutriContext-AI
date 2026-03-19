import json
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
)


def analyze_meal(image: Image.Image, goal: str, meal_context: str) -> dict:
    prompt = f"""
You are a professional nutritionist AI. Analyze the food in this image.

User Goal: {goal}
Meal Context: {meal_context}

Respond ONLY with a valid JSON object in this exact format (no markdown, no extra text):
{{
  "food_name": "string",
  "calories": integer,
  "protein_g": float,
  "carbs_g": float,
  "fats_g": float,
  "health_score": integer (0-100),
  "verdict": "string (1-2 sentences about this meal for the user's goal)",
  "smart_swap": "string (a healthier alternative suggestion, or null if meal is already healthy)"
}}

Be realistic with calorie estimates. health_score should reflect how well this meal aligns with the user's goal.
"""
    try:
        response = model.generate_content([prompt, image])
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except (json.JSONDecodeError, IndexError, Exception) as e:
        return {"error": str(e)}
