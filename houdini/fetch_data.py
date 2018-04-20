import os

from pymongo import MongoClient
from data import TweetFetcher

options = {
    'MONGODB_URI': os.environ.get('MONGODB_URI', None),
    'APP_KEY': os.environ.get('APP_KEY', None),
    'APP_SECRET': os.environ.get('APP_SECRET', None),
    'OAUTH_TOKEN': os.environ.get('OAUTH_TOKEN', None),
    'OAUTH_TOKEN_SECRET': os.environ.get('OAUTH_TOKEN_SECRET', None),
    'REDIS_URI': os.environ.get('REDIS_URI', None)
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
    client = MongoClient(options['MONGODB_URI'])
    db = client.houdini_db

    beach_filter = ['want beach maldives', 'want beach caribbean', 'travel beach maldives', 'recommend beach maldives']
    food_filter  = ['want pizza', 'purchase pizza', 'buy pizza', 'recommend pizza', 'want dinner', 'buy dinner', 'buy lunch', 'purchase lunch', 'obtain lunch']
    hour_filter  = ['need hour', 'need year', 'purchase hour', 'need peace', 'want combat', 'desire combat', 'wish combat']
    phone_filter = ['suggest phone', 'buy phone', 'want phone', 'buy iphone', 'buy ipad', 'purchase ipad', 'purchase iphone']
    peace_filter = ['obtain peace', 'recommend peace', 'desire peace', 'need peace']

    fetcher.fetch( beach_filter, db )
    fetcher.fetch( food_filter , db )
    fetcher.fetch( hour_filter , db )
    fetcher.fetch( phone_filter, db )
    fetcher.fetch( peace_filter, db )


if __name__ == '__main__':
    run()