import os 
from pymongo import MongoClient

SECRET_KEY = os.environ.get('HOUDINI_API_KEY', None)
MONGODB_URI = os.environ.get('MONGODB_URI', None)
SESSION_MONGODB = MongoClient(MONGODB_URI)