from textblob.classifiers import NaiveBayesClassifier
from pattern.en import parsetree


# Must do... Clean the document and standardize it.
# 1. Remove stop words.
# 2. Find lemma of all extracted verbs or objects (nouns) of interest.
 

PURCHASE_ACTION_WORDS = {'buy', 'recommend', 'hire', 'have', 'suggest', 'advise', 'want', 'need', 'purchase', 'wish'}
PURCHASE_OBJECT_CATEGORY = {}
VERB_TAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
NOUN_TAGS = ['NN', 'NNS', 'NNP', 'NNPS']


def purchase_intent_extractor(document):
    
    # Build a dictionary of Purchase Action words and purchase object words.
    # Set all to False, indicating absence, set to True when present in document as well as passing the PI test.
    features = {key: False for key in PURCHASE_ACTION_WORDS}
    
    sentences = parsetree(document, relations=True)
    
    for sentence in sentences:
        for chunk in sentence.chunks:
            print 'DEBUG: (chunk) -> {}, (chunk.type) -> {}'.format(chunk, chunk.type)
            if chunk.type == 'VP':
                words = [(w.string, w.type) for w in chunk.words]
                # 1. extract all verbs from sentence
                extracted_verbs = filter(lambda x: x[1] in VERB_TAGS, words)
                print 'DEBUG: (verbs) -> {}'.format(extracted_verbs)
                
                #2. are they purchase action words?
                extracted_verbs_set = {x[0] for x in extracted_verbs}
                intersection = PURCHASE_ACTION_WORDS.intersection(extracted_verbs_set)
                print '\tDEBUG: (intersection) -> {}'.format(intersection)
                print
                
                if intersection:
                    obj = chunk.object
                    if obj is not None:
                        if obj.type == 'NP':
                            # Check if object belongs to Purchase Object Category
                            print '\tDEBUG: (object) -> {}\n'.format(obj.string)                                                    
                            for verb in intersection:
                                features[verb] = True
    
    return features

# def purchase_intent_extractor_old(document):
#
#     pa_set = {pa_word.word for pa_word in PAWord.objects.all()}
#     po_set = {keyword for campaign in Campaign.objects.all() for keyword in campaign.get_keywords()}
#
#     vb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
#     noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
#
#     features = {}
#
#     s = parsetree(document, relations=True)
#
#     for sentence in s:
#
#         for chunk in sentence.chunks:
#
#             if chunk.type == 'VP':
#                 words = [(w.string, w.type) for w in chunk.words]
#                 #1. extract all verbs from sentence
#                 ext_vbs = filter(lambda x: x[1] in vb_tags, words)
#                 #2. are they purchase action words?
#                 ext_vbs_set = {x[0] for x in ext_vbs}
#                 intersection = pa_set.intersection(ext_vbs_set)
#
#                 if len(intersection):
#                     obj = chunk.object
#                     if obj is not None:
#                         # obj_words = [(w.string, w.type) for w in obj.words]
#                         # ext_nns = filter(lambda x: x[1] in noun_tags, obj_words)
#
#                         keywords_present = any(word in obj.string for word in po_set)
#
#                         if obj.type == 'NP' and keywords_present:
#                             for entry in intersection:
#                                 features[u'PA({0})'.format(entry)] = True
#                                 # features[u'PA'] = True
#                         else:
#                             pass
#                             # for entry in ext_nns:
#                             #     features[u'PO({0})'.format(entry)] = False
#                     else:
#                         #It does not have a direct OBJECT, what does this mean?
#                             #it means it is not a PI, but has PAs
#                             # a good place to capture ???
#                         pass
#
#                 else:
#                     #It does not contain PA words, what does this mean?
#                         #It means it is a VP but does not contain any PA
#                         #A good place to capture, Non-PA words
#                     # pass
#                     for entry in ext_vbs_set:
#                         features[u'PA({0})'.format(entry)] = False
#
#             else:
#                 #It is not a VP, what does this mean? it is definitely not a PI
#                 #So how do I capture the right features?
#                 pass
#
#     return features
    


if __name__ == '__main__':
    
    import pprint
    
    print 'Statement: I want to buy a phone'
    pprint.pprint(purchase_intent_extractor('I want to buy a phone'))
    print 
    print 'Statement: Mom can you recommend a farmers market where I could buy some oranges'    
    pprint.pprint(purchase_intent_extractor('Mom you recommend a farmers market where I could buy some oranges'))     
    print     
    print 'Statement: I need a recommendation'    
    pprint.pprint(purchase_intent_extractor('I need a recommendation'))
    print 
    print 'Statement: I have multiple phones but I need a new one, can you recommend to me something new?'
    pprint.pprint(purchase_intent_extractor('I have multiple phones but I need a new one, can you recommend to me something new?'))      