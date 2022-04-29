from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse


class Parser:
    '''A class with different method to parse a webpage''' #todo:completa docstring con l'elenco dei metodi di classe

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
        pattern_questions = '<p><strong>'
        self.questions = [str(item).replace('<p><strong>', '').replace('</strong></p>', '') for item in self.rawtext
                          if pattern_questions in str(item)]
        return self.questions

    def answers_parser(self):
        """a method that return answers"""
        pattern_questions = '<p><strong>'
        self.questions = [str(item).replace('<p>', '').replace('</p>', '') for item in self.rawtext
                          if pattern_questions not in str(item)]
        return self.questions  #todo: completa questo metodo


if __name__ == '__main__':
    url = 'https://www.agid.gov.it/it/node/1638'
    parser = Parser(url)
    print(parser.html_parser()[:10])
    #print(parser.questions_parser())
    print(parser.answers_parser())
