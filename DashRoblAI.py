import telebot
import openai

# 🔑 ТВОИ КЛЮЧИ
BOT_TOKEN = "Telegram_Token"
OPENAI_KEY = "OpenAI_Key"

openai.api_key = OPENAI_KEY
bot = telebot.TeleBot(BOT_TOKEN)

CREATOR_ID = 123456789
creator_mode = False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋, я DashRoblAI! Готов помочь тебе 🤖")

@bot.message_handler(commands=['about'])
def about(message):
    text = (
        "Меня зовут DashRoblAI.\n"
        "🧠 Я искусственный интеллект, созданный человеком @DashRoblYT.\n"
        "📘 Моя цель — помогать, отвечать и развиваться.\n"
        "⚙️ Сейчас я нахожусь в стадии 'Альфа-Тестирования'."
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['creator'])
def creator_mode_toggle(message):
    global creator_mode
    if message.from_user.id == CREATOR_ID:
        creator_mode = not creator_mode
        status = "включён ✅" if creator_mode else "выключен ❌"
        bot.reply_to(message, f"🧩 Creator Mode {status}")
    else:
        bot.reply_to(message, "⛔ У тебя нет доступа к этой команде.")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong!")

@bot.message_handler(func=lambda m: True)
def main_handler(message):
    content = message.text.strip()

    if "@DashRoblAI" in content:
        content = content.replace("@DashRoblAI", "").strip()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # можно заменить на gpt-5, когда Railway обновит версию openai
            messages=[
                {"role": "system", "content": "Ты — умный ассистент DashRoblAI, созданный @DashRoblYT."},
                {"role": "user", "content": content}
            ]
        )
        reply = response["choices"][0]["message"]["content"]

        if creator_mode:
            reply = f"💻 (Creator mode)\n{reply}"

        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

print("🚀 DashRoblAI Telegram Bot запущен...")
bot.polling(non_stop=True)