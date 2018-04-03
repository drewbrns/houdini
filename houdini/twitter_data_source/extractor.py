import re
import time 
import html
from textblob import TextBlob


class Extractor():
    
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def get_text(self):
        data = self.raw_data
        retweeted_data = data.get('retweeted_status', None)    
        extended_tweet = data.get('extended_tweet', None)    
        text = data.get('text', None)        

        if retweeted_data is not None:
            extended = retweeted_data.get('extended_tweet', None)
            if extended is not None:
                full = extended.get('full_text', None)
                if full is not None:
                    return full

        elif extended_tweet is not None:
            full_text = extended_tweet.get('full_text', None)
            if full_text is not None:
                return full_text

        elif text is not None:
            return text
        
        raise Exception('Tweet must contain text')         
            
    def clean_created_at(self, created_at):
        # convert `created_at` to unix timestamp
        # Fri Mar 30 17:53:28 +0000 2018
        try:
            parsed = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')        
            return int(time.mktime( parsed )) - time.timezone
        except Exception as e:
            raise e        

    def clean_text(self, text):
        # replace any url found with domain of the url
        text = text.strip()
        text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')
        text = html.unescape(text)

        b = TextBlob(u"{}".format(text))
        if b.detect_language() != 'en':
            raise Exception('Tweet must be english')
        return text

    def clean_source(self, url):
        # extract anchor name from url in `source` 
        try:
            text = re.sub('<[^<]+?>', '', url)
            return text
        except Exception as e:
            raise e            

    def validated_data(self):
        data = self.raw_data

        if data['is_quote_status'] or data['user']['lang'].lower() == 'en':
            raise Exception('Skip this tweet')
        return {
            'created_at': self.clean_created_at( data['created_at'] ),
            'text': self.clean_text( self.get_text() ),
            'source': self.clean_source( data['source'] ),
        }