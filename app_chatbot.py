from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from chatbot_skeleton import chat
from q_and_a_model import question_answering, extract_original_faq, cosine_similarity_cast_fl
import pandas as pd

app = Flask(__name__)
load_dotenv()
CORS(app)

"""logger setup and model instantiation"""
logger = logging.getLogger()
chat_history = None
q_and_a_hist = []
model = "davinci:ft-unica-tesigaraun-2022-06-13-11-28-47"

df_faqs = pd.read_csv('txt_files/dataset_faqs.csv')


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
    response_json = {"GPT reply": "",
                     "id faq": "",
                     "original faq": "",
                     "cosine similarity": ""}
    try:
        global q_and_a_hist
        answer = question_answering(user_input, model)
        response_json["GPT reply"] = answer
        q_and_a_hist.append(f"Tu: {user_input['user_input']}\nSimone: {answer}")
        print(q_and_a_hist)
        semantic_search_df = extract_original_faq(df_faqs, user_input)
        response_json["id faq"] = semantic_search_df['id'].values[0]
        response_json["original faq"] = semantic_search_df['answer'].values[0]
        response_json["cosine similarity"] = str(cosine_similarity_cast_fl(answer, response_json["original faq"]))
        response_json = jsonify(response_json)
        return response_json
    except Exception as e:
        response_json = jsonify({'error': 'app Q&A dialog service error'})
        logger.info(" APP Q&A DIALOG ERROR", exc_info=e)
        return response_json


if __name__ == '__main__':
    app.run()
