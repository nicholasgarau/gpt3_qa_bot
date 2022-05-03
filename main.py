import scraper_4finetuning

'''Scraping html SPID-faq page for the fine tuning and generating jsonl file'''

url = 'https://www.agid.gov.it/it/node/1638'
parser = scraper_4finetuning.Parser(url)
questions = parser.questions_parser()
answers = parser.answers_parser()
# print(questions[14]) #not a question
questions.remove(questions[14])
ds = scraper_4finetuning.DatasetGenerator(questions, answers)
ds.create_jsonl()