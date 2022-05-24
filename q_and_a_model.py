import os
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")
file_id = os.getenv("ID_CORPUS_AGID")

"""logger setup"""
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def question_answering(request_json, model=str, chat_hist=None):
    question = request_json['user_input']
    try:
        response = openai.Answer.create(
            search_model="ada",
            model=model,
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
        chat_hist += f"\nTu: {question}\nSimone: {reply}"
        return str(reply), ''.join(chat_hist)
    except RuntimeError:
        logger.error("ERROR in Dialog GPT3 pipeline", exc_info=True)
