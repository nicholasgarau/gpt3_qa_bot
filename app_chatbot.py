from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from chatbot_skeleton import chat
from q_and_a_model import question_answering

app = Flask(__name__)
load_dotenv()
CORS(app)

"""logger setup and model instantiation"""
logger = logging.getLogger()
chat_history = None
q_and_a_hist = []
model = "text-davinci-002"

documents = ["""La domanda che spesso arriva alla nostra attenzione: cos’è la PEC? Si tratta di un indirizzo di posta elettronica che consente di inviare email dal valore legale. Con la posta elettronica certificata il tuo messaggio di posta elettronica è simile a una raccomandata di ricevuta di ritorno. Quindi hai degli strumenti in più per verificare la consegna avvenuta o mancata. La PEC, acronimo di posta elettronica certificata, è un servizio email che permette di confermare l’invio da parte tua e la ricezione di un messaggio nella casella di posta del destinatario. Questo consente di dare un 
                valore legale alla posta elettronica simile a quello di una raccomandata con ricevuta di ritorno.Altro vantaggio della PEC: la certezza del contenuto, grazie ai protocolli di sicurezza non è possibile modificare il messaggio o gli allegati. La certificazione del messaggio riguarda questo: il gestore PEC del mittente rilascia una prova legale del fatto che hai mandato
                il messaggio. Ecco cos’è la PEC. Inoltre conferma che il messaggio non è stato alterato. Chi riceve invia a chi ha mandato l’email la conferma. E cosa succede se invio una PEC a un contatto che ha un gestore di posta tradizionale? Solo tu avrai la ricevuta di invio messaggio. Le aziende possono eliminare la comunicazione cartacea con fornitori e clienti, inviando così anche contratti e fatture. I privati invece possono mandare documentazione alla Pubblica Amministrazione. In sintesi, cosa puoi fare con la PEC? 
                Inviare documenti a Enti Pubblici; trasmettere documenti per gare di appalto ;inviare stipendi ai dipendenti ;convocazione assemblee e giunte ;disdire polizze e contratti di fornitura ;inoltro circolari e direttive ufficiali.La PEC ha valore legale. Può essere paragonata a una raccomandata con ricevuta di ritorno e attesta l’ora esatta di ricezione. Inoltre consente l’opponibilità a terzi dell’avvenuta consegna.
                 Il valore legale della PEC è definito dal DPR n.68 dell’11 febbraio 2005. Si possono inviare messaggi tra utenti che utilizzano differenti gestori PEC? Sì, e il valore legale è inalterato in questi casi. Qauli sono i vantaggi della PEC? In primo luogo la PEC si usa come una qualsiasi posta elettronica sul tuo client o su una webmail fornita dal provider. Oltre alla semplicità c’è la sicurezza dalla tua parte, la PEC si basa su trasferimenti dati crittografati e protocolli di sicurezza come:
                POP3s ; IMAPs; SMTPs; HTTPs. Questo ti mette al riparo dai malintenzionati e, al tempo stesso, è un sistema più economico rispetto a raccomandate o fax. Ma anche più comodo da gestire per chi si trova sempre fuori ufficio, basta avere il telefonino in tasca. Cosa succede se si perdono le ricevute di queste email PEC che hanno valore legale? Ogni messaggio viene conservato dal gestore per 30 mesi e se hai bisogno di ritrovare la corrispondenza puoi ritrovare i contenuti necessari. 
                A chi serve la posta elettronica certificata?La legge 2/09 ha imposto di utilizzare la PEC ad aziende, ditte individuali che si iscrivono al registro delle imprese, professionisti iscritti all’albo per comunicare con quest’ultimo o con i colleghi, le società e le Pubbliche Amministrazioni. In sintesi, la PEC è obbligatoria per queste categorie che devono comunicare il domicilio digitale, ma serve anche ai cittadini. O almeno quelli che vogliono dare certezza di aver mandato il messaggio, e che sia stato ricevuto.
                 Poi ci sono i tributi verso la Pubblica Amministrazione: in alcuni casi la posta elettronica certificata è obbligatoria. Senza dimenticare la comodità di un servizio PEC che consente di risparmiare tempo nel fare una raccomandata con ricevuta di ritorno alla posta. Come si ottiene l’indirizzo PEC? Tutti possono usare la posta elettronica certificata, e non ci sono obblighi o limiti per crearla. Per avere un indirizzo PEC puoi usare i servizi dei provider. Devi digitare il nome del tuo dominio per la tua email o registrarne uno nuovo.
                  Pochi passaggi e puoi utilizzare la tua casella di posta certificata per le comunicazioni importanti. Ma come come attivare la PEC? Con il Servizio PEC Serverplan puoi sfruttare l’assistenza del nostro team per avere sempre supporto e sicurezza, senza dimenticare uno degli aspetti più importanti quando si parla di posta elettronica certificata: lo spazio disponibile. Con la versione base hai 1 Gb di spazio e allegati di 50 Megabyte, nella versione avanzata si arriva a 5. Inoltre per tutte le alternative è previsto controllo malware e antispam,
                   ricorda che hai sempre la possibilità inviare e ricevere email non PEC."""]

@app.route("/chat_GPT3_notuning", methods=['POST'])
def bot():
    user_input = request.json
    response_json = {"reply": ""}
    try:
        global chat_history, model
        if user_input["user_input"] == "clean history":
            chat_history = None
        answer, chat_history = chat(user_input, model, chat_history)
        print(chat_history)
        response_json["reply"] = answer
        response_json = jsonify(response_json)
        return response_json
    except Exception as e:
        response_json = jsonify({'error': 'app dialog service error'})
        logger.info(" APP DIALOG ERROR", exc_info=e)
        return response_json


@app.route("/q&a_solution", methods=["POST"])
def q_and_a():
    user_input = request.json
    response_json = {"reply": ""}
    try:
        global q_and_a_hist, documents
        answer = question_answering(user_input, model)
        response_json["reply"] = answer
        q_and_a_hist.append(f"Tu: {user_input['user_input']}\nSimone: {answer}")
        print(q_and_a_hist)
        response_json = jsonify(response_json)
        return response_json
    except Exception as e:
        response_json = jsonify({'error': 'app Q&A dialog service error'})
        logger.info(" APP Q&A DIALOG ERROR", exc_info=e)
        return response_json



if __name__ == '__main__':
    app.run()
