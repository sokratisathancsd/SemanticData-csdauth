'''
Created on Thu Mar 12 01:37:41 2020

@author: Sokratis Athanasiadis
'''
from ConceptNet import ConceptNet
from WordNet import WordNet
from DBpedia import DBpedia

def main():
    term = input("Give the term: ")
    '''Data is a dictionary to project the final Data'''
    Data = dict()
    
    '''get Data From ConceptNet'''
    ConceptNetData = ConceptNet(term).getData()
    
    '''get Data from nltk.wordnet'''
    WordNetData = WordNet(ConceptNetData,term).getData()
    
    '''get Data from DBpedia'''
    DBpediaData = DBpedia(ConceptNetData, term).getData()
    
    
    for key in ConceptNetData.keys():   
        Data[key] = []            
        for triple in range(len(ConceptNetData[key])):
            if WordNetData[key][triple][1] == None:
                '''If Distance is not found and so the field's value is None,
                    we replace it with 1000 (a huge value so the weight is close
                    to 0 (1/1000 = 0.001)'''
                WordNetData[key][triple][1] = 1000 
                
            '''In WordNet Distance +1 exists to avoid division by zero in the cases
                that we have the same word (for example word1=tea word2=tea so their 
                distance is 0), so the WordNet distance is 0'''
            Data[key].append([ConceptNetData[key][triple][0], 1/(WordNetData[key][triple][1] + 1) + DBpediaData[key][triple][1] + ConceptNetData[key][triple][1]])
    
    '''Print the output Data'''        
    for key in ConceptNetData.keys():
        print(key)
        Data[key] = Sort(Data[key])
        for triple in range(len(ConceptNetData[key])):
            print(Data[key][triple])
        print('\n')


'''sort the tuples using second element  
    of sublist Function to sort using sorted() '''
def Sort(sub_li): 
    # reverse = True (Sorts in Ascending order) 
    # key is set to sort using second element of  
    # sublist lambda has been used 
    return(sorted(sub_li, key = lambda x: x[1] ,reverse = True))         
    
    
if __name__ == '__main__':
    main()