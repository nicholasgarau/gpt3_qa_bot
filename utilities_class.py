import os
import openai
import json

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

    def __init__(self, filename, path=None):
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


    """

    def __init__(self, path, filename):
        self.path = path
        self.file = filename
        self.fullpath = self.path + self.file
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
        return self.text_values

    def create_json_for_answers(self):
        #todo: completa questo metodo poi lancia il codice e riprova a uploadare il file su openai
