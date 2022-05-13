import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

start_sequence = "\nSimone:"
restart_sequence = "\n\nTu: "
session_prompt = "Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza.\n\nTu: Ciao Simone \nSimone: Ciao, sono Simone, come posso aiutarti?"


def chat(request_json, model=str, chat_log=None):
    """The main function which generate the response from gpt3 Q&A model"""
    question = request_json['user_input']
    if (chat_log == None):
        chat_log = session_prompt
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = completion.create(
        engine=model,
        prompt=prompt_text,
        temperature=0.60,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n"]
    )
    reply = response['choices'][0]['text']
    return str(reply)


def create_history(question, answer, chat_log=None):
    """A function to create an history for chatbot"""
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
