import os
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
completion = openai.Completion()

start_sequence = "\nSimone:"
restart_sequence = "\nTu: "
session_prompt = "Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza.\n\nTu: Ciao Simone \nSimone: Ciao, sono Simone, come posso aiutarti?"


def chat(request_json, chat_log=None):
    question = request_json['user_input']
    if (chat_log == None):
        chat_log = session_prompt
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.50,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Tu:", " Simone:"]
    )
    reply = response['choices'][0]['text']
    return str(reply)




