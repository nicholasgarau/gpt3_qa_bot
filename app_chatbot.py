import json

from flask import Flask, request, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from chatbot_skeleton import chat

app = Flask(__name__)
load_dotenv()
CORS(app)


@app.route("/chat", methods=['POST'])
def bot():
    user_input = request.json
    response_json = {"reply": ""}
    answer = chat(user_input, chat_log=None)
    response_json["reply"] = answer
    response_json = jsonify(response_json)
    return response_json


if __name__ == '__main__':
    app.run()
