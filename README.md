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
1. Встановлення
git clone https://github.com/vladsel/text-analyzer-OpenAI-LLM.git
cd text-analyzer-OpenAI-LLM
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt

2. Налаштування
Створіть .env файл на основі .env.example
Вкажіть свої ключі:
OPENAI_KEY="your_openai_key"
TELEGRAM_BOT_TOKEN="yyour_telegram_bot_token"

3. Структура проекту
text-analyzer-OpenAI-LLM/
├── services/       # Логіка роботи з LLM
├── prompts/        # Шаблони запитів
├── libs/           # Допоміжні бібліотеки
├── scripts/        # CLI скрипти
├── api/            # REST API
├── web/            # Веб-інтерфейс
└── bot/            # Telegram бот

## Режими роботи
1. CLI скрипти
- Генерація підсумку
python scripts/get_summary.py

- Генерація змісту і тез
python scripts/get_contents.py

2. REST API
python api/endpoints.py

Доступні ендпоінти
- POST /api/v1/get_summary
- POST /api/v1/get_contents_and_theses

3. Веб-інтерфейс
python web/app.py

Відкрийте http://localhost:5001 у браузері

4. Telegram бот
python bot/bot.py



