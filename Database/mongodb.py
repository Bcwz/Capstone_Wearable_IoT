import os
from dotenv import load_dotenv
from datetime import date, datetime
from pymongo import MongoClient

class mongoDatabase:
    
    def insertDatabase(dbURL,tableName,collectionName, currentDateTime):
        client = MongoClient(dbURL)
        db = client[tableName]
        collection = db[collectionName]
        data = {"dateTime":currentDateTime}
        collection.insert_one(data)