import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from libs.context import ProcessingContextManager
from libs.logger import log_info, log_error, log_critical
from scripts.get_contents import ContentsGenerator
from scripts.get_summary import SummaryGenerator

load_dotenv()
TEXT_DOCUMENT_KEY = os.environ["TEXT_DOCUMENT_KEY"]
GENERATED_SUMMARY_KEY = os.environ["GENERATED_SUMMARY_KEY"]
GENERATED_CONTENTS_KEY = os.environ["GENERATED_CONTENTS_KEY"]

app = Flask(__name__)


def generate_request(class_generator, text_doc: str, text_generated: str):
    try:
        log_info("Сервер Flask готовий приймати запит")

        if not request.is_json:
            log_error("Запит request не містить JSON даних")
            return jsonify({"error": "Запит не містить JSON даних"}), 400

        data = request.get_json()
        text_document_api = data.get(text_doc)
        text_generated_api = data.get(text_generated)

        if not text_document_api or not text_document_api.lower().endswith(".txt"):
            log_error(f"Необхідно передати '{text_doc}' до сервера, який повинен мати розширення '.txt'")
            return jsonify({"error": f"Необхідно передати '{text_doc}', який повинен мати розширення '.txt'"}), 400

        if text_generated_api is not None and not text_generated_api.lower().endswith(".txt"):
            log_error("Результуючий документ повинен мати розширення '.txt'")
            return jsonify({"error": "Результуючий документ повинен мати розширення '.txt'"}), 400

        log_info(f"Розпочинається виконання запиту до LLM ({class_generator.__name__}), "
                 f"де text = {text_document_api}, generated = {text_generated_api}")

        with ProcessingContextManager() as ctx:
            generator = class_generator(ctx, text_document_api, text_generated_api)
            executed_prompt = generator.start_generating()

        log_info(f"Запит через Flask виконано, відображено результати виконання "
                 f"{class_generator.__name__} і збережено у відповідному файлі")
        return jsonify({"message": executed_prompt}), 200

    except Exception as e:
        log_critical(f"Внутрішня помилка сервера: {str(e)}")
        return jsonify({"error": f"Помилка при обробці на сервері: {str(e)}"}), 500


@app.route("/api/v1/get_summary", methods=["POST"])
def generate_summary_api():
    return generate_request(SummaryGenerator, TEXT_DOCUMENT_KEY, GENERATED_SUMMARY_KEY)


@app.route("/api/v1/get_contents_and_theses", methods=["POST"])
def generate_contents_api():
    return generate_request(ContentsGenerator, TEXT_DOCUMENT_KEY, GENERATED_CONTENTS_KEY)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
