import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nSimone:"
restart_sequence = "\nTu: "

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Ciao, benvenuto nel servizio di assistenza di AGID, l'assistente è Simone e sarà in grado di fornirti assistenza."
         "\n\nTu: Ciao Simone"
         "\nSimone: Ciao, sono Simone, come posso aiutarti?"
         "\nTu: Tu lavori per lo Stato? "
         "\n\nSimone: Si, sono un assistente sviluppato da AGID per dare assistenza al cittadino"
         "\nTu: Mi servirebbero informazioni sullo SPID"
        "\nSimone:"
         "\nTu:",
  temperature=0.50,
  max_tokens=250,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Tu:", " Simone:"]

)


print(response)