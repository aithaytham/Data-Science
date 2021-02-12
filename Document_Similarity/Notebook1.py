#!/usr/bin/env python
# coding: utf-8

# # <center> Programming Project Document Similarity</center>#
# #  NAMES: AIT ETTAJER Haytham #


# In[16]:

import sys
import nltk
import numpy as np
import pandas as pd
#from requests import get
from random import shuffle
#from bs4 import BeautifulSoup
from copy import deepcopy


# # define extra parameter

# In[2]:

name_file_text = str(sys.argv[1])
threshold_simmilarity = float(sys.argv[2])

# use this variable for the tokenize the text
tokenizer = nltk.RegexpTokenizer(r'\w+')

# name File Text
#name_file_text = "tweets.txt"

# the threshold value
#threshold_simmilarity = 0.05

# the number of permutation function
number_hash_function = 10

# the number of bande 
number_of_bande = 5

# the size of shingle
size_shingle = 5


# # load data
# the list containing each line of the doc
array_data = list()

# open the file and build the list
file1 = open(name_file_text,"r")
for i in file1.readlines():
    array_data.append(i.split("\r\n")[0])
file1.close() 

# creation of a dataframe containing the text
data_frame_text_1 = pd.DataFrame(data=array_data, columns=['Text_line'])


# # Define the Jaccard similarity
def jaccard_similarity(text_1, text_2):
    """This function take two list of word and return the jaccard similarity"""
    
    text_1_inter_text_2 = 0
    
    for i in text_1:
        if i in text_2:
            text_1_inter_text_2+=1
            
    return float(text_1_inter_text_2)/float(len(text_1)+len(text_2)-text_1_inter_text_2)


# # Define the other version of Jaccard similarity
def jaccard_similarity_(kkkk, s1,s2):
    """Another version of jaccard similarity"""
    
    valeur = 0
    
    for kj in range(len(kkkk)):
        if(kkkk[kj][s1] == kkkk[kj][s2]):
            valeur+=1
    
    return valeur


# # Preprocessing data
def preprocessing_doc(array_data):
    """We use this function for build a dictionary where the keys is the ids of document and the values is the 
    texts"""
    
    # define a dictionnary that the function will return 
    dictionnary_doc_1 = dict()
    
    #tokekenize the doc
    for i in range(len(array_data)):
        array_text_tokenize = tokenizer.tokenize(array_data[i].lower())
        text = ""
        for k in array_text_tokenize:
            text+=k
        
        dictionnary_doc_1[i]=text
        
    return dictionnary_doc_1


# # Define the k shingling function
def k_shingling_caractere(dictionnary_doc, size_k):
    """This function take a dictionary where the keys are the ids of docs and the values 
    are the texts containing the essential words of the document. The second parameter is
    the length of shingling"""
    
    shingling = dict()
    
    key = 0
    for i in dictionnary_doc:
        kkkk = list()
        text = dictionnary_doc[i]
        
        if(len(text)>=size_k):
            j = 0;
            
            while(j+size_k < len(text)):
                kkk = ""
                for k in range(j, j+size_k):
                    kkk+=text[k]
                j+=1
                kkkk.append(kkk)
            
            kkk = ""
            for k in range(j, len(text)):
                kkk+=text[k]
            kkkk.append(kkk)
            
            shingling[key]=kkkk
            key+=1
        else:
            kkk = ""
            for k in range(len(text)):
                kkk+=text[k]
            kkkk.append(kkk)
            shingling[key]=kkkk
            key+=1
            
    
    # the dictionnary will contain all different k-shingle
    shingle_hash = list()
    
    # building the shingle_hash
    k = 0
    for i in shingling:
        for j in shingling[i]:
            if j not in shingle_hash:
                shingle_hash.append(j)
            
    return shingling, shingle_hash


