from flask import Flask, session, request, render_template
from chatbot_skeleton import ask, append_interaction_to_chat_log
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()


@app.route("/", methods=['GET','POST'])
def bot():
    incoming_msg = request.values['Body']
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    return render_template(str(answer))

if __name__ == '__main__':
    app.run()