from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_cors import CORS

from chatbot_skeleton import chat

app = Flask(__name__)
load_dotenv()
CORS(app)

chat_history = []


@app.route("/chat_GPT3_davinci", methods=['POST'])
def bot():
    user_input = request.json
    response_json = {"reply": ""}
    global chat_history
#    if user_input["user_input"] == "clean history":
#        chat_history = []
    answer, chat_history = chat(user_input, chat_history)
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
