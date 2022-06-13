import os
import openai
import logging

openai.api_key = os.getenv("OPENAI_API_KEY")

"""logger setup"""
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

"""Prompt definition"""
prompt = """
Questo è il servizio di assistenza SPID: fai una domanda e l'assistente ti fornirà la risposta corretta.
Domanda: Chi può richiedere SPID? 
Risposta: Tutti i cittadini maggiorenni, in possesso di un documento italiano in corso di validità, possono attivare SPID rivolgendosi ad uno dei gestori dell’identità digitale riconosciuti da AgID.
Domanda: Qual'è il senso della vita?
Risposta: Domanda fuori contesto. Inserisca domande relative a SPID.
Domanda:
"""


def question_answering(request_json, model=str):
    question = request_json['user_input']
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=f"{prompt}{question}",
            temperature=0.30,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0.8,
            stop=["\nDomanda:", "<|endoftext|>"]
        )
        reply = response['choices'][0]['text']
        return str(reply).strip().replace('Risposta:', '')
    except RuntimeError:
        logger.error("ERROR in Dialog Q&A pipeline", exc_info=True)
