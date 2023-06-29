import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

import sys
sys.path.append('..')

from  Vectorizers.factory import get_question_embeddings, get_vectorizer

'''
Available Models:
- 'sentence-transformers/all-MiniLM-L6-v2'
- 'sentence-transformers/all-MiniLM-L12-v1'
- 'sentence-transformers/all-MiniLM-L12-v2'
- 'sentence-transformers/paraphrase-MiniLM-L3-v2'
- 'sentence-transformers/paraphrase-MiniLM-L6-v2'
- 'sentence-transformers/paraphrase-MiniLM-L12-v2'
- 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
- 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1'
'''
default_model_name = 'sentence-transformers/all-MiniLM-L6-v2'

class FaqEngine:

    def __init__(self, data_folder_path, type_='UniversalSentenceEncoder', model_name=default_model_name, force_create_new=False):

        self.stemmer = PorterStemmer()
        self.data = pd.read_csv(f'{data_folder_path}/FAQs.csv')
        self.vectorizer = get_vectorizer(data_folder_path, type_, model_name, force_create_new)
        self.question_embeddings = get_question_embeddings(data_folder_path, type_, model_name, force_create_new)


    def cleanup(self, sentence):
        try:
            words = nltk.word_tokenize(sentence)
        except:
            nltk.download('punkt')
            words = nltk.word_tokenize(sentence)

        stemmed_words = [self.stemmer.stem(word) for word in words if word.isalnum()]
        return ' '.join(stemmed_words)


    def query(self, user_query, threshold = 0.6):

        try:
            # Cleanup questions and them vectorize them
            user_ques = self.cleanup(user_query)
            user_array = self.vectorizer.query(user_ques)

            # Find cosine similarity with all questions
            cos_sims = cosine_similarity(self.question_embeddings, user_array)
            idx = cos_sims.argmax()

            # Get the answer to the most similar question, above threshold
            if cos_sims[idx] > threshold:
                ans = self.data.iloc[idx]['Answers']
            else:
                ans = "Could not follow your question [" + user_query + "], Try again"

            return ans
        
        except Exception as e:
            print(e)
            return "Could not follow your question [" + user_query + "], Try again"
