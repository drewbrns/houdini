import os 

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

from nltk.tag.stanford import StanfordNERTagger
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
    'WPA', 'WNPA', 'SENTIMENT', 'CPO',
    'CNPO', 'ADO', 'ORG', 'LOC'    
]

NLTK_PATH = os.environ.get('NLTK_DATA', None)

stanford_tagger = StanfordNERTagger(
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
            row = {
               'WPA'  : self._extract_wpa(document),
               'WNPA' : self._extract_wnpa(document),               
               'SENTIMENT' : self._extract_sentiment(document),
               'CPO'  : int(self._extract_cpo(document)),
               'CPNO' : int(self._extract_cpno(document)),
               'ADO'  : self._extract_ado(document)
            }

            psd = self._extract_psd(document)
            row['LOC'] = psd['LOC']
            row['ORG'] = psd['ORG']

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
        s = wordnet.synsets(word, pos=VERB)[0]

        similarities = []
        append_sim = similarities.append

        for paword in PA_WORDS:
            pa_s = wordnet.synsets(paword, pos=VERB)[0]
            append_sim( s.similarity(pa_s) )

        return max(similarities)        
    

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
            s = wordnet.synsets(verb, pos=VERB)[0]               
            for paword in PA_WORDS:
                pa_s = wordnet.synsets(paword, pos=VERB)[0]                
                frame[paword][verb] = s.similarity(pa_s)

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
            s = wordnet.synsets(verb, pos=VERB)[0]               
            for paword in NON_PA_WORDS:
                pa_s = wordnet.synsets(paword, pos=VERB)[0]                
                frame[paword][verb] = s.similarity(pa_s)

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

        s = parsetree(document, relations=True, lemmata=True)
        for sentence in s:
            for chunk in sentence.chunks:
                
                # --- ado extraction --- 
                if chunk.type == 'VP' and chunk.object is not None:
                    
                    obj = chunk.object.string
                    verbs = [w.string for w in chunk.words]

                    for v in verbs:
                        PA_WORD_PRESENT = self._get_paword_similarity( v ) > 0.5
                        if PA_WORD_PRESENT:
                            break
                    
                    nouns = filter(lambda x: x.type in NOUN_TAGS, obj.words)        
                    nouns = set([noun.string for noun in nouns])                    
                    for n in nouns:                        
                        PO_CATEGORY_PRESENT = self._belongs_to_po_category( n )
                        if PO_CATEGORY_PRESENT:
                            break

                    if PA_WORD_PRESENT and PO_CATEGORY_PRESENT == True:
                        return int(PA_WORD_PRESENT and PO_CATEGORY_PRESENT)

                # --- ado extraction --- 


        return int(PA_WORD_PRESENT and PO_CATEGORY_PRESENT)


    def _extract_psd(self, document):
        """Purchase supportive words are the keywords that provide knowledge about 
              a particular Purchase Object or Purchase Action
           
           They are usually the names of locations or organizations related with the Purchase Object 
              or Purchase Action and this relation is captured in preposition based dependencies 
              in the text
           
           We extract two binary features related to PSD - ORG and LOC. 
           
           If there is an object belonging to PO category 
           that has a prepositionally dependent organization then ORG = 1 else ORG = 0. 
           
           Similarly, 
           
           if there is an object belonging to PO category 
           that has a prepositionally dependent location then LOC = 1 else LOC = 0
        """

        LOC = False
        ORG = False

        s = parsetree(document, relations=True, lemmata=True)
        for sentence in s:
            for chunk in sentence.chunks:
                if chunk.type == 'PP' and chunk.object is not None:
                    pnp = chunk.pnp
                    # NER 
                    break

        return {'LOC': LOC, 'ORG': ORG}




  

        
