import json
import os
from datetime import datetime

from dotenv import load_dotenv

from libs.logger import log_info

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_FILE = os.path.join(BASE_DIR, os.getenv("REPORT_FILE"))


def write_tokens_usage_report(prompt: str, model: str, prompt_tokens: int,
                              completion_tokens: int, execution_time: float):
    if not REPORT_FILE:
        raise ValueError("Змінна середовища REPORT_FILE не встановлена")
    if prompt_tokens < 0 or completion_tokens < 0 or execution_time < 0:
        raise ValueError("Час виконання та кількість використаних токенів не можуть бути менше нуля")

    report_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "execution_time": execution_time
    }

    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    with open(REPORT_FILE, "a", encoding="utf-8") as report_file:
        report_file.write(json.dumps(report_entry, ensure_ascii=False) + "\n")

    log_info(f"Час виконання та кількість використаних токенів успішно записано у файл: {REPORT_FILE}")
