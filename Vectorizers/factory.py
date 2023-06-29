import os
import sys
sys.path.append('..')

from Vectorizers import sentenceencoder, tfidfvectorgenerator


def get_vectorizer(data_folder_path, type_, model_name, force_create_new=False):


    if type_ == 'tfidf':
        return tfidfvectorgenerator.get_vectorizer(data_folder_path, force_create_new)
    
    elif type_ == 'UniversalSentenceEncoder':
        return sentenceencoder.get_vectorizer(data_folder_path, model_name, force_create_new)
    
    else:
        print(f"Invalid type_ = {type_}. Please choose from ['tfidf', 'UniversalSentenceEncoder']")


def get_question_embeddings(data_folder_path, type_, model_name, force_create_new=False):
    
    if type_ == 'tfidf':
        return tfidfvectorgenerator.get_question_embeddings(data_folder_path, force_create_new)
    
    if type_ == 'UniversalSentenceEncoder':
        return sentenceencoder.get_question_embeddings(data_folder_path, model_name, force_create_new)
    
    else:
        print(f"Invalid type_ = {type_}. Please choose from ['tfidf', 'UniversalSentenceEncoder']")