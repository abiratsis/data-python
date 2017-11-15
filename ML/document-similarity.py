import numpy as np
import nltk
from nltk.corpus import wordnet as wn
import pandas as pd

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None
    
def convert_tag(tag):
    """Convert the tag given by nltk.pos_tag to the tag used by wordnet.synsets"""
    
    tag_dict = {'N': 'n', 'J': 'a', 'R': 'r', 'V': 'v'}
    try:
        return tag_dict[tag[0]]
    except KeyError:
        return None


def doc_to_synsets(doc):
    pos_tags = nltk.pos_tag(nltk.word_tokenize(doc))
    synsets_list = []
    for token, tag in pos_tags:
        t = convert_tag(tag)
        synsets = wn.synsets(token, t)
        if len(synsets) > 0:
            synsets_list.append(synsets[0])
            
    return synsets_list


def similarity_score(s1, s2):
    lsim = []
    for s_1 in s1:
        max_sim = 0.0
        for s_2 in s2:
            c_sim = s_1.path_similarity(s_2)
            
            if c_sim is None:
                c_sim = 0.0
                
            if c_sim > max_sim:
                max_sim = c_sim
        
        if max_sim > 0.0:
            lsim.append(max_sim)
    
    return np.mean(lsim)


def document_path_similarity(doc1, doc2):
    synsets1 = doc_to_synsets(doc1)
    synsets2 = doc_to_synsets(doc2)

    return (similarity_score(synsets1, synsets2) + similarity_score(synsets2, synsets1)) / 2
	
def test_document_path_similarity():
    doc1 = 'This is a function to test document_path_similarity.'
    doc2 = 'Use this function to see if your code in doc_to_synsets \
    and similarity_score is correct!'
    return document_path_similarity(doc1, doc2)
	
paraphrases = pd.read_csv('paraphrases.csv')

def calc_similarity(row):
    if row['Quality'] == 1:
        return document_path_similarity(row['D1'], row['D2'])
    
    return None

def most_similar_docs():
    global paraphrases
    paraphrases['sim'] = paraphrases.apply(calc_similarity, axis=1)
    max_sim_par = paraphrases.loc[paraphrases['sim'].idxmax()]
    paraphrases = paraphrases.drop('sim', 1)
    
    return (max_sim_par[1], max_sim_par[2], max_sim_par[3])
	
def label_accuracy():
    from sklearn.metrics import accuracy_score

    paraphrases['Paraphrase'] = paraphrases.apply(lambda row: 1 if document_path_similarity(row['D1'], row['D2']) > 0.75 else 0, axis=1)
    
    return accuracy_score(paraphrases['Quality'], paraphrases['Paraphrase'])