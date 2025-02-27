import time
from contextlib import ContextDecorator

import openai
from werkzeug.exceptions import HTTPException

from libs.logger import log_info, log_warning, log_error, log_critical
from libs.tokens import write_tokens_usage_report


class ProcessingContextManager(ContextDecorator):
    @staticmethod
    def record_tokens_usage_report(
            prompt: str, model: str, prompt_tokens: int, completion_tokens: int, execution_time: float):
        write_tokens_usage_report(prompt, model, prompt_tokens, completion_tokens, execution_time)
        log_info("Логування виконано успішно")

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time

        if exc_type is not None:
            error_message = f"{exc_type.__name__}: {exc_val} (Час виконання: {execution_time:.2f} с)"

            if exc_type in {FileNotFoundError, PermissionError, FileExistsError, IOError, OSError}:
                log_error(f"Файлова помилка: {error_message}")
            elif exc_type in {ValueError, TypeError, AttributeError, NameError}:
                log_warning(f"Помилка змінних/типів: {error_message}")
            elif exc_type in {TimeoutError}:
                log_error(f"Час очікування перевищено: {error_message}")
            elif isinstance(exc_val, openai.OpenAIError):
                log_error(f"Помилка OpenAI API: {error_message}")
            elif exc_type is RuntimeError:
                log_critical(f"Критична помилка під час виконання: {error_message}")
            elif exc_type is HTTPException:
                log_error(f"Помилка виконання запитів сервера: {error_message}")
            else:
                log_critical(f"Невідома помилка: {error_message}")
            return False

        log_info(f"Програма виконана успішно за {execution_time:.2f} с")
        return True
