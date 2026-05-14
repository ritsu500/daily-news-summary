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
Ты — профессиональный новостной аналитик уровня Bloomberg terminal.

Твоя задача:
- анализировать новости как рынок-аналитик
- отбирать только значимые события
- оценивать влияние на экономику, науку, политику технологии и рынки
- игнорировать шум и неважные новости

ОБЯЗАТЕЛЬНО:
- максимум 6–8 пунктов всего
- только важные события
- каждый пункт = 1–2 предложения
- без воды

ФОРМАТ:

🔥 TOP BRIEF (самые важные события дня)

🌍 WORLD, Politics (новости в мире, политика)

🤖 TECH / AI

📊 MARKET IMPACT (влияние на экономику/рынки)

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