
import openai
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

openai.api_key = "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"
file_id = "file-DyuwXq7efH5m8dDz79RR2RWR"
doc_list

def question_answering_1():
    question = "Cos'è SPID?"
    try:
        response = openai.Answer.create(
            search_model="ada",
            model='curie',
            question=question,
            file=file_id,
            examples_context="Lo Stato italiano ha deciso di stanziare fondi per la digitalizzazione del paese",
            examples=[["A quanto ammonta il finanziamento che lo Stato italiano ha previsto per la digitalizzazione?",
                       "49,86 miliardi di euro."]],
            max_rerank=10,
            max_tokens=5,
            stop=["\n", "<|endoftext|>"]
        )
        print(response)
        reply = response[0]
        return reply
    except RuntimeError:
        logger.error("ERROR in Dialog GPT3 pipeline", exc_info=True)


def question_answering_2():
    question = "Cos'è SPID?"
    try:
        response = openai.Answer.create(
            search_model="ada",
            model='curie',
            question=question,
            docu=file_id,
            examples_context="Lo Stato italiano ha deciso di stanziare fondi per la digitalizzazione del paese",
            examples=[["A quanto ammonta il finanziamento che lo Stato italiano ha previsto per la digitalizzazione?",
                       "49,86 miliardi di euro."]],
            max_rerank=10,
            max_tokens=5,
            stop=["\n", "<|endoftext|>"]
        )
        print(response)
        reply = response[0]
        return reply
    except RuntimeError:
        logger.error("ERROR in Dialog GPT3 pipeline", exc_info=True)


print(question_answering_2())

