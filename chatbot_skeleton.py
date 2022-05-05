import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

start_sequence = "\nSimone:"
restart_sequence = "\nTu: "
session_prompt = "Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza.\n\nTu: Ciao Simone \nSimone: Ciao, sono Simone, come posso aiutarti?"


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.50,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Tu:", " Simone:"]
    )
    story = response['choices'][0]['text']
    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    """a function that help the chatbot to remember"""
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
