import os
import json
from twython import TwythonStreamer
from pymongo import MongoClient

#Mongo Host
MONGO_HOST= 'mongodb://mongo:27017/houdini_db'

APP_KEY = os.environ.get('APP_KEY', None)
APP_SECRET = os.environ.get('APP_SECRET', None)
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)
FILENAME = os.environ.get('FILENAME', None)

PA_WORDS = ['buy', 'recommend', 'hire', 'have', 'suggest', 'advise', 'want', 'need', 'purchase', 'wish']
PO_WORDS = ['iPad', 'sunglasses', 'pizza', 'dinner', 'holiday', 'hotel', 'vacation', 'need', 'purchase', 'wish']

class TweetStreamer(TwythonStreamer):
    def on_success(self, data):
        #Connect to mongoDB and store tweets
        try:
            client = MongoClient(MONGO_HOST)
            # Use houdini_db database. If it doesn't exist, it will be created.
            db = client.houdini_db

            print (data)

            # Decode the JSON from Twitter
            #data_json = json.load(data)
            #print(data_json)
                
            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(data['created_at']))
            
            #insert the data into the mongoDB into a collection called twitter_stream
            #if twitter_stream doesn't exist, it will be created.
            db.twitter_stream.insert(data)
        except Exception as e:
            print(e)
        # Want to disconnect after the first result?
        #self.disconnect()
    
    def on_error(self, status_code, data):
        print (status_code, data)
        
# Call TweetStreamer with Authentication
stream = TweetStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#Filter Streams with some Purchase Action Words
stream.statuses.filter(track=PA_WORDS)