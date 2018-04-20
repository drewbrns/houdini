import os 
import itertools

from pattern.vector import count, words
from pattern.vector import stem, PORTER, LEMMA
from pattern.vector import Document, Model, TFIDF, IG, BINARY
from pattern.vector import Vector, distance, tfidf

from pattern.en import parse, Sentence, parsetree
from pattern.en import wordnet, NOUN, VERB, ADJECTIVE, ADVERB
from pattern.en import sentiment

from textblob import TextBlob

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize


# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
VERB_TAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
NOUN_TAGS = ['NN', 'NNS', 'NNP', 'NNPS']

PA_WORDS  = [
    'buy', 'recommend', 'hire', 'have',
    'suggest', 'advise', 'want', 'need', 'purchase',
    'wish', 'pay'
]

NON_PA_WORDS = [
    'came', 'facing', 'disappear', 'joking', 'betray',
    'share', 'fill', 'allow', 'shoot', 'reproduce'
]

PO_CATEGORIES = ['consumer product', 'food', 'hospitality business']
NPO_CATEGORIES = ['unit of time', 'religion', 'military conflict']


FEATURE_LABELS = [
    'WPA', 'WNPA', 'SENTIMENT', 'CPO', 'CPNO', 'ADO', 'ORG', 'LOC', 'CLASS'
]

NLTK_PATH = os.environ.get('NLTK_DATA', None)

tagger = StanfordNERTagger(
    os.path.join(NLTK_PATH, 'stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'),
    os.path.join(NLTK_PATH, 'stanford-ner/stanford-ner.jar'),
    encoding='utf-8'
)


