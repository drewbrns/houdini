import os

from pymongo import MongoClient
from twitter_data_source import TweetFetcher


MONGODB_URI = os.environ.get('MONGODB_URI', None)
REDIS_URI   = os.environ.get('REDIS_URI', None) 
APP_KEY     = os.environ.get('APP_KEY', None)
APP_SECRET  = os.environ.get('APP_SECRET', None)
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)
REDIS_URI   = os.environ.get('REDIS_URI', None)

options = {
    'MONGODB_URI': MONGODB_URI,
    'APP_KEY': APP_KEY,
    'APP_SECRET': APP_SECRET,
    'OAUTH_TOKEN': OAUTH_TOKEN,
    'OAUTH_TOKEN_SECRET': OAUTH_TOKEN_SECRET,
    'REDIS_URI': REDIS_URI
}

pa_words = [
    'buy', 'recommend', 'hire', 'have', 'suggest', 'advise', 
    'want', 'need', 'purchase', 'wish', 'acquire', 'obtain', 
    'came', 'facing', 'disappear', 'joking', 'betray', 'share',
    'fill', 'allow', 'shoot', 'reproduce'
]

po_words = [
    'iPad', 'sunglasses', 'pizza', 'dinner', 'hour', 'year', 'Pope', 'Islam', 'war', 'combat'
]


def run():
    fetcher = TweetFetcher(
        options['APP_KEY'], options['APP_SECRET'],
        options['OAUTH_TOKEN'], options['OAUTH_TOKEN_SECRET']
    )
    client = MongoClient(os.environ.get('MONGODB_URI', None))
    db = client.houdini_db
    filters = []
    add_to_filters = filters.append

    for verb in pa_words:
        for obj in po_words:
            add_to_filters(verb + ' ' + obj)

    fetcher.fetch(filters, db)


if __name__ == '__main__':
    run()