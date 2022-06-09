import os
import openai
import json
import jsonlines
import fitz
import re

openai.api_key = os.getenv("OPENAI_API_KEY")


class Loader:
    """
    a class for uploading documents to openai and get information about them
    _____
    attributes:
    filname(str) = the name of the file
    path(str), default=None = the path for the file to upload
    _____
    methods:
    upload(): a method to upload files on OpenAI.
        params: encoding(str, default=None), purpose(str, the purpose for the uploading)

    id_printer(): a method that print a log with the id of the charghed file.

    """

    def __init__(self, path, filename):
        self.path = path
        self.file = filename
        self.fullpath = self.path + self.file
        self.file_uploaded = None

    def upload(self, purpose, encoding=None):
        self.file_uploaded = openai.File.create(file=open(self.fullpath, encoding=encoding), purpose=purpose)
        return self

    def id_printer(self):
        print(self.file_uploaded['id'])
        return self


class JsonManipulator:
    """
    A class to operate on json files
    _________
    attributes:
    filname(str) = the name of the file
    path(str), default=None = the path for the file
    _________
    methods:
    to_dict() = a method to open a jsonl file. it returns a list of dictionaries

    extract_text() = a method to get keys and values of  the dictoinary create in to_dict method

    create_json_for_answers() 0 a method that creates a json ready to be uploaded on OpenAI


    """

    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.list_of_dictionary = []
        self.text_values = None

    def to_dict(self):
        with open(self.fullpath, "r", encoding='UTF-8') as json_file:
            json_list = list(json_file)
            for json_str in json_list:
                result = json.loads(json_str)
                self.list_of_dictionary.append(result)
        return self

    def extract_text(self):
        self.text_values = [f"{item['prompt']} {item['completion']}" for item in self.list_of_dictionary]
        return self

    def create_json_for_answers(self, filename):
        json_text = [{"text": item, "metadata": "FAQ su SPID"} for item in self.text_values]
        with jsonlines.open(filename, 'w') as writer:
            writer.write_all(json_text)
        return json_text

    def extract_text_for_faqs(self):
        faqs_list = [item['text'] for item in self.list_of_dictionary]
        return faqs_list


def append_text_to_json(list_of_text, file):
    json_template = [{"text": item, "metadata": "FAQ SPID base"} for item in list_of_text]
    with jsonlines.open(file, mode='w') as writer:
        writer.write_all(json_template)
    return json_template





class PdfManipulator:
    """
    A class for PDF operations
    ______
    attributes
    """

    def __init__(self, path, filename):
        self.path = path
        self.file = filename
        self.fullpath = self.path + self.file
        self.text = ""

    def extract_pdf_text(self):
        with fitz.open(self.fullpath) as doc:
            for page in doc:
                self.text += page.get_text()
        return self


if __name__ == '__main__':
    """'faq_spid_full.jsonl' creation"""
    # jsonl_imported = JsonManipulator('json_files/', 'faq_finetuning.jsonl').to_dict().extract_text().create_json_for_answers(
    #    'faq_spid_full.jsonl')

    """ snippet to extract the text from cecpac pdf"""
    # pdf_text = PdfManipulator("pdf_files/", "faq_cecpac.pdf").extract_pdf_text().text
    # txt_no_intest = pdf_text.replace('FAQ CHIUSURA CEC-PAC ', '')
    # print(txt_no_intest)
    # faqs = re.split(r'\n[1-9][.]', txt_no_intest)
    # faqs_clean = [item.replace('\n-', '').replace('\n', '') for item in faqs[1:]]
    # print(faqs_clean)

    """appending new faqs from pdf"""

    # append_text_to_json(faqs_clean, 'json_files/faq_spid_full.jsonl')

    """upload on OpenAI"""

    # file_faq_id = Loader('json_files/', 'faq_spid_full.jsonl').upload('answers', encoding='UTF-8').id_printer()

    """ open and jsoning new faqs from spid.gov """

    # with open('txt_files/SPID_faqs.txt', 'r', encoding='utf-8') as infile:
    #   faqs_basic_spid = infile.readlines()

    # faqs_spid_clean = [
    #    item.replace('&nsbp', ' ').replace('\t', '').replace('\n', '').replace('\xa0', '').replace('\ufeff', '')
    #   for item in faqs_basic_spid if len(item) > 1]
    # print(faqs_spid_clean)

    # append_text_to_json(faqs_spid_clean,'json_files/FAQ_base.jsonl')

    # file_spid_id = Loader('json_files/', 'FAQ_base.jsonl').upload('answers', encoding='UTF-8').id_printer()




