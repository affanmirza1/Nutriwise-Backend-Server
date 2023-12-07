# import os
# from mongo_connect import connect_to_mongo

# # Connect to MongoDB
# mongo_client = connect_to_mongo()
# print(mongo_client)
# db = mongo_client.Nutriwise

# def save_user_data(user_id, nutrient_info):
#     users_collection = db.users
#     existing_user_data = users_collection.find_one({'userid': user_id})

#     if existing_user_data:
#         existing_nutrient_info = existing_user_data.get('nutrients_intake', [])

#         for existing_nutrient, new_nutrient in zip(existing_nutrient_info, nutrient_info):
#             # Add the new values to the existing values
#             existing_nutrient['calories'] += new_nutrient.get('calories', 0)
#             existing_nutrient['serving_size_g'] += new_nutrient.get('serving_size_g', 0)
#             existing_nutrient['fat_total_g'] += new_nutrient.get('fat_total_g', 0)
#             existing_nutrient['fat_saturated_g'] += new_nutrient.get('fat_saturated_g', 0)
#             existing_nutrient['protein_g'] += new_nutrient.get('protein_g', 0)
#             existing_nutrient['sodium_mg'] += new_nutrient.get('sodium_mg', 0)
#             existing_nutrient['potassium_mg'] += new_nutrient.get('potassium_mg', 0)
#             existing_nutrient['cholesterol_mg'] += new_nutrient.get('cholesterol_mg', 0)
#             existing_nutrient['carbohydrates_total_g'] += new_nutrient.get('carbohydrates_total_g', 0)
#             existing_nutrient['fiber_g'] += new_nutrient.get('fiber_g', 0)
#             existing_nutrient['sugar_g'] += new_nutrient.get('sugar_g', 0)

#         # Update the user data in the collection with the modified existing_nutrient_info
#         users_collection.update_one(
#             {'userid': user_id},
#             {'$set': {'nutrients_intake': existing_nutrient_info}}
#         )
#     else:
#         # Insert new user data if it doesn't exist
#         user_data = {
#             'userid': user_id,
#             'nutrients_intake': nutrient_info
#         }
#         users_collection.insert_one(user_data)

import os
from mongo_connect import connect_to_mongo

# Connect to MongoDB
mongo_client = connect_to_mongo()
 
db = mongo_client.Nutriwise
def save_user_data(email, nutrient_info):
    users_collection = db.users
    existing_user_data = users_collection.find_one({'email': email})

    if existing_user_data:
        existing_nutrient_info = existing_user_data.get('nutrients_intake', [])

        if not existing_nutrient_info:
            # If the existing_nutrient_info is empty, initialize it with the default structure
            existing_nutrient_info = [[
                {
                    'name': 'onion',
                    'calories': 0,
                    'serving_size_g': 0,
                    'fat_total_g': 0,
                    'fat_saturated_g': 0,
                    'protein_g': 0,
                    'sodium_mg': 0,
                    'potassium_mg': 0,
                    'cholesterol_mg': 0,
                    'carbohydrates_total_g': 0,
                    'fiber_g': 0,
                    'sugar_g': 0
                }
            ]]

        # Update the existing nutrient information
        for existing_nutrient, new_nutrient in zip(existing_nutrient_info[0], nutrient_info):
            existing_nutrient['calories'] += new_nutrient.get('calories', 0)
            existing_nutrient['serving_size_g'] += new_nutrient.get('serving_size_g', 0)
            existing_nutrient['fat_total_g'] += new_nutrient.get('fat_total_g', 0)
            existing_nutrient['fat_saturated_g'] += new_nutrient.get('fat_saturated_g', 0)
            existing_nutrient['protein_g'] += new_nutrient.get('protein_g', 0)
            existing_nutrient['sodium_mg'] += new_nutrient.get('sodium_mg', 0)
            existing_nutrient['potassium_mg'] += new_nutrient.get('potassium_mg', 0)
            existing_nutrient['cholesterol_mg'] += new_nutrient.get('cholesterol_mg', 0)
            existing_nutrient['carbohydrates_total_g'] += new_nutrient.get('carbohydrates_total_g', 0)
            existing_nutrient['fiber_g'] += new_nutrient.get('fiber_g', 0)
            existing_nutrient['sugar_g'] += new_nutrient.get('sugar_g', 0)

        # Update the user data in the collection with the modified existing_nutrient_info
        update_data = {
            'nutrients_intake': existing_nutrient_info
        }

        users_collection.update_one(
            {'email': email},
            {'$set': update_data}
        )
    # No need to create a new user if the user doesn't exist

def save_bmr_data(email, name, bmr_info):
    users_collection = db.users
    existing_user_data = users_collection.find_one({'email': email})

    if existing_user_data:
        # Update the user data in the collection with the new BMR data and name
        update_data = {
            'name': name,
            'bmr_info': bmr_info,
            'nutrients_intake': existing_user_data.get('nutrients_intake', [])
        }

        # Initialize nutrient values to 0 for each nutrient
        for nutrient_array in update_data['nutrients_intake']:
            for nutrient_object in nutrient_array:
                for nutrient_key in nutrient_object:
                    nutrient_object[nutrient_key] = 0

        users_collection.update_one(
            {'email': email},
            {'$set': update_data}
        )
    else:
        # Insert new user data if it doesn't exist
        user_data = {
            'email': email,
            'name': name,
            'bmr_info': bmr_info,
            'nutrients_intake': [
                [
                    {
                        'name': 'onion',
                        'calories': 0,
                        'serving_size_g': 0,
                        'fat_total_g': 0,
                        'fat_saturated_g': 0,
                        'protein_g': 0,
                        'sodium_mg': 0,
                        'potassium_mg': 0,
                        'cholesterol_mg': 0,
                        'carbohydrates_total_g': 0,
                        'fiber_g': 0,
                        'sugar_g': 0
                    }
                ]
            ]
        }

        users_collection.insert_one(user_data)


def get_user_data(email):
    users_collection = db.users
    existing_user_data = users_collection.find_one({'email': email})

    if existing_user_data:
        return existing_user_data
    else:
        raise ValueError(f"User with email '{email}' not found.")

