'''
@author: Sokratis Athanasiadis
'''
#requests library is used to get the json file from http://api.conceptnet.io/c/en/
#only english words are supported
import requests

class ConceptNet:
    def __init__(self, term):
        #term is given from user
        self.term = term
        #data to return
        #data is a dictionary in this format 
        #[[Relation1: [word1 , weight1],[word2 , weight2]],[Relation2: [word3 , weight3],[word4 , weight4]],...
        self.data = dict()
    
    def getData(self):
        response = requests.get('http://api.conceptnet.io/c/en/'+self.term+'?offset=0&limit=1000')
        obj=response.json()
        
        '''Convert json text Data to a Dictionary'''
        for resurl in obj['edges']:    
            #take the source
            source = resurl['sources'][0]['@id']        
            #take the id
            resurl1 = resurl['@id']
            resurl1 = resurl1.replace(","," ")
            tempWords = resurl1.split()
            #filtering the sources of results
            if 'wordnet' in source or 'verbosity' in source: 
                relation = tempWords[0][7:][:-1]
                #keep only the triples with the given entity
                if '/c/en/'+self.term+'/' in tempWords[1]: 
                    second=tempWords[2].split("/")[3]
                if '/c/en/'+self.term+'/' in tempWords[2]:
                    second=tempWords[1].split("/")[3]
                weight = resurl['weight']
                #add on dictionary
                if relation in self.data:
                    self.data[relation].append([second, weight])
                else:
                    self.data[relation] = []
                    self.data[relation].append([second, weight])

        #remove some properties we don't need
        propertiesToRem = ['Synonym', 'Antonym', 'NotHasProperty', 'ExternalURL', 'EtymologicallyDerivedFrom', 'FormOf', 'HasSubevent', 'HasFirstSubevent', 'HasLastSubevent', 'DistinctFrom', 'SymbolOf', 'DefinedAs']
        for remKey in propertiesToRem:
            self.data.pop(remKey, None)
    
        return self.data