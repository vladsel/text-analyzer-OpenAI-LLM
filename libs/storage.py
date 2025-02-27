from libs.logger import log_info


def write_generated_text(generated_file: str, generated_text: str):
    if generated_file and generated_text:
        with open(generated_file, "w", encoding="utf-8") as file:
            file.write(generated_text)
            log_info(f"Файл {generated_file} успішно записано")
    else:
        raise RuntimeError("Не вказано файл або текст для запису")
