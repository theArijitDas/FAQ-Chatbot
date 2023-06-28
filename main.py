import sys
sys.path.append('..')
from Models.model import FaqEngine

model = FaqEngine("Data/")

def FaqBot(question, threshold = 0.6):
    return model.query(question, threshold = threshold)

if __name__ == '__main__':
    question = str(input())
    print(FaqBot(question))