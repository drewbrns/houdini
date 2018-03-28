import os
from twython import TwythonStreamer

APP_KEY = os.environ.get('APP_KEY', None)
APP_SECRET = os.environ.get('APP_SECRET', None)
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)
FILENAME = os.environ.get('FILENAME', None)

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
        # Want to disconnect after the first result?
        self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data


# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

stream.statuses.filter(track='twitter')
# stream.user()
# Read the authenticated users home timeline
# (what they see on Twitter) in real-time
# stream.site(follow='twitter')
