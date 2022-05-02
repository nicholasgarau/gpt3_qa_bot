from bs4 import BeautifulSoup
import requests
import re


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
        '''a method that return raw text'''
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        self.rawtext = soup.find('div', class_="Prose text-long").find_all()[2:]
        return self.rawtext

    def questions_parser(self):
        """a method that return questions"""
        self.html_parser()
        pattern_questions = '<p><strong>'
        self.questions = [str(item).replace('<p><strong>', '').replace('</strong></p>', '')[4:] for item in self.rawtext
                          if pattern_questions in str(item)]
        return self.questions

    def answers_parser(self):
        """a method that return answers"""
        self.html_parser()
        pattern_answers = '<p>R'
        self.answers = [str(item).replace('<p>', '').replace('</p>', '')[4:] for item in self.rawtext
                        if pattern_answers in str(item)]
        lost_sentence = ''.join(str(self.rawtext[3:6])).replace('<p>', '').replace('</p>', '').replace('.,', '.')
        self.answers[0] = self.answers[0] + lost_sentence.replace('[', '').replace(']', '')
        return self.answers

    def __call__(self, *args, **kwargs):
        return f'Questions: \n {self.questions_parser()}\n\n Answers: \n {self.answers_parser()} '


if __name__ == '__main__':
    url = 'https://www.agid.gov.it/it/node/1638'
    parser = Parser(url)
    print(parser())
