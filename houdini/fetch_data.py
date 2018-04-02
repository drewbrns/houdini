import os 
from pymongo import MongoClient
from twitter_data_source import TweetFetcher


MONGODB_URI = os.environ.get('MONGODB_URI', None)
REDIS_URI   = os.environ.get('REDIS_URI', None) 
APP_KEY     = os.environ.get('APP_KEY', None)
APP_SECRET  = os.environ.get('APP_SECRET', None)
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', None)
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', None)

options = {
    'MONGODB_URI': MONGODB_URI,
    'APP_KEY': APP_KEY,
    'APP_SECRET': APP_SECRET,
    'OAUTH_TOKEN': OAUTH_TOKEN,
    'OAUTH_TOKEN_SECRET': OAUTH_TOKEN_SECRET
}

filters = [
    'ipad', 'iphone', 'smartphone', 'smart phone', 'phone', 'mobile phone',
    'laptop', 'earphones', 'samsung', 'samsung galaxy s9', 'samsung s9+', 'galaxy s9', 'galaxy s9+',
    'macbook pro', 'macbook air', 'macbook', 'galaxy note 8', 'samsung galaxy note 8', 'iphone x',
    'microsoft surface', 'microsoft surface pro', 'microsoft surface laptop', 'microsoft surface book',
    'toyota', 'hyundai', 'ford', 'tesla', 'corolla', 'camry', 'totoya camry', 'toyota corolla', 'nissan',
    'beats by dre', 'samsung galaxy note 8.0',
]

def run():
    fetcher = TweetFetcher(
        options['APP_KEY'], options['APP_SECRET'],
        options['OAUTH_TOKEN'], options['OAUTH_TOKEN_SECRET']
    )
    client = MongoClient(os.environ.get('MONGODB_URI', None))
    db = client.houdini_db
    fetcher.fetch(filters, db)


if __name__ == '__main__':
    run()