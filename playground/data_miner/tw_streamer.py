from twython import TwythonStreamer

APP_KEY = '8gwqTJfGUId1cPMeq7cWMs4cW'
APP_SECRET = 'fWm4bHFk7WveYw4r22fjgWFBILzmd4PywOc9K3wrJDse8XXoNY'
OAUTH_TOKEN = '144124443-sJya9WzRaHXh773f6wd77LzFTtG2db2zvWNhiy4q'
OAUTH_TOKEN_SECRET = 'P0wSdeUeQYaXfv2qfcZ19pSyybNCHrorxrdTLwJorCRq0'

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
