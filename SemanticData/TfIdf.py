'''
@author: Sokratis Athanasiadis
'''
#sparql requests handler
from SPARQLWrapper import SPARQLWrapper, JSON
#import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
#library for cosine similarity
from scipy import spatial


class TfIdf:
    def __init__(self, data, term):
        self.term = term
        #data is a dictionary with the input data (the one retrieved from DBpedia)
        self.data = data
        #corpus contains all commentBoxes from DBpedia (=all different docs for tf-idf)
        self.corpus = []
        #store cosine similarity score
        self.weights = []
        #DBdata is a dictionary in this format 
        #[[Relation1: [word1 , CosSim1],[word2 , CosSim2]],[Relation2: [word3 , CosSim3],[word4 , CosSim4]],...
        self.TfIdfData = dict()
        
    def getData(self):
        #get commentBox of the input term from DBpedia
        word = self.term.capitalize()
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
                        SELECT ?abstract
                        WHERE { <http://dbpedia.org/resource/"""+word+"""> dbo:abstract ?abstract
                        FILTER (lang(?abstract) = 'en')}
                        
                        """)
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        termCB = result["results"]["bindings"][0]["abstract"]["value"] #get CommentBox for term      
        self.corpus.append(termCB)
        
        #get commentBox of every other from DBpedia data
        for key in self.data.keys():
            for triple in range(len(self.data[key])):
                if(self.data[key][triple][1] == None):
                    self.corpus.append("WeHaveNoDataFromDBpedia")
                else:
                    self.corpus.append(self.data[key][triple][1])
                
        #tf idf vectors
        vectorizer = TfidfVectorizer()
        #Learn vocabulary and idf, return term-document matrix.
        vectors = vectorizer.fit_transform(self.corpus) 
        #feature_names = vectorizer.get_feature_names() #Array mapping from feature integer indices to feature name.
        dense = vectors.todense()
        denselist = dense.tolist()
        
        ''' print the inverted index'''
        '''
        df = pd.DataFrame(denselist, columns=feature_names)
        print(df)
        '''
        
        '''Compute cosine similarity of the first vector (=vector that has been created
            by the input term's commentBox) and every other vector (=vector that has
            been created by every other CommentBox)'''
        for vector in denselist:
            self.weights.append(TfIdf.getCosSimilarity(denselist[0], vector))
        
        '''Create the dictionary that will be returned'''
        wpos = 1
        for relation in self.data.keys():
            for triple in range(len(self.data[relation])):
                if relation in self.TfIdfData:
                    self.TfIdfData[relation].append([self.data[relation][triple][0], self.weights[wpos]])
                else:
                    self.TfIdfData[relation] = []
                    self.TfIdfData[relation].append([self.data[relation][triple][0], self.weights[wpos]])
                wpos = wpos + 1
        return self.TfIdfData
            
    '''Function that computes the cosine similarity of vector1 and vector2'''
    def getCosSimilarity(vector1, vector2):
        result = 1 - spatial.distance.cosine(vector1, vector2)
        return result
        


    

