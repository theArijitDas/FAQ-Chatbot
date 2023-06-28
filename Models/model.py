import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

import sys
sys.path.append('..')

from  Vectorizers.tfidfvectorgenerator import get_question_embeddings, get_vectorizer

class FaqEngine:

    def __init__(self, data_folder_path):

        self.stemmer = PorterStemmer()
        self.data = pd.read_csv(f'{data_folder_path}/FAQs.csv')
        self.vectorizer = get_vectorizer(data_folder_path)
        self.question_embeddings = get_question_embeddings(data_folder_path)


    def cleanup(self, sentence):
        try:
            words = nltk.word_tokenize(sentence)
        except:
            nltk.download('punkt')
            words = nltk.word_tokenize(sentence)

        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)


    def query(self, user_ques):

        try:
            # Cleanup questions and them vectorize them
            user_ques = self.cleanup(user_ques)
            user_array = self.vectorizer.query(user_ques)

            # Find cosine similarity with all questions
            cos_sims = cosine_similarity(self.question_embeddings, user_array)
            idx = cos_sims.argmax()

            # Get the answer to the most similar question
            ans = self.data.iloc[idx]['Answers']

            return ans
        
        except Exception as e:
            print(e)
            return "Could not follow your question [" + user_ques + "], Try again"
