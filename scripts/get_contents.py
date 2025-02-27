import os
import re
import time

from dotenv import load_dotenv

from libs.context import ProcessingContextManager
from libs.logger import log_debug, log_info, log_warning
from libs.storage import write_generated_text
from prompts.contents import contents_prompt
from services.llm import Llm

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DOCUMENT = os.path.join(BASE_DIR, os.getenv("TEXT_DOCUMENT"))
GENERATED_CONTENTS = os.path.join(BASE_DIR, os.getenv("GENERATED_CONTENTS"))


class ContentsGenerator:

    def __init__(self, ctx, text_document_api=None, generated_contents_api=None):
        self.ctx = ctx
        self.text_doc = text_document_api or TEXT_DOCUMENT
        self.generated_contents = generated_contents_api or GENERATED_CONTENTS
        self.gpt_llm = Llm()

        if not self.text_doc or not os.path.exists(self.text_doc):
            raise FileNotFoundError(f"Текстовий документ {self.text_doc} відсутній для генерації змісту і цитат тексту")
        if not self.generated_contents:
            raise ValueError("Змінна середовища GENERATED_CONTENTS не встановлена")

    @staticmethod
    def extract_section_count(content):
        words = content.split()
        for item in words[::-1]:
            match = re.search(r"\d+", item)
            if match:
                log_info(f"Визначена кількість пунктів у згенерованому змісті: {match.group()}")
                return
        log_warning("Не вдалося визначити кількість пунктів у згенерованому змісті")

    def read_text_document(self) -> str:
        log_info(f"Читання текстового документа: {self.text_doc}")
        with open(self.text_doc, "r", encoding="utf-8", errors="replace") as text_file:
            return text_file.read()

    def generate_contents(self, prompt, log_message, report_suffix="") -> str:
        log_info(log_message)
        start_time = time.time()
        response = self.gpt_llm.generate_call(prompt)
        execution_time = round(time.time() - start_time, 5)

        self.ctx.record_tokens_usage_report(
            prompt=os.path.basename(__file__).split('.')[0] + report_suffix,
            model=self.gpt_llm.MODEL,
            prompt_tokens=response.get("prompt_tokens", 0),
            completion_tokens=response.get("completion_tokens", 0),
            execution_time=execution_time
        )
        return response.get("content", "")

    def get_save_contents_theses(self, contents, theses) -> str:
        os.makedirs(os.path.dirname(self.generated_contents), exist_ok=True)
        log_debug(f"Каталог {os.path.dirname(self.generated_contents)} створено або вже існує")

        write_generated_text(
            os.path.splitext(self.generated_contents)[0] + "_" + os.path.basename(self.text_doc),
            "Сформований зміст текстового документа:\n" + contents
            + "\n\nДодані ключові тези або цитати до змісту:\n" + theses
        )
        return ("Сформований зміст текстового документа:\n" + contents
                + "\n\nДодані ключові тези або цитати до змісту:\n" + theses)

    def start_generating(self) -> str:
        text_document = self.read_text_document()

        contents = self.generate_contents(contents_prompt(text_document), "Генерація змісту...")
        self.extract_section_count(contents)

        theses = self.generate_contents(contents_prompt(text_document, contents),
                                        "Генерація ключових тез та цитат...", "_quotes")

        return self.get_save_contents_theses(contents, theses)


if __name__ == '__main__':
    with ProcessingContextManager() as ctx:
        contents_generator = ContentsGenerator(ctx)
        contents_generator.start_generating()
