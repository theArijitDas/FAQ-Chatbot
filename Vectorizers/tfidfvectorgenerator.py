import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def get_vectorizer(data_folder_path):

    tfidf_path = f'{data_folder_path}/tfidf.pkl'

    if not os.path.exists(tfidf_path):
        csv_path = f'{data_folder_path}/FAQs.csv'
        vectorizer = TfdifVectorGenerator(csv_path)

        with open(tfidf_path, 'wb') as output_file:
             pickle.dump(vectorizer, output_file)
    
    with open(tfidf_path, 'rb') as input_file:
        return pickle.load(input_file)


def get_question_embeddings(data_folder_path):

    question_embeddings_path = f'{data_folder_path}/question_embeddingd.pkl'

    if not os.path.exists(question_embeddings_path):
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

        self.tfdif = TfidfVectorizer()
        self.tfdif.fit(questions)

    def vectorize_corpus(self, csv_path):

        data = pd.read_csv(csv_path)
        questions = data['Questions'].to_list()

        return self.tfdif.transform(questions).A.tolist()

    def query(self, sentence):

        try:
            sentence_vector = self.tfdif.transform([sentence]).toarray()
            return sentence_vector
        
        except Exception as e:
            print(e)
            return "Could not follow your question [" + sentence + "], Try again"