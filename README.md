# Text Analysis System
Система для аналізу текстових документів з використанням LLM (OpenAI API)

## Можливості
- Генерація коротких підсумків текстових документів
- Створення структурованого змісту з ключовими тезами
- 4 режими роботи:
1. CLI скрипти
2. REST API
3. Веб-інтерфейс
4. Telegram-бот

## Вимоги
- Python 3.10+
- Обліковий запис OpenAI
- Telegram бот (для режиму бота)

## Швидкий старт
## 1. Встановлення
```
git clone https://github.com/vladsel/text-analyzer-OpenAI-LLM.git

cd text-analyzer-OpenAI-LLM

python -m venv venv

source venv/bin/activate  # Linux/MacOS

venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## 2. Налаштування

Створити .env файл на основі .env.example

Обов'язково вказати свої ключі:

OPENAI_KEY="your_openai_key"

TELEGRAM_BOT_TOKEN="your_telegram_bot_token"


## 3. Структура проекту

text-analyzer-OpenAI-LLM/

├── 📂 api/             # REST API

├── 📂 bot/             # Telegram бот

├── 📂 web/             # Веб-інтерфейс

├── 📂 scripts/         # CLI скрипти

├── 📂 services/        # Основна логіка LLM

├── 📂 libs/            # Допоміжні модулі

├── 📂 logs/            # Логи та звітність

├── 📂 prompts/         # Шаблони запитів

├── 📂 documents/       # Вхідні файли

├── 📂 results/         # Вихідні файли

├── .env.example        # Приклад конфігурації

├── make_request.py     # Запит до API

├── .gitignore          # Ігноровані файли

├── requirements.txt    # Список залежностей

├── README.md           # Цей файл


## Режими роботи
## 1. CLI скрипти
- Генерація підсумку
```
python scripts/get_summary.py
```
- Генерація змісту і тез
```
python scripts/get_contents.py
```

Результати зберігаються в:
- results/generated_summary_[filename].txt
- results/generated_contents_[filename].txt

## 2. REST API
```
python api/endpoints.py
```

Доступні ендпоінти
```
- POST /api/v1/get_summary
- POST /api/v1/get_contents_and_theses
```

- Приклад запиту через curl
```
curl -X POST http://localhost:5000/api/v1/get_summary \
  -H "Content-Type: application/json" \
  -d '{"text_document": "documents/fruits.txt"}'
```
```
curl -X POST http://localhost:5000/api/v1/get_contents_and_theses \
  -H "Content-Type: application/json" \
  -d '{"text_document": "documents/fruits.txt"}'
```

- Вказати куди зберегти результати
 ```
curl -X POST http://localhost:5000/api/v1/get_summary \
  -H "Content-Type: application/json" \
  -d '{
    "text_document": "documents/report.txt",
    "generated_summary": "results/generated_summary_report.txt"
  }'
 ```

- Використати скрипт make_request.py
```
TEXT_DOCUMENT="documents/text_file.txt"  # Шлях до аналізованого файлу
GENERATED_SUMMARY="results/generated_summary_text_file.txt"  # Шлях для збереження підсумку
GENERATED_CONTENTS="results/generated_contents_text_file.txt" # Шлях для збереження змісту
```
```
python make_request.py # Виконати обидва запити
```
```
# Або виконати окремо
python make_request.py summary
python make_request.py contents
```


## 3. Веб-інтерфейс
```
python web/app.py
```
Відкрити http://localhost:5001 у браузері


## 4. Telegram бот
```
python bot/bot.py
```

Послідовність дій у Telegram:
- Надіслати боту команду /start
- Надіслати .txt файл
- Ввести "summary" або "contents"


## Логування (app.log)
```
[Формат запису]
2025-02-28 14:30:45,123 - module_name - LEVEL - Повідомлення

[Приклад]
2025-02-27 21:46:22,807 - app - INFO - Отримано запит на сторінку для завантаження документа
2025-02-27 21:46:22,811 - app - INFO - Валідація завершена, параметри введені вірно
2025-02-27 21:46:22,815 - app - INFO - Файл text_document.txt збережено у documents/text_document.txt
2025-02-27 21:46:22,817 - app - INFO - Тип аналізу текстового документа встановлено успішно
2025-02-27 21:46:22,821 - app - INFO - Надсилання запиту до API http://127.0.0.1:5000/api/v1/get_contents_and_theses з файлом documents/text_document.txt
2025-02-27 21:46:22,839 - endpoints - INFO - Сервер Flask готовий приймати запит
2025-02-27 21:46:22,841 - endpoints - INFO - Розпочинається виконання запиту до LLM (ContentsGenerator), де text = documents/text_document.txt, generated = None
2025-02-27 21:46:22,857 - get_contents - INFO - Читання текстового документа: documents/text_document.txt
2025-02-27 21:46:22,858 - get_contents - INFO - Генерація змісту...
2025-02-27 21:46:22,858 - llm - INFO - Виконується запит до OpenAI API...
2025-02-27 21:46:23,823 - llm - INFO - Отримано відповідь response від OpenAI API
2025-02-27 21:46:23,823 - tokens - INFO - Час виконання та кількість використаних токенів успішно записано у файл: logs/report.jsonl
2025-02-27 21:46:23,823 - context - INFO - Логування виконано успішно
2025-02-27 21:46:23,838 - get_contents - INFO - Визначена кількість пунктів у згенерованому змісті: 4
2025-02-27 21:46:23,841 - get_contents - INFO - Генерація ключових тез та цитат...
2025-02-27 21:46:23,841 - llm - INFO - Виконується запит до OpenAI API...
2025-02-27 21:46:28,157 - llm - INFO - Отримано відповідь response від OpenAI API
2025-02-27 21:46:28,157 - tokens - INFO - Час виконання та кількість використаних токенів успішно записано у файл: logs/report.jsonl
2025-02-27 21:46:28,157 - context - INFO - Логування виконано успішно
2025-02-27 21:46:28,176 - storage - INFO - Файл results/generated_contents_text_document.txt успішно записано
2025-02-27 21:46:28,176 - context - INFO - Програма виконана успішно за 5.33 с
2025-02-27 21:46:28,176 - endpoints - INFO - Запит через Flask виконано, відображено результати виконання ContentsGenerator і збережено у відповідному файлі
2025-02-27 21:46:28,176 - app - INFO - API успішно опрацював запит для аналізу documents/text_document.txt
2025-02-27 21:47:00,477 - app - INFO - Отримано запит на сторінку для завантаження документа
```


## Метрики (report.jsonl)
```
[Приклад summary]
{"timestamp": "2025-02-28T02:15:08.415600+02:00", "prompt": "get_summary", "model": "gpt-4o-mini", "prompt_tokens": 1829, "completion_tokens": 208, "execution_time": 3.44709}

