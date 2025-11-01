import telebot
from openai import OpenAI
import os

BOT_TOKEN = "твой_токен_бота"
OPENAI_KEY = "твой_openai_api_ключ"

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋, я DashRoblAI! Готов помочь тебе 🤖")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Ты умный и дружелюбный помощник DashRoblAI."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

print("DashRoblAI Telegram Bot запущен...")
bot.polling()