class BasicExtractor(object):

    def __init__(self, documents):
        self.documents = documents
        self._features = self._extract_features(documents)

    def get_features(self):
        return self._features

    def _extract_features(self, documents):
        
        features = []
        append_features = features.append
        
        for document in documents:

            text   = document['text']
            target = document['class'] 
            
            row = {
                'WPA'  : self._extract_wpa(text),
                'WNPA' : self._extract_wnpa(text),
                'SENTIMENT' : self._extract_sentiment(text),
                'CPO'  : int(self._extract_cpo(text)),
                'CPNO' : int(self._extract_cpno(text))
            }
            
            ado, _, poword = self._extract_ado(text)
            psd = self._extract_psd(poword)

            row['ADO'] = ado
            row['LOC'] = psd['LOC']
            row['ORG'] = psd['ORG']
            row['CLASS'] = 1 if target.lower() == 'pi' else 0

            append_features(row)

        return DataFrame(features, columns=FEATURE_LABELS)


    def _get_verbs(self, document):
        blob = TextBlob(document)
        tags = filter(lambda x: x[1] in VERB_TAGS, blob.tags)
        return set([verb[0] for verb in tags])


    def _get_nouns(self, document):
        blob = TextBlob(document)
        tags = filter(lambda x: x[1] in NOUN_TAGS, blob.tags)
        return set([noun[0] for noun in tags])


    def _get_paword_similarity(self, word):
        s = wordnet.synsets(word, pos=VERB)

        if len(s) > 0:
            s = s[0]
            similarities = []
            append_sim = similarities.append

            for paword in PA_WORDS:
                pa_s = wordnet.synsets(paword, pos=VERB)
                if len(pa_s) > 0:
                    pa_s = pa_s[0]
                    append_sim( s.similarity(pa_s) )
                else:
                    append_sim( 0 )

            return max(similarities)
        else:
            return 0


    def _belongs_to_po_category(self, word):
        # check membership
        return False 


    def _belongs_to_npo_category(self, word):
        # check membership
        return False 


    def _extract_wpa(self, document):

        verbs = self._get_verbs(document)

        row_size = len(verbs)
        column_size = len(PA_WORDS)

        frame = DataFrame(
            np.empty((row_size, column_size)),
            index=verbs, columns=PA_WORDS
        )

        for verb in verbs:
            s = wordnet.synsets(verb, pos=VERB)
            if len(s) > 0:
                s = s[0]
                for paword in PA_WORDS:
                    pa_s = wordnet.synsets(paword, pos=VERB)
                    if len(pa_s) > 0:
                        pa_s = pa_s[0]
                        frame[paword][verb] = s.similarity(pa_s)
                    else:
                        frame[paword][verb] = 0
            else:
                for paword in PA_WORDS:
                    frame[paword][verb] = 0
                

        return max(frame.max())


    def _extract_wnpa(self, document):
        
        verbs = self._get_verbs(document)

        row_size = len(verbs)
        column_size = len(NON_PA_WORDS)

        frame = DataFrame(
            np.empty((row_size, column_size)),
            index=verbs, columns=NON_PA_WORDS
        )

        for verb in verbs:
            s = wordnet.synsets(verb, pos=VERB)
            if len(s) > 0:
                s = s[0]
                for paword in NON_PA_WORDS:
                    pa_s = wordnet.synsets(paword, pos=VERB)                    
                    if len(pa_s) > 0:
                        pa_s = pa_s[0]                        
                        frame[paword][verb] = s.similarity(pa_s)
                    else:
                        frame[paword][verb] = 0
            else:
                for paword in NON_PA_WORDS:
                    frame[paword][verb] = 0

        return max(frame.max())


    def _extract_sentiment(self, document):
        return sentiment(document)[0]


    def _extract_cpo(self, document):
        nouns = self._get_nouns(document)
        return 0 


    def _extract_cpno(self, document):
        nouns = self._get_nouns(document)
        return 0


    def _extract_ado(self, document):
        """
            PA word has dependent object of PO category (ADO)

            In a PI post, a purchase action is targeted towards a consumable object. 
            This is reflected in the dependency structure of the text.

            In a PI post, the consumable object is usually the directly 
            dependent object of the purchase action verb.

            If there is a PA word in the text and it has a dependent object belonging to a PO category, ADO = 1, otherwise ADO = 0
        """

        # 1. Identify if there is a PA word. (or a very similar one)
        # 2. Identify if this PA word has an object.
        # 3. Identify if this object belongs to the PO category.
        # 4. If the 3 statements above are true, return ADO = 1 else ADO = 0

        PA_WORD_PRESENT = False
        PO_CATEGORY_PRESENT = False
        pa_word = None
        po_word = None

        text = parsetree(document, relations=True, lemmata=True)

        for sentence in text:
            
            for chunk in sentence.chunks:

                if chunk.type == 'VP' and chunk.object is not None:
                    
                    pa_word = chunk.head
                    po_word = chunk.object

                    PA_WORD_PRESENT = self._get_paword_similarity( pa_word ) > 0.5

                    nouns = filter(lambda x: x.type in NOUN_TAGS, po_word.words)
                    nouns = set([noun.string for noun in nouns])

                    PO_CATEGORY_PRESENT = any([self._belongs_to_po_category( n ) for n in nouns])

                    if PA_WORD_PRESENT and PO_CATEGORY_PRESENT:
                        return ( 
                            int(PA_WORD_PRESENT and PO_CATEGORY_PRESENT), 
                            pa_word, po_word
                        )

        return ( 
            int(PA_WORD_PRESENT and PO_CATEGORY_PRESENT), 
            pa_word, po_word 
        )


    def _extract_psd(self, purchase_object):

        PSD = {'LOC': 0, 'ORG': 0}

        prep_phrase = purchase_object.nearest(type='PP')
        if prep_phrase is not None:
            noun_phrase = prep_phrase.next(type='NP')
            tokenized  = [ word_tokenize(word.string) for word in noun_phrase ]
            classified = tagger.tag_sents(tokenized)
            flattened  = itertools.chain.from_iterable(classified)
                
            PSD['LOC'] = int( any(filter(lambda x: x[1] == 'LOCATION', flattened)) )
            PSD['ORG'] = int( any(filter(lambda x: x[1] == 'ORGANIZATION', flattened)) )

            return PSD 
        else:            
            return PSD
