# scheduler.py
from collection_handler import connect_to_mongo

def reset_nutrients():
    try:
        # Connect to MongoDB
        mongo_client = connect_to_mongo()
        db = mongo_client.Nutriwise
        users_collection = db.users

        # Reset nutrients intake for all users
        users_collection.update_many({}, {'$set': {'nutrients_intake': []}})
        print("Nutrients intake reset successfully.")
    except Exception as e:
        print(f"Error resetting nutrients intake: {str(e)}")
