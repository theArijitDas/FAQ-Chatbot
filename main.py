import sys
sys.path.append('..')

import warnings
warnings.filterwarnings('ignore')

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

model_name = 'sentence-transformers/all-MiniLM-L6-v2'

from Models.model import FaqEngine
model = FaqEngine('Data',
                   type_='UniversalSentenceEncoder',
                   model_name=model_name,
                   force_create_new=True)

def FaqBot(question, threshold=0.6):
    return model.query(question, threshold=threshold)

if __name__ == '__main__':
    question = str(input())
    print(FaqBot(question))