[Приклад contents]
{"timestamp": "2025-02-28T02:16:19.147094+02:00", "prompt": "get_contents", "model": "gpt-4o-mini", "prompt_tokens": 1500, "completion_tokens": 59, "execution_time": 1.16529}
{"timestamp": "2025-02-28T02:16:25.136147+02:00", "prompt": "get_contents_quotes", "model": "gpt-4o-mini", "prompt_tokens": 1714, "completion_tokens": 386, "execution_time": 5.97509}
```

- prompt_tokens: Витрачено токенів на запит
- completion_tokens: Витрачено токенів на відповідь
- execution_time: Час виконання (секунди)


## Діаграма системи у форматі mermaid

```
graph TD
    subgraph "Ядро системи"
        A[LLM Service] -->|API Call| B[OpenAI API]
        C[Prompt Templates] --> A
        D[Storage] -->|Save Results| E[File System]
        F[Logger] -->|Logs| G[Log Files]
        H[Tokens] -->|Track Usage| I[REPORT_FILE]
        J[Context Manager] -->|Execution Control| A
    end
    
    subgraph "Інтерфейси"
        K[CLI Scripts] --> A
        L[REST API] --> A
        M[Web Interface] --> L
        N[Telegram Bot] --> L
    end
    
    subgraph "Додаткові сервіси"
        O[Configuration] --> P[.env]
        Q[Validation] -->|Check Input| R[Error Handling]
        S[Reporting] -->|Generate Logs| T[Log Files]
    end
    
    subgraph "Обробка запиту"
        U[User Upload .txt] -->|Send Document| M
        U -->|Send Document| N
        V[System] -->|Validate Input| W[.txt Check]
        W -->|Process| X[Analysis Type]
        X -->|summary/contents| Y[Generate Prompt]
        Y --> A
        A -->|Response| Z[Save Results]
        Z --> AA[Output to User]
    end
    
    K -->|Context Manager| R
    L --> R
    M --> R
    N --> R
    R --> F
    
    subgraph "Архітектура"
        AB[User Interface Layer] -->|Request| AC[REST API]
        AC -->|Process| AD[Processing Core]
        AD -->|Request| AE[OpenAI API]
    end
    
    subgraph "Деталізація компонентів"
        AF[LLM Class] -->|Initialize API| AG[OpenAI]
        AF -->|Validate Params| AH[Validation]
        AF -->|Process Requests| AI[Prompt Engineering]
        AF -->|Process Responses| AJ[Result Handling]
        
        AK[Flask Endpoints] -->|POST /get_summary| AL[Summary Processing]
        AK -->|POST /get_contents| AM[Contents Processing]
        AK -->|Validate JSON| AN[Validation]
        AK -->|Route Requests| AO[Request Handling]
        AK -->|Error Handling| AP[Logging]
        
        AQ[Web Interface] -->|Upload Files| AR[File Handling]
        AQ -->|Display Results| AS[Result Presentation]
        AQ -->|Integrate API| AT[API Calls]
        AQ -->|Template Rendering| AU[HTML Templates]
    end
    
    subgraph "Повна схема взаємодії"
        AV[User Interfaces] -->|Request| AW[Processing Core]
        AX[CLI Scripts] --> AW
        AY[Web Browser] --> AZ[Web Interface]
        BA[Telegram User] --> BB[Telegram Bot]
        AZ --> BC[REST API]
        BB --> BC
        BC --> BD{Route Request}
        BD -->|summary| BE[Summary Generator]
        BD -->|contents| BF[Contents Generator]
        BE/BF --> BG[LLM Service]
        BG --> BH[OpenAI API]
        BE/BF --> BI[Storage]
        BE/BF --> BJ[Logger]
        BJ --> BK[Log Files]
        BI --> BL[Result Files]
        
        BM[Report Generator] --> BN[Token Usage]
        BN --> BO[REPORT_FILE]
    end
    
    BH -->|Response| BG
    BG -->|Result| BE/BF
    BE/BF -->|Output| BC
    BC -->|Response| AZ/BB
```