# # Build the min hashing matrix
def build_min_hashing_matrix(dictionnary_doc, shingle_hash, permutation_functions):
    """this function is used to build the signature matrix"""
    
    signature_matrix = dict()
 
    for k in range(len(permutation_functions)):
        value_row = list()

        #--------------------------------------------
        for i in dictionnary_doc:
            for j in permutation_functions[k]:
                if(j in dictionnary_doc[i]):
                    value_row.append(j)
                    break
        #--------------------------------------------            
        
        signature_matrix[k] = value_row
        
    return signature_matrix


# # Build the similarity matrix
def build_similarity_matrix(signature_matrix):
    """This function take minhashing matrix and return the signature matrix"""
    
    similarity_matrix = dict()
    
    
    for i in range(len(signature_matrix[0])-1):
        
        array_tampon = list()
        
        for j in range(i,len(signature_matrix[0])):
            array_tampon.append(jaccard_similarity_(signature_matrix, i,j)/number_hash_function)
        
        similarity_matrix[i]=array_tampon
            
    
    return similarity_matrix


# # hash bande function
def hash_bande(bande,hashage_function):
    """We use this function to hash a band"""
    
    hash_bande = list()
    
    for i in range(len(bande[0])):
        array_test = list()
        for j in range(len(bande)):
            array_test.append(bande[j][i])
        
        for k in hashage_function:
            if k in array_test:
                hash_bande.append(k)
                break
                
    return hash_bande


# # Build the locality sensitive function
def locality_sensitive_hashing(signature_matrix,number_of_bande,shingle_hash):
    """This function constructs the function of Locality sensitive hashing"""
    
    bande_bucket = dict()
    size_bande = 0
        
    locality_sensitive_hashing_matrix = dict()
    
    # we create number_of_bande of permutation function
    hashage_function = dict()
    for i in range(number_of_bande):
        hashage_function[i] = deepcopy(shingle_hash)
        shuffle(hashage_function[i])     
    
    # it is necessary to choose a number_of_bande that divide the number of row of signature_matrix
    if(len(signature_matrix) % number_of_bande != 0):
        print(" number of bande is not a multiple of number of row signature matrix")
        return bande_bucket
    else:
        size_bande = len(signature_matrix)//number_of_bande
        

    for k in range(number_of_bande):
        
        bande_k = dict()
        
        for kj in range(size_bande):
            bande_k[kj] = signature_matrix[k*size_bande+kj]
        
        bande_bucket[k] = hash_bande(bande_k,hashage_function[k])
        
        
        
    for i in range(len(bande_bucket[0])):
        array_test = list()
        for j in range(len(bande_bucket[0])):
            kkp = 0
            for z in range(number_of_bande):
                if(bande_bucket[z][i] == bande_bucket[z][j]):
                    kkp+=1

            array_test.append(kkp/number_of_bande)
        
        locality_sensitive_hashing_matrix[i] = array_test
        
    return locality_sensitive_hashing_matrix


#dictionnary_doc = preprocessing_document(array_data)
dictionnary_doc_1 = preprocessing_doc(array_data)


# creation of k-shingling
k_shingling_carac, shingle_hash = k_shingling_caractere(dictionnary_doc_1, size_shingle)

# we create number_perm of permutation function
permutation_functions = dict()
for i in range(number_hash_function):
    permutation_functions[i] = deepcopy(shingle_hash)
    shuffle(permutation_functions[i]) 


# build the mini hashing matrix
signature_matrix = build_min_hashing_matrix(k_shingling_carac, shingle_hash, permutation_functions)


#Build the similarity matrix
testest = build_similarity_matrix(signature_matrix)


#Build the locality sensistive hashing matrix
locality_sensitive_hashing_matrix = locality_sensitive_hashing(signature_matrix,number_of_bande,shingle_hash)


#number_hash_function = 10  and  size_shingle = 5
for i in range(len(signature_matrix[0])-1):
    for j in range(i+1,len(signature_matrix[0])):
        if jaccard_similarity(k_shingling_carac[i], k_shingling_carac[j])>threshold_simmilarity:
            print(i,"    ",j,"    ",jaccard_similarity(k_shingling_carac[i], k_shingling_carac[j]))
