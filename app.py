from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, request, jsonify
from flask_cors import CORS
from Function import predict_image
from macros import calculate_bmr  # Import calculate_bmr function
from collection_handler import save_user_data, save_bmr_data, get_user_data
from mongo_connect import connect_to_mongo
from scheduler import reset_nutrients
from pytz import timezone
import os
import requests

app = Flask(__name__)
CORS(app)

NUTRITION_API_URL = "https://api.api-ninjas.com/v1/nutrition"
API_KEY = "l82xUDUirHuKYdX5BiVtHw==iFIGX68tmV3ncaZd"
karachi_timezone = timezone('Asia/Karachi')

app.config['SCHEDULER_API_ENABLED'] = True
app.config['JOBS'] = [
    {
        'id': 'reset_nutrients',
        'func': 'scheduler:reset_nutrients',
        'trigger': CronTrigger(hour=0, minute=0, timezone=karachi_timezone), 
    }
]

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def get_nutrition_info(food_query):
    try:
        headers = {'X-Api-Key': API_KEY}
        params = {'query': food_query}
        
        response = requests.get(NUTRITION_API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        nutrition_data = response.json()    
        return nutrition_data
    except requests.exceptions.RequestException as e:
        return {'error': f"Error accessing nutrition API: {str(e)}"}

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        image_file = request.files['image']
        email = request.form.get('email') 

        # Save the uploaded image temporarily
        image_path = 'temp.jpg'  
        image_file.save(image_path)

        # Call predict_image function
        prediction = predict_image(image_path)

        # Remove the temporary image
        os.remove(image_path)

        # Call the nutrition API with the prediction result
        nutrition_info = get_nutrition_info(prediction)

        # Save the user data
        save_user_data(email=email, nutrient_info=nutrition_info)

        return jsonify({'prediction': prediction, 'nutrition_info': nutrition_info})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/calculate_bmr', methods=['POST'])
def calculate_user_bmr():
    try:
        data = request.get_json()

        # Extract required parameters from the JSON data
        email = data['email']
        name = data['name']
        weight_kg = data['weight_kg']
        height_cm = data['height_cm']
        age = data['age']
        gender = data['gender']
        activity_level = data['activity_level']

        # Call the calculate_bmr function
        bmr_info = calculate_bmr(weight_kg, height_cm, age, gender, activity_level)

        # Save the BMR data and name against the email
        save_bmr_data(email=email, name=name, bmr_info=bmr_info)

        return jsonify({'bmr_info': bmr_info})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_user_data', methods=['GET'])
def get_user_data_api():
    try:
        email = request.args.get('email')  # Get email from query parameters

        # Call the get_user_data function
        user_data = get_user_data(email)

        # Convert ObjectId to string for JSON serialization
        if '_id' in user_data:
            user_data['_id'] = str(user_data['_id'])

        return jsonify({'user_data': user_data})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404  # HTTP 404 Not Found for user not found
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # HTTP 500 Internal Server Error for other exceptions



#Default route
@app.route('/')
def default():
    return 'Welcome to the Nutriwise Backend Server!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

