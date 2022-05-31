import os
import openai
import logging


openai.api_key = os.getenv("OPENAI_API_KEY")


"""logger setup"""
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def question_answering(request_json, model=str):
    question = request_json['user_input']
    try:
        response = openai.Answer.create(
            search_model="ada",
            model=model,
            question=question,
            file=os.getenv("FILE_SPID_BASIC"),
            examples_context="La PEC è la Posta Elettronica Certificata",
            examples=[["Cosa significa PEC?",
                       "Posta Elettronica Certificata"]],
            max_rerank=10,
            max_tokens=70,
            stop=["\n", "<|endoftext|>"]
        )
        #print(response)
        if response["answers"][0] == "":
            reply = "Gentile utente, la prego di riformulare la domanda"
        else:
            reply = response["answers"][0]
        return str(reply)
    except RuntimeError:
        logger.error("ERROR in Dialog Q&A pipeline", exc_info=True)


