from pymongo import MongoClient 
from dotenv import load_dotenv
import os
from utils.constants import MONGODB_URI
load_dotenv("../dev.env")  # Load environment variables from .env file

def init_mongo_connnection():
    
    global client 
    client =  MongoClient(os.environ.get(MONGODB_URI))
    client.admin.command('ping')
    print("Connected to MongoDB")



def get_mongo_client():
    return client