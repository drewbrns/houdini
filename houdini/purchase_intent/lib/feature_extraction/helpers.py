import nltk
import textblob
from textblob import TextBlob
from nltk.corpus import stopwords

VERB_TAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
NOUN_TAGS = ['NN', 'NNS', 'NNP', 'NNPS']


def remove_stop_words(word_list):
    if not isinstance(word_list, list):
        raise (TypeError, '`word_list` argument must be a list')
    return [
        word for word in word_list if word not in set(stopwords.words('english'))
        ]


def extract_pos(blob, POS_TAGS):
    if not isinstance(blob, TextBlob):
        raise (TypeError, '`blob` argument must be a TextBlob')
    if not isinstance(POS_TAGS, list):
        raise (TypeError, '`POS_TAGS` argument must be a list')
    
    tokens = blob.tokenize()
    tokens = remove_stop_words(tokens)
    text = ''.join(tokens)
    tags = TextBlob(text).tags
    return filter(lambda x: x[1] in POS_TAGS, tags)


def extract_terms(blob, pos):
    if pos.lower() == 'verb' or pos.lower() == 'vb':
        verbs = extract_pos(blob, VERB_TAGS)
        return [x[0] for x in verbs]
    elif pos.lower() == 'noun' or pos.lower() == 'nn':
        nouns = extract_pos(blob, NOUN_TAGS)
        return [x[0] for x in nouns]
    elif pos.lower() == 'pronoun' or pos.lower() == 'pn':
        raise(Exception('Not implemented'))
    elif pos.lower() == 'adjective' or pos.lower() == 'adj':
        raise(Exception('Not implemented'))
    elif pos.lower() == 'adverb' or pos.lower() == 'adv':
        raise(Exception('Not implemented'))
    elif pos.lower() == 'preposition' or pos.lower() == 'pre':
        raise(Exception('Not implemented'))
    elif pos.lower() == 'conjunction' or pos.lower() == 'cn':
        raise(Exception('Not implemented'))
    elif pos.lower() == 'interjection' or pos.lower() == 'in':
        raise(Exception('Not implemented'))
    else:
        raise(Exception('Please provide valid pos. verb, noun, pronoun, adjective')) 
