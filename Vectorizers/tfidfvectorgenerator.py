import pandas as pd
import os
import nltk
from nltk.stem import PorterStemmer
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


def get_vectorizer(data_folder_path, force_create_new=False):

    tfidf_path = f'{data_folder_path}/tfidf.vec'

    if not os.path.exists(tfidf_path) or force_create_new:
        csv_path = f'{data_folder_path}/FAQs.csv'
        vectorizer = TfdifVectorGenerator(csv_path)

        with open(tfidf_path, 'wb') as output_file:
             pickle.dump(vectorizer, output_file)
    
    with open(tfidf_path, 'rb') as input_file:
        return pickle.load(input_file)


def get_question_embeddings(data_folder_path, force_create_new=False):

    question_embeddings_path = f'{data_folder_path}/question_embeddings.embed'

    if not os.path.exists(question_embeddings_path) or force_create_new:
        csv_path = f'{data_folder_path}/FAQs.csv'
        vectorizer = get_vectorizer(data_folder_path)
        question_embeddings = vectorizer.vectorize_corpus(csv_path)

        with open(question_embeddings_path, 'wb') as output_file:
             pickle.dump(question_embeddings, output_file)
    
    with open(question_embeddings_path, 'rb') as input_file:
        return pickle.load(input_file)


class TfdifVectorGenerator:

    def __init__(self, csv_path):

        data = pd.read_csv(csv_path)
        questions = data['Questions'].to_list()

        self.stemmer = PorterStemmer()

        self.tfdif = TfidfVectorizer()
        self.tfdif.fit(questions)
    
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

        return self.tfdif.transform(corpus).A.tolist()

    def query(self, sentence):

        try:
            sentence_vector = self.tfdif.transform([sentence]).toarray()
            return sentence_vector
        
        except Exception as e:
            print(e)
            return "Could not follow your question [" + sentence + "], Try again"