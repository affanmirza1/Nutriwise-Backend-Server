# medical_records.py
from mongo_connect import connect_to_mongo

mongo_client = connect_to_mongo()

db = mongo_client.Nutriwise  # Use the same database as in the previous file

def save_medical_record(email, medical_info):
    medical_records_collection = db.medical_records
    existing_medical_records = medical_records_collection.find_one({'email': email})

    if existing_medical_records:
        # Update existing medical records
        existing_medical_records['records'].append(medical_info)

        # Update the user's medical records in the collection
        update_data = {
            'records': existing_medical_records['records']
        }

        medical_records_collection.update_one(
            {'email': email},
            {'$set': update_data}
        )
    else:
        # Insert new medical records if they don't exist
        medical_records_data = {
            'email': email,
            'records': [medical_info]
        }

        medical_records_collection.insert_one(medical_records_data)

def get_medical_records(email):
    medical_records_collection = db.medical_records
    existing_medical_records = medical_records_collection.find_one({'email': email})

    if existing_medical_records:
        return existing_medical_records['records']
    else:
        return None
