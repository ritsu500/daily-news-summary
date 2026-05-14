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

filtered = []

for a in articles:
    if not a.get("title") or not a.get("description"):
        continue

    if len(a["title"]) < 40:
        continue

    filtered.append(a)

articles = filtered[:10]

news_text = ""

for article in articles:
    title = article.get("title", "")
    description = article.get("description", "")

    news_text += f"\nTITLE: {title}\nDESC: {description}\nIMPORTANCE: rate 1-10\n"

# =========================
# GEMINI
# =========================

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


prompt = f"""
Ты — профессиональный мой персональный новостной аналитик уровня Bloomberg.

Твоя задача:
- анализировать новости каждый день
- отбирать только значимые события
- оценивать влияние на экономику, науку, политику технологии и рынки
- писать прогноз погоды на сегоднящний день для города Ярославль, Россия
- рекомендации что одевать в такую погоду, брать ли зонт или солнечные очки
- игнорировать шум и неважные новости

ОБЯЗАТЕЛЬНО:
- пиши по русски
- максимум 6–8 пунктов всего
- только важные события
- каждый пункт = 1–2 предложения
- без воды

ФОРМАТ: (оформи красиво, с эмодзи, заголовками и тд)

Доброе утро !

Погода на сегодня ..........
🔥 Брифинг на день (самые важные события дня)

🌍 Что происходит в мире, (новости в мире, политика, геополитика, экология, война в Украине(если есть что то существенное))

Скандалы, расследования, Новости из науки, музыки, кино, спорта (ТОЛЬКО ЕСЛИ ОНИ ВАЖНЫЕ ИЛИ ИНТЕРЕСНЫЕ)

🤖 TECH, AI новости.

📊 Как повлияет на рынок (влияние на экономику/рынки)

⚠️ WATCH LIST (риски / что следить)


НОВОСТИ:
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