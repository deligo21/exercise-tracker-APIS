from dotenv import load_dotenv
import os
import requests
from datetime import datetime

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

GENDER = "MALE"
WEIGHT_KG = "75"
HEIGHT = "175"
AGE = "20"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id":APP_ID,
    "x-app-key": APP_KEY,
}

user_input = input("Tell me wich exercises you did: ")

body_exercise = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(exercise_endpoint, json=body_exercise, headers=headers)
response.raise_for_status()
exercise_data = response.json()

shetty_endpoint = f"https://api.sheety.co/{os.getenv('USERNAME')}/workoutTracking/workouts"
date_today = datetime.now().strftime("%m/%d/%Y")
hour_today = datetime.now().strftime("%X")

list_data = [[item["name"], item["duration_min"],item["nf_calories"] ] for item in exercise_data["exercises"]]

for row in list_data:
    
    headers_sheet = {
        "Authorization": f"Bearer {os.getenv('BEARER_TOKEN')}"
    }
    body = {
        "workout": {
            "date":date_today,
            "time":hour_today,
            "exercise": row[0].title(),
            "duration": row[1],
            "calories": row[2]}
    }
    
    response_sheet = requests.post(shetty_endpoint, json=body, headers=headers_sheet)
    response_sheet.raise_for_status()
    print(response_sheet.json())