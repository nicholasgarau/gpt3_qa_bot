from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from chatbot_skeleton import chat

app = Flask(__name__)
load_dotenv()
CORS(app)

"""logger setup and model instantiation"""
logger = logging.getLogger()
chat_history = None
model = "text-davinci-002"


@app.route("/chat_GPT3_davinci", methods=['POST'])
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
