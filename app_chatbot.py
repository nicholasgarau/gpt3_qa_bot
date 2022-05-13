from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_cors import CORS

from chatbot_skeleton import chat, create_history

app = Flask(__name__)
load_dotenv()
CORS(app)

chat_history = []
model = 'text-davinci-002'


@app.route("/chat", methods=['POST'])
def bot():
    user_input = request.json
    response_json = {"reply": ""}
    global model, chat_history
    answer = chat(user_input, model, chat_history)
    chat_history.append(create_history(user_input, answer, chat_history)) #todo: valuta se farlo con il +=, gira ma devi correggere il prompt
    print(chat_history)
    response_json["reply"] = answer
    response_json = jsonify(response_json)
    return response_json


# @app.route("/load_model", methods=["POST"])
# def load_model():
#   user_input = request.json
#  response_json = {"reply": ""}
# answer = chat(user_input, model, chat_log=None)
# response_json["reply"] = answer
# response_json = jsonify(response_json)
# return response_json


if __name__ == '__main__':
    app.run()
