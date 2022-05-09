import openai
import os


def chat(question, chat_log=None) -> str:
    if (chat_log == None):
        chat_log = start_chat_log
    prompt = f"{chat_log}Tu: {question}\nSimone:"
    response = completion.create(prompt=prompt, engine="davinci", temperature=0.85, top_p=1, frequency_penalty=0,
                                 presence_penalty=0.7, best_of=2, max_tokens=100, stop="\nTu: ")
    return response.choices[0].text


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.Completion()

    start_chat_log = """Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza.
    \nTu: Ciao Simone \nSimone: Ciao, sono Simone, come posso aiutarti?
    """
    flag = True
    while flag:
        question = input("Digita la domanda: ")
        print("Simone: ", chat(question, start_chat_log))
        if question == 'chiudi':
            print('grazie ciao!')
            flag == False
            break