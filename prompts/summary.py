def summary_prompt(document_text: str = "Текст для формування підсумку не надійшов, проінформуй про це") -> list:
    messages = [
        {"role": "developer", "content": (
            "Ти аналітик текстів, який вміє аналізувати та створювати короткий опис основних ідей тексту.\n"
            "Ти надаєш тільки чітку відповідь чистим без форматування текстом, не використовуючи жирний шрифт тощо."
        )},
        {"role": "user", "content": (
            "Сформуй короткий підсумок для наступного текстового документу:\n" f"{document_text}"
            "\nСистемна примітка: текст може містити помилки кодування, наприклад позначені як �"
            "\nПроаналізуй вміст, враховуючи можливе пошкодження даних і надай коректну відповідь без пошкоджень."
        )}
    ]
    return messages
