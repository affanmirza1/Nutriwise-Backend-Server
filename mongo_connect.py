from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
ca = certifi.where()

def connect_to_mongo():
    password = "6uyiD4hNwyxNUxdi"


    uri = f"mongodb+srv://affanmirza1:{password}@cluster0.iccn5c0.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)
   
    try:
        db = client.Nutriwise  
        if 'dummy_collection' not in db.list_collection_names():
            print("Database 'Nutriwise' does not exist. Creating...")
            db.create_collection("dummy_collection") 
            print("Database 'Nutriwise' created successfully.")
        else:
            print("Database 'Nutriwise' already exists.")
    except Exception as e:
        print(f"Error creating 'Nutriwise' database: {e}")

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None
