from bs4 import BeautifulSoup
import requests
import jsonlines
import numpy as np


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

    def html_parser(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        self.rawtext = soup.find('div', class_="Prose text-long").get_text()
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
    urlspid = "https://www.agid.gov.it/it/piattaforme/spid"
    urlpec = "https://www.agid.gov.it/it/piattaforme/posta-elettronica-certificata"
    urlsiope = "https://www.agid.gov.it/it/piattaforme/siope"
    parser_spid = Parser(urlspid).html_parser()
    parser_pec = Parser(urlpec).html_parser()
    parser_siope = Parser(urlsiope).html_parser()

    corpus_dict = [{"text": parser_spid.strip(), "metadata": "documentazione spid"},
                   {"text": parser_pec.strip(), "metadata": "documentazione pec"},
                   {"text": parser_siope.strip(), "metadata": "documentazione siope"}
                   ]
    with jsonlines.open('json_files/corpus_agid.jsonl', 'w') as writer:
        writer.write_all(corpus_dict)