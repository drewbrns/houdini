import os
import io
import json
from twython import Twython, TwythonError

APP_KEY = os.environ.get('APP_KEY', None)
APP_SECRET = os.environ.get('APP_SECRET', None)
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)
FILENAME = os.environ.get('FILENAME', None)

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
