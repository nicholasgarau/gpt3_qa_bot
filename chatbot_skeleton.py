import os
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

"""logger setup"""
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

"""Prompt definition"""
start_sequence = "\nSimone:"
restart_sequence = "\nTu: "
session_prompt = """
Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza.
Tu: Ciao Simone 
Simone: Ciao, sono Simone, come posso aiutarti?
"""


def chat(request_json, model=str, chat_log=None):
    """
    The main function which generate the response from gpt3 Q&A model
    """
    question = request_json['user_input']
    try:
        logger.info(f' GPT3 user input: {question}')
        if chat_log is None:
            chat_log = session_prompt
        prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
        response = completion.create(
            engine=model,
            prompt=prompt_text,
            temperature=0.80,
            max_tokens=250,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\nTu:"]
        )
        reply = response['choices'][0]['text']
        #if chat_log is None:
        #    chat_log = session_prompt
        chat_log += f"\nTu: {question}\nSimone: {reply}"
        return str(reply), ''.join(chat_log)

    except RuntimeError:
        logger.error("ERROR in Dialog GPT3 pipeline", exc_info=True)
