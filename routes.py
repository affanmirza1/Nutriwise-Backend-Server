from flask import Blueprint, request, jsonify
from flask_cors import CORS
from Function import predict_image  # Import your function
import os
import requests
import json

prediction_routes = Blueprint('prediction_routes', __name__)
CORS(prediction_routes)

NUTRITION_API_URL = "https://api.api-ninjas.com/v1/nutrition"
API_KEY = "l82xUDUirHuKYdX5BiVtHw==iFIGX68tmV3ncaZd"

def get_nutrition_info(food_query):
    try:
        headers = {'X-Api-Key': API_KEY}
        params = {'query': food_query}
        
        response = requests.get(NUTRITION_API_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            try:
                nutrition_data = response.json()
                return nutrition_data
            except json.JSONDecodeError:
                return {'error': 'Failed to parse JSON response'}
        else:
            return {'error': f"API Error: {response.status_code} - {response.content.decode('utf-8')}"}
    except requests.exceptions.RequestException as e:
        return {'error': f"Error accessing nutrition API: {str(e)}"}

@prediction_routes.route('/prediction', methods=['POST'])  # Updated route name
def upload_image():
    try:
        image_file = request.files['image']

        # Save the uploaded image temporarily
        image_path = 'temp.jpg'  # Choose a temporary path
        image_file.save(image_path)

        # Call your predict_image function
        prediction = predict_image(image_path)

        # Remove the temporary image
        os.remove(image_path)

        # Call the nutrition API with the prediction result
        nutrition_info = get_nutrition_info(prediction)

        return jsonify({'prediction': prediction, 'nutrition_info': nutrition_info})
    except Exception as e:
        return jsonify({'error': str(e)})
