import os
import sys

import requests
from dotenv import load_dotenv
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from libs.logger import log_info, log_warning, log_error, log_critical

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DOCUMENT_KEY = os.environ["TEXT_DOCUMENT_KEY"]
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DOCUMENTS = os.path.join(BASE_DIR, os.getenv("DOCUMENTS"))


def get_api_parameters(analysis_type: str) -> tuple:
    generated_analysis_key, analysis_api_url = None, None
    if analysis_type == "summary":
        generated_analysis_key = os.getenv("GENERATED_SUMMARY_KEY", "generated_summary")
        analysis_api_url = os.getenv("SUMMARY_API_URL", "http://127.0.0.1:5000/api/v1/get_summary")
    elif analysis_type == "contents":
        generated_analysis_key = os.getenv("GENERATED_CONTENTS_KEY", "generated_contents")
        analysis_api_url = os.getenv("CONTENTS_API_URL", "http://127.0.0.1:5000/api/v1/get_contents_and_theses")
    return generated_analysis_key, analysis_api_url


def check_parameters(file_path: str, analysis_type: str) -> str | None:
    if not file_path or not os.path.isfile(file_path):
        return "Файл не вибрано або він не існує."
    if not file_path.lower().endswith(".txt"):
        return f"Непідтримуваний формат файлу: {os.path.basename(file_path)}"
    if analysis_type not in ["summary", "contents"]:
        return "Відсутній або некоректний тип аналізу.\nВиберіть 'summary' або 'contents'"
    return None


async def start(update: Update, context: CallbackContext) -> None:
    log_info("Отримано команду /start")
    await update.message.reply_text("Вітаю!\nНадішли мені текстовий документ (.txt) для аналізу")


async def handle_text_document(update: Update, context: CallbackContext) -> None:
    document: Document = update.message.document
    if not document.file_name.lower().endswith(".txt"):
        await update.message.reply_text("Підтримуються виключно (.txt) документи для аналізу")
        return
    file_path = os.path.join(DOCUMENTS, document.file_name)

    try:
        file = await document.get_file()
        await file.download_to_drive(file_path)
        log_info(f"Файл {document.file_name} збережено у {file_path}")

        context.user_data["file_path"] = file_path
        await update.message.reply_text("Файл отримано!\nВведіть тип аналізу:\nsummary або contents")

    except Exception as e:
        log_error(f"Помилка при завантаженні файлу {document.file_name}: {str(e)}")
        await update.message.reply_text("Сталася помилка під час завантаження файлу.\nПовторіть спробу")


async def handle_analysis_type(update: Update, context: CallbackContext) -> None:
    analysis_type = update.message.text.strip().lower()
    file_path = context.user_data.get("file_path")

    if not file_path:
        await update.message.reply_text("Спочатку надішліть .txt файл.")
        return

    status = check_parameters(file_path, analysis_type)
    if status:
        log_warning(status)
        await update.message.reply_text(status)
        return

    output_key, api_url = get_api_parameters(analysis_type)
    if not output_key or not api_url:
        log_error("Некоректні параметри API, змінні середовища .env не встановлені")
        await update.message.reply_text("Внутрішня помилка сервера.\nПовторіть спробу")
        return

    await update.message.reply_text("Аналіз розпочато, зачекайте...")
    log_info(f"Надсилання запиту до API {api_url} з файлом {file_path}")

    try:
        response = requests.post(api_url, timeout=150, json={TEXT_DOCUMENT_KEY: file_path, output_key: None})

        if response.ok:
            result = response.json().get("message", "Аналіз завершено успішно")
            await update.message.reply_text(f"Результат аналізу:\n{result}")
            log_info(f"API успішно опрацював файл {file_path}")
        else:
            error = response.json().get("error", f"Виникла помилка {response.status_code}: {response.text}")
            await update.message.reply_text(f"Помилка під час аналізу: {error}\nПовторіть спробу")
            log_error(f"Виникла помилка API: {error}")

    except requests.exceptions.RequestException as e:
        error = "Неочікувана помилка запиту до API"
        log_error(error + f": {str(e)}")
        await update.message.reply_text(error + ".\nПовторіть спробу")
    except Exception as e:
        error = f"Виникла невідома помилка"
        log_critical(error + f": {str(e)}")
        await update.message.reply_text(error + ".\nПовторіть спробу")


def start_bot():
    if not TELEGRAM_BOT_TOKEN:
        log_critical("API TOKEN не знайдено. Перевірте змінну середовища .env TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    if not DOCUMENTS:
        log_critical("Перевірте змінну середовища .env DOCUMENTS")
        sys.exit(1)
    os.makedirs(DOCUMENTS, exist_ok=True)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_text_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_analysis_type))

    log_info("Телеграм бот працює...")
    app.run_polling()


if __name__ == "__main__":
    start_bot()
