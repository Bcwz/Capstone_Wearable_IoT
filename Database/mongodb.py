from datetime import date, datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

class mongoDatabase:
    
    def insertDatabase(currentDateTime):
        load_dotenv()
        URL = os.getenv('MONGODB_BASEURL')
        client = MongoClient(URL)
        db = client['Sensor']
        collection = db['DHT11']
        data = {"dateTime":currentDateTime}
        collection.insert_one(data)