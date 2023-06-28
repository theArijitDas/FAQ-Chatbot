import sys
sys.path.append('..')
from Models.model import FaqEngine

model = FaqEngine("Data/")

def FaqBot(question):
    return model.query(question)

if __name__ == '__main__':
    question = str(input())
    print(FaqBot(question))