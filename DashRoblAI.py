import telebot
import openai
import time

# === Настройки ===
BOT_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"
OPENAI_API_KEY = "КЛЮЧ_GPT5"

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋, я DashRoblAI! Готов помочь тебе. 🤖")

# === Команда /about ===
@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "Я — DashRoblAI, нейроассистент на GPT-5. Помогаю, отвечаю, думаю!")

# === Основной обработчик сообщений ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[{"role": "user", "content": user_text}],
        )
        reply = completion.choices[0].message["content"]
    except Exception as e:
        reply = "Сервис временно недоступен."

    bot.send_message(message.chat.id, reply)

# === Запуск polling ===
print("DashRoblAI Telegram Bot запущен...")
while True:
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"[Ошибка polling] {e}")
        time.sleep(5)