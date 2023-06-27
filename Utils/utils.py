import PyPDF2
import re
import pandas as pd

def convert_pdf_to_csv(path_to_pdf:str = '..\Resources/FAQs.pdf', verbose:bool=False, save:bool=True) -> None:
    # Open the PDF file
    with open(path_to_pdf, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract the text from the PDF file
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        text+='\n'

        # Define the regular expressions to extract the questions and answers
        question_regex = r'Q\.\s+(.*?)\n'
        answer_regex = r'A\.\s+(.*?)\n'

        # Find all the questions and answers using regular expressions
        questions = re.findall(question_regex, text)
        answers = re.findall(answer_regex, text)

        if verbose:
            for i, (question, answer) in enumerate(zip(questions, answers)):
                print(f'Q{i}: {question}')
                print(f'A{i}: {answer}\n')

    if save:
        # Make the DataFrame and make csv
        df = pd.DataFrame({"Question" : questions,
                        "Answer" : answers})
        df.to_csv(path_to_pdf.removesuffix('.pdf')+'.csv', index=False)