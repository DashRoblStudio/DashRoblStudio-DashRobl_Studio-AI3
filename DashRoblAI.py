import telebot
import openai

# === НАСТРОЙКИ ===
BOT_TOKEN = "8511162242:AAH9kpND-WBOOE4Esltd8mVtPvZYweCuUgY"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# === ОБРАБОТКА КОМАНДЫ /start ===
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет 👋, я DashRoblAI! Готов помочь тебе. 🤖")

# === ОБРАБОТКА ВСЕХ СООБЩЕНИЙ ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    try:
        # GPT-5 ответ
        response = openai.ChatCompletion.create(
            model="gpt-5-turbo",
            messages=[
                {"role": "system", "content": "Ты — умный помощник DashRoblAI, отвечай дружелюбно и понятно."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, f"DashRoblAI:\n{reply}")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Сервис временно недоступен.")
        print(f"[Ошибка] {e}")

# === ЗАПУСК БОТА ===
print("🚀 DashRoblAI Telegram Bot запущен...")
bot.polling(non_stop=True)