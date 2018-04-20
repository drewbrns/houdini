import os
import time
from twython import TwythonStreamer
from twython.exceptions import TwythonError, TwythonRateLimitError, TwythonAuthError, TwythonStreamError

from .extractor import Extractor
from .helpers import to_slack


class TweetFetcher(TwythonStreamer):

    def on_success(self, data):
        try:
            extractor = Extractor(data)
            validated_data = extractor.validated_data()
            self.houdini_db.data_lake.insert_one(
                validated_data
            )
            print ('[TweetFetcher] Tweet collected at: {}'.format(str(data['created_at'])))
        except Exception as e:
            # print(data['retweeted_status'])
            # print(e)
            pass 
    
    def on_error(self, status_code, data):
        raise (status_code, data)

    def fetch(self, filters, db):
        try:
            self.houdini_db = db         
            self.statuses.filter(track=filters)
        except TwythonRateLimitError as e:
            retry_after = e.retry_after
            if retry_after:
                time.sleep(retry_after)
                self.fetch( filters, db )
            to_slack(
                'Rate limit exceeded retrying after {} seconds.'.format(retry_after)
            )
        except ( TwythonAuthError, TwythonError,  TwythonStreamError ) as e:
            print(e)            
            time.sleep(60)
            self.fetch( filters, db )                
        except Exception as e:
            print(e)            
            time.sleep(60)
            self.fetch( filters, db )