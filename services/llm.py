import os

import openai
from dotenv import load_dotenv

from libs.logger import log_info

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
MAX_TOKENS = os.getenv("MAX_TOKENS")
MODEL = os.getenv("MODEL")


class Llm:
    def __init__(self):
        self._OPENAI_KEY = OPENAI_KEY
        if not self._OPENAI_KEY:
            raise ValueError("API ключ не знайдено. Перевірте змінну середовища OPENAI_KEY")
        self.MAX_TOKENS = int(MAX_TOKENS)
        if not self.MAX_TOKENS:
            raise ValueError("Відсутня максимальна кількість токенів. Перевірте змінну середовища MAX_TOKENS")
        self.MODEL = MODEL
        if not self.MODEL:
            raise ValueError("Відсутній тип моделі. Перевірте змінну середовища MODEL")
        self.client = openai.Client(api_key=self._OPENAI_KEY)

    def generate_call(self, messages: list[dict[str, str]],
                      tokens: int = 1024, temperature: float = 0.7) -> dict:
        if tokens <= 0 or tokens > self.MAX_TOKENS:
            raise ValueError(f"Задана невірна кількість токенів. Допустимі значення: 1-{self.MAX_TOKENS}")
        if temperature < 0 or temperature > 1:
            raise ValueError("Задано невірне значення креативності. Допустимі значення: 0-1")
        if not messages:
            raise ValueError("Інструкції на виконання запиту відсутні")

        log_info("Виконується запит до OpenAI API...")

        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=messages,
            max_tokens=tokens,
            temperature=temperature
        )

        if response.object != "chat.completion":
            raise RuntimeError("Несподіваний формат відповіді від OpenAI API")

        if response.choices and response.choices[0].message.content and response.usage:
            log_info("Отримано відповідь response від OpenAI API")
            return {
                "content": response.choices[0].message.content.strip(),
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
        else:
            raise RuntimeError("Відповідь response від OpenAI API порожня")
