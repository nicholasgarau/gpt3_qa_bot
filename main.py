import scraper
"""
'''Scraping html SPID-faq page for the fine tuning and generating jsonl file'''

url = 'https://www.agid.gov.it/it/node/1638'
parser = scraper_4finetuning.Parser(url)
questions = parser.questions_parser()
answers = parser.answers_parser()
# print(questions[14]) #not a question
questions.remove(questions[14])
ds = scraper_4finetuning.DatasetGenerator(questions, answers)
ds.create_jsonl()

"""

"""
Scraping html SPID-PEC-SIOPE main page

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
"""


