import os
import requests
import google.generativeai as genai
from telegram import Bot

# =========================
# API KEYS
# =========================

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# =========================
# GET NEWS
# =========================

url = (
    f"https://newsapi.org/v2/top-headlines?"
    f"language=en&pageSize=15&apiKey={NEWS_API_KEY}"
)

response = requests.get(url).json()

articles = response["articles"]

news_text = ""

for article in articles:
    title = article.get("title", "")
    description = article.get("description", "")

    news_text += f"""
Title: {title}
Description: {description}

"""

# =========================
# GEMINI
# =========================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

prompt = f"""
Ты — ИИ, который делает ежедневную выжимку новостей.

Сделай:
- кратко;
- понятно;
- структурированно;
- на русском языке;
- максимум 10 пунктов.

Добавь:
1. Главные мировые события
2. Технологии / AI
3. Экономику если есть важные новости

Вот новости:

{news_text}
"""

response = model.generate_content(prompt)

summary = response.text

# =========================
# TELEGRAM
# =========================

bot = Bot(token=TELEGRAM_TOKEN)

bot.send_message(
    chat_id=CHAT_ID,
    text=summary
)

print("Done!")