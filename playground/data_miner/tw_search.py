import os.path
from twython import Twython, TwythonError
import json
import io

APP_KEY = '8gwqTJfGUId1cPMeq7cWMs4cW'
APP_SECRET = 'fWm4bHFk7WveYw4r22fjgWFBILzmd4PywOc9K3wrJDse8XXoNY'
OAUTH_TOKEN = '144124443-sJya9WzRaHXh773f6wd77LzFTtG2db2zvWNhiy4q'
OAUTH_TOKEN_SECRET = 'P0wSdeUeQYaXfv2qfcZ19pSyybNCHrorxrdTLwJorCRq0'
FILENAME = 'data.json'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
try:
    search_results = twitter.search(q='twitter', count=1)
    # print json.dumps(search_results)
except TwythonError as e:
    print e

for tweet in search_results['statuses']:
    # tweet_data = 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'), tweet['created_at'])
    # tweet['text'].encode('utf-8'), '\n'

    tweet_data = json.dumps({'created_at': tweet['created_at'], 'screen_name': tweet['user']['screen_name'].encode(
        'utf-8'), 'text':  tweet['text'].encode('utf-8')})
    print tweet_data

    a = []
    # Check if FILENAME exist else create it
    if os.path.isfile(FILENAME):
        with io.open(FILENAME, encoding='utf-8') as f:
            feeds = json.load(open(FILENAME))
            feeds.append(tweet_data)
        with io.open(FILENAME, mode='w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(feeds, indent=1, ensure_ascii=False)))
    else:
        a.append(tweet_data)
        with io.open(FILENAME, mode='w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(a, indent=1, ensure_ascii=False)))
