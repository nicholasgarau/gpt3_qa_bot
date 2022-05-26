import os
import openai
import logging


openai.api_key = os.getenv("OPENAI_API_KEY")


"""logger setup"""
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def question_answering(request_json, model=str, docs=list):
    question = request_json['user_input']
    try:
        response = openai.Answer.create(
            search_model="ada",
            model=model,
            question=question,
            documents=docs,
            examples_context="La PEC è la Posta Elettronica Certificata",
            examples=[["Cosa significa PEC?",
                       "Posta Elettronica Certificata"]],
            max_rerank=10,
            max_tokens=40,
            stop=["\n", "<|endoftext|>"]
        )
        #print(response)
        reply = response["answers"][0]
        return str(reply)
    except RuntimeError:
        logger.error("ERROR in Dialog GPT3 pipeline", exc_info=True)


