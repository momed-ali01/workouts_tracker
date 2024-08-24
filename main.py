from datetime import datetime
import requests
import os

# Load environment variables
APP_ID = os.environ["ENV_APP_ID"]
API_KEY = os.environ["ENV_API_KEY"]
API_TOKEN = os.environ["ENV_API_TOKEN"]
SHEET_ENDPOINT = os.environ["ENV_SHEET_ENDPOINT"]

# Define API endpoints
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"


def get_user_input(prompt):
    return input(prompt)


def process_data(datas):
    today = datetime.now()
    exercise = datas["name"].title()
    duration = datas["duration_min"]
    nf_calories = datas["nf_calories"]

    inputs = {
        "date": today.strftime("%d/%m/%Y"),
        "time": today.strftime("%H:%M:%S"),
        "exercise": exercise,
        "duration": duration,
        "calories": nf_calories
    }
    return inputs


# Set headers for API requests
exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

sheet_headers = {
    "Authorization": API_TOKEN
}

# Get user input for exercises
exercise_text = get_user_input("Tell me which exercises you did: ")

# Send exercise data to Nutritionix API
response = requests.post(url=EXERCISE_ENDPOINT, json={"query": exercise_text}, headers=exercise_headers)
exercises = response.json()["exercises"]

# Process and log exercise data
for data in exercises:
    workout = process_data(data)
    sheet_inputs = {"workout": workout}
    print(sheet_inputs)

    sheet_response = requests.post(url=SHEET_ENDPOINT, json=sheet_inputs, headers=sheet_headers)
    print(sheet_response.status_code)
