'''
@author: Sokratis Athanasiadis
'''
#sparql requests handler
from SPARQLWrapper import SPARQLWrapper, JSON
#class for tf-idf and cosine similarity scores
from TfIdf import TfIdf
import wikipedia

class DBpedia:
    def __init__(self, data, term):
        #data is a dictionary with the input data (the one retrieved from ConceptNet)
        self.data = data
        #term is the input word
        self.term = term
        #data to return
        #DBdata is a dictionary in this format 
        #[[Relation1: [word1 , CommentBox1],[word2 , CommentBox2]],[Relation2: [word3 , CommentBox3],[word4 , CommentBox4]],...
        self.DBdata = dict()
        
    def getData(self):
        for relation in self.data.keys():
            for word in self.data[relation]:
                '''try 3 times with 3 different method to find the word in DBpedia'''
                '''1st try || Capitalize each word because in DBpedia the word needs to be capitalized'''
                results = DBpedia.Query(word[0].capitalize())
                if not results["results"]["bindings"]:
                    ''' 2nd try || word 'Bass' doesn't exist, but Bass_(fish) exists
                       adds '_(term)' in the end of the word '''
                    results = DBpedia.Query(word[0].capitalize()+"_("+self.term+")")
                    
                    if not results["results"]["bindings"]: 
                        '''3rd try || word schrod doesn't exist, but Scrod (same word) exists 
                           uses wikipedia to correct the word '''
                        wikiTerms = wikipedia.search(word[0].capitalize())
                        #replace " " with "_" because the words in DBpedia are seperated by this char "_"
                        wikiWord = wikiTerms[0].replace(" ", "_")
                        results = DBpedia.Query(wikiWord)
                        
                        '''If can't find the word in DBpedia the weight is None'''
                        if not results["results"]["bindings"]: 
                            if relation in self.DBdata:
                                self.DBdata[relation].append([word[0], None])
                            else:
                                self.DBdata[relation] = []
                                self.DBdata[relation].append([word[0], None])
            
                #add the data to DBdata dictionary
                for result in results["results"]["bindings"]:
                    if relation in self.DBdata:
                        self.DBdata[relation].append([word[0], result["abstract"]["value"]])
                    else:
                        self.DBdata[relation] = []
                        self.DBdata[relation].append([word[0], result["abstract"]["value"]])
        
        '''Uses TfIdf class to compute tf-idf scores and CosineSimilarity on 
            the CommentBoxes that we retrieve from DBpedia'''            
        TfIdf_CosineSimilarityData = TfIdf(self.DBdata, self.term).getData()   
        return TfIdf_CosineSimilarityData


    '''function that performs a Sparql query to get the CommentBox of each Word from DBpedia'''
    def Query(word):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
                        SELECT ?abstract
                        WHERE { <http://dbpedia.org/resource/"""+word+"""> dbo:abstract ?abstract
                        FILTER (lang(?abstract) = 'en')}
                        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
       
        

    

