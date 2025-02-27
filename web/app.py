import os
import sys

import requests
from dotenv import load_dotenv
from flask import Flask, request, render_template

from libs.logger import log_info, log_warning, log_error, log_critical

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(BASE_DIR, os.getenv("TEMPLATES"))
DOCUMENTS = os.path.join(BASE_DIR, os.getenv("DOCUMENTS"))
TEXT_DOCUMENT_KEY = os.environ["TEXT_DOCUMENT_KEY"]

if not TEMPLATES or not os.path.isdir(TEMPLATES):
    log_critical(f"Заданий шлях {TEMPLATES} не є директорією або не існує")
    sys.exit(1)
if not DOCUMENTS:
    log_critical("Перевірте змінну середовища .env DOCUMENTS")
    sys.exit(1)
os.makedirs(DOCUMENTS, exist_ok=True)

app = Flask(__name__, template_folder=TEMPLATES)
app.config["DOCUMENTS"] = DOCUMENTS


def get_api_parameters(analysis_type: str) -> tuple:
    generated_analysis_key, generated_analysis, analysis_api_url = None, None, None

    if analysis_type == "summary":
        generated_analysis_key = os.environ["GENERATED_SUMMARY_KEY"]
        # generated_analysis = os.path.join(BASE_DIR, os.environ["GENERATED_SUMMARY"])
        analysis_api_url = os.environ["SUMMARY_API_URL"]

    elif analysis_type == "contents":
        generated_analysis_key = os.environ["GENERATED_CONTENTS_KEY"]
        # generated_analysis = os.path.join(BASE_DIR, os.environ["GENERATED_CONTENTS"])
        analysis_api_url = os.environ["CONTENTS_API_URL"]

    return generated_analysis_key, generated_analysis, analysis_api_url


def save_doc_file(doc_file) -> str | None:
    try:
        doc_file_path = os.path.join(app.config["DOCUMENTS"], doc_file.filename)
        doc_file.save(doc_file_path)
        log_info(f"Файл {doc_file.filename} збережено у {doc_file_path}")
        return doc_file_path
    except OSError as e:
        log_error(f"Помилка збереження файлу {doc_file.filename}: {str(e)}")
        return None


def check_parameters(doc_file, analysis_type) -> str | None:
    if not doc_file or doc_file.filename == "":
        return "Файл не вибрано або не завантажено"
    if not doc_file.filename.lower().endswith(".txt"):
        return f"Непідтримуваний формат файлу: {doc_file.filename}"
    if analysis_type not in ["summary", "contents"]:
        return "Відсутній або некоректний тип аналізу файлу"
    return None


@app.route("/", methods=["GET", "POST"])
def upload_document_get_generated():
    log_info("Отримано запит на сторінку для завантаження документа")

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        doc_file = request.files.get("doc_file")
        analysis_type = request.form.get("analysis_type")

        status = check_parameters(doc_file, analysis_type)
        if status:
            log_warning(status)
            return render_template("index.html", error=status)
        log_info("Валідація завершена, параметри введені вірно")

        try:
            doc_file_path = save_doc_file(doc_file)
            if not doc_file_path:
                return render_template("index.html", error=f"Помилка збереження файлу {doc_file.filename}")

            output_key, output_file, api_url = get_api_parameters(analysis_type)
            if not output_key or not api_url:
                log_error("Параметри задані невірно, змінні середовища .env не встановлені")
                return render_template("index.html", error="Внутрішні невизначені параметри сервера")
            if output_file is not None:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
            log_info("Тип аналізу текстового документа встановлено успішно")

            log_info(f"Надсилання запиту до API {api_url} з файлом {doc_file_path}")

            response = requests.post(api_url, timeout=150,
                                     json={TEXT_DOCUMENT_KEY: doc_file_path, output_key: output_file})
            if response.ok:
                result = response.json().get("message", "Аналіз виконано успішно")
                error = None
                log_info(f"API успішно опрацював запит для аналізу {doc_file_path}")
            else:
                error = response.json().get("error", f"Виникла помилка {response.status_code}: {response.text}")
                result = None
                log_error(f"Виникла помилка API: {error}")

            return render_template("index.html", result=result, error=error)

        except requests.exceptions.RequestException as e:
            error = "Неочікувана помилка запиту до API"
            log_error(error + f": {str(e)}")
        except Exception as e:
            error = f"Виникла невідома помилка"
            log_critical(error + f": {str(e)}")

        return render_template("index.html", error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
