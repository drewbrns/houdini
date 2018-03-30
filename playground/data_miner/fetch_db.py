from pymongo import MongoClient

MONGO_HOST= 'mongodb://mongo:27017/houdini_db'

client = MongoClient(MONGO_HOST)
db = client.houdini_db
print (list(db.twitter_stream.find()))