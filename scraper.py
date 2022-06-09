from bs4 import BeautifulSoup
import requests
import jsonlines
import numpy as np
import pandas as pd
import string


class Parser:
    """
    A class to parse an html page.

    Attributes
    ------------
        url=the page's url to scrape.

    Methods
    ------------
    html_parser():
        a method that saves parsed html on the 'rawtext' slot.

    questions_parser():
        a method to filter the questions of the page and saves them on the 'questions' slot.

    question_answers():
        a method to filter the answers of the page and saves them on the 'answers' slot.



    """

    def __init__(self, url=str):
        self.url = url
        self.answers = []
        self.questions = None
        self.rawtext = []

    def html_parser(self, class_to_scrape):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text.encode('latin-1'), 'html.parser')
        self.rawtext = "".join([p.text for p in soup.find_all("div", class_=class_to_scrape)])
        return self.rawtext

    def questions_parser(self):
        self.html_parser()
        pattern_questions = '<p><strong>'
        self.questions = [str(item).replace('<p><strong>', '').replace('</strong></p>', '')[4:] for item in self.rawtext
                          if pattern_questions in str(item)]
        return self.questions

    def answers_parser(self):
        self.html_parser()
        pattern_answers = '<p>R'
        self.answers = [str(item).replace('<p>', '').replace('</p>', '')[4:] for item in self.rawtext
                        if pattern_answers in str(item)]
        lost_sentence = ''.join(str(self.rawtext[3:8])).replace('<p>', '').replace('</p>', '').replace('.,', '.')
        self.answers[0] = self.answers[0] + lost_sentence.replace('[', '').replace(']', '')
        return self.answers

    def __call__(self, *args, **kwargs):
        return f'Questions: \n {self.questions_parser()}\n\n Answers: \n {self.answers_parser()} '


class DatasetGenerator:
    """A class that takes some lists and generate a dataset"""

    def __init__(self, column1, column2, *args):
        self.col1 = column1
        self.col2 = column2
        pass

    def create_jsonl(self):
        """a method that generate a jsonl file"""
        items = [{"prompt": item1, "completion": item2} for item1, item2 in np.column_stack((self.col1, self.col2))]
        with jsonlines.open('faq_finetuning.jsonl', 'w') as writer:
            writer.write_all(items)
        return None


if __name__ == '__main__':
    url = "https://www.spid.gov.it/domande-frequenti/"

    """ Questions parsing """

    questions_raw = Parser(url).html_parser("single-faq-header collapse-header")
    # print(questions_raw)
    questions_clean = [item.strip() for item in questions_raw.split('\n\n\n')]
    # print(questions_clean)
    print(len(questions_clean))

    """ importing file with ordered answers """
    with open('txt_files/answers_ordered.txt', 'r', encoding='UTF-8') as infile:
        answers_raw = infile.readlines()

    print(answers_raw)

    answers_clean = [item.replace('\n', '') for item in answers_raw if len(item) > 1]

    print(len(answers_clean))

    """ dataframe creation and csv creation """

    input_df_data = {
        'id': pd.Series(range(1, 53)),
        'question': questions_clean,
        'answer': answers_clean
    }

    df_faq = pd.DataFrame(input_df_data)
    print(df_faq)
    df_faq.to_csv('txt_files/dataset_faqs.csv', index=False)
