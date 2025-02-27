import os
import time

from dotenv import load_dotenv

from libs.context import ProcessingContextManager
from libs.logger import log_debug, log_info
from libs.storage import write_generated_text
from prompts.summary import summary_prompt
from services.llm import Llm

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DOCUMENT = os.path.join(BASE_DIR, os.getenv("TEXT_DOCUMENT"))
GENERATED_SUMMARY = os.path.join(BASE_DIR, os.getenv("GENERATED_SUMMARY"))


class SummaryGenerator:
    def __init__(self, ctx, text_document_api=None, generated_summary_api=None):
        self.ctx = ctx
        self.text_doc = text_document_api or TEXT_DOCUMENT
        self.generated_summary = generated_summary_api or GENERATED_SUMMARY
        self.gpt_llm = Llm()

        if not self.text_doc or not os.path.exists(self.text_doc):
            raise FileNotFoundError(f"Текстовий документ {self.text_doc} відсутній для генерації підсумку")
        if not self.generated_summary:
            raise ValueError("Змінна середовища GENERATED_SUMMARY не встановлена")

    def read_text_document(self) -> str:
        log_info(f"Читання текстового документа: {self.text_doc}")
        with open(self.text_doc, "r", encoding="utf-8", errors="replace") as text_file:
            return text_file.read()

    def generate_summary(self, text_document) -> str:
        log_info("Генерація підсумку...")
        summ_prompt = summary_prompt(text_document)

        start_time = time.time()
        response = self.gpt_llm.generate_call(summ_prompt)
        execution_time = round(time.time() - start_time, 5)

        self.ctx.record_tokens_usage_report(
            prompt=os.path.basename(__file__).split('.')[0],
            model=self.gpt_llm.MODEL,
            prompt_tokens=response.get("prompt_tokens", 0),
            completion_tokens=response.get("completion_tokens", 0),
            execution_time=execution_time
        )
        return response.get("content", "")

    def get_save_summary(self, summary_text) -> str:
        os.makedirs(os.path.dirname(self.generated_summary), exist_ok=True)
        log_debug(f"Каталог {os.path.dirname(self.generated_summary)} створено або вже існує")

        write_generated_text(
            os.path.splitext(self.generated_summary)[0] + "_" + os.path.basename(self.text_doc),
            "Сформований підсумок текстового документа:\n" + summary_text
        )

        return "Сформований підсумок текстового документа:\n" + summary_text

    def start_generating(self) -> str:
        text_document = self.read_text_document()
        summary = self.generate_summary(text_document)
        return self.get_save_summary(summary)


if __name__ == '__main__':
    with ProcessingContextManager() as ctx:
        summary_generator = SummaryGenerator(ctx)
        summary_generator.start_generating()
