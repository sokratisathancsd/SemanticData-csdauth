'''
@author: Sokratis Athanasiadis
'''
from nltk.corpus import wordnet as wn
#use this to singularized words 
#(ex. gills to gill to avoid WordNetError: no lemma 'gills' with part of speech 'n')
from pattern.text.en import singularize 

class WordNet:  
    def __init__(self, data, term):
        term = wn.synset(term+'.n.01')
        #data is a dictionary we store the input data (the one we retrieve from ConceptNet)
        self.data = data
        #term is given from user
        self.term = term
        self.WordNetData = dict()
       
    def getData(self):
        for relation in self.data.keys():
            for value in self.data[relation]:
                word = value[0]
                try:
                    keepTheWord = word
                    word = singularize(word)
                    word = wn.synset(word+'.n.01')
                    common = self.term.lowest_common_hypernyms(word)[0]
                    distance = abs(self.term.min_depth() + word.min_depth() - 2*common.min_depth())
                except:
                    #print('can not find depth diff for word: '+word)
                    #and the distance is None
                    distance = None
            
                if relation in self.WordNetData:
                    self.WordNetData[relation].append([keepTheWord, distance])
                else:
                    self.WordNetData[relation] = []
                    self.WordNetData[relation].append([keepTheWord, distance])
        return self.WordNetData

    
    
    
'''
#code projects graph and depth of word1 and word2
#code computes distance between the 2 words

from nltk.corpus import wordnet as wn
from pprint import pprint
hyp = lambda s:s.hypernyms() #we use this to print the tree
term1 = 'virus'
term2 = 'microorganism'

pprint(wn.synset(term1+'.n.01').tree(hyp))
print(wn.synset(term1+'.n.01').min_depth())
print('\n')

pprint(wn.synset(term2+'.n.01').tree(hyp))
print(wn.synset(term2+'.n.01').min_depth())
print('\n')

commonTerm = wn.synset(term1+'.n.01').lowest_common_hypernyms(wn.synset(term2+'.n.01'))[0]
pprint(commonTerm.tree(hyp))
print(commonTerm.min_depth())
print('\n')
'''
    