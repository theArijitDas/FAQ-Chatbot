import pandas as pd
import os
import nltk
from nltk.stem.porter import PorterStemmer
import pickle
from sentence_transformers import SentenceTransformer

'''
Available Models:
- 'sentence-transformers/use-cmlm-multilingual'
- 'sentence-transformers/all-MiniLM-L6-v2'
- 'sentence-transformers/all-MiniLM-L12-v1'
- 'sentence-transformers/all-MiniLM-L12-v2'
- 'sentence-transformers/paraphrase-MiniLM-L3-v2'
- 'sentence-transformers/paraphrase-MiniLM-L6-v2'
- 'sentence-transformers/paraphrase-MiniLM-L12-v2'
- 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
- 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1'

'''

def get_vectorizer(data_folder_path, model_name, force_create_new=False):

    vectorizer_path = f'{data_folder_path}/{model_name.split("/")[-1]}.vec'

    if not os.path.exists(vectorizer_path) or force_create_new:
        vectorizer = SentenceVectorGenerator(model_name)

        with open(vectorizer_path, 'wb') as output_file:
             pickle.dump(vectorizer, output_file)
    
    with open(vectorizer_path, 'rb') as input_file:
        return pickle.load(input_file)


def get_question_embeddings(data_folder_path, model_name, force_create_new=False):

    question_embeddings_path = f'{data_folder_path}/question_embeddings_{model_name.split("/")[-1]}.embed'

    if not os.path.exists(question_embeddings_path) or force_create_new:
        csv_path = f'{data_folder_path}/FAQs.csv'
        vectorizer = get_vectorizer(data_folder_path, model_name)
        question_embeddings = vectorizer.vectorize_corpus(csv_path)

        with open(question_embeddings_path, 'wb') as output_file:
             pickle.dump(question_embeddings, output_file)
    
    with open(question_embeddings_path, 'rb') as input_file:
        return pickle.load(input_file)


class SentenceVectorGenerator:
    
    def __init__(self, model_name='sentence-transformers/use-cmlm-multilingual'):

        self.stemmer = PorterStemmer()
        self.model = SentenceTransformer(model_name)
    
    def cleanup(self, sentence):
        try:
            words = nltk.word_tokenize(sentence)
        except:
            nltk.download('punkt')
            words = nltk.word_tokenize(sentence)

        stemmed_words = [self.stemmer.stem(word) for word in words if word.isalnum()]
        return ' '.join(stemmed_words)

    def vectorize_corpus(self, csv_path):

        data = pd.read_csv(csv_path)
        questions = data['Questions'].to_list()
        corpus = [self.cleanup(sentence) for sentence in questions]

        return self.model.encode(corpus)
    
    def query(self, sentence):

        try:
            sentence_vector = self.model.encode([sentence])
            return sentence_vector
        
        except Exception as e:
            print(e)
            return "Could not follow your question [" + sentence + "], Try again"