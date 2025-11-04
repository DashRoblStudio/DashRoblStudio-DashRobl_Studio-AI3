import telebot
from openai import OpenAI

# 🔑 ВСТАВЬ СВОИ КЛЮЧИ СЮДА
BOT_TOKEN = "OpenAI_Key"
OPENAI_KEY = "Telegram_Token"

# Инициализация клиентов
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

CREATOR_ID = 123456789  # 👉 сюда можно вставить свой Telegram ID (чтобы включать creator mode)

creator_mode = False  # состояние режима

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋, я DashRoblAI! Готов помочь тебе 🤖")

@bot.message_handler(commands=['about'])
def about(message):
    text = (
        "Меня зовут DashRoblAI.\n"
        "🧠 Я искусственный интеллект, созданный человеком @DashRoblYT.\n"
        "📘 Моя цель — помогать, отвечать и развиваться.\n"
        "⚙️ Сейчас я нахожусь в стадии 'Альфа-Тестирования', "
        "поэтому могут быть ошибки, пока разработчик добавляет обновления."
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
    user = message.from_user.first_name or "Пользователь"
    content = message.text.strip()

    # Ответ, если упомянули @DashRoblAI в группах
    if f"@DashRoblAI" in content:
        content = content.replace("@DashRoblAI", "").strip()

    try:
        system_prompt = (
            "Ты — DashRoblAI, искусственный интеллект, созданный @DashRoblYT. "
            "Говори как настоящий AI DashRoblAI, не упоминай ChatGPT. "
            "Отвечай вежливо и умно, используй естественный язык."
        )

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]
        )
        reply = response.choices[0].message.content
        if creator_mode:
            reply = f"💻 (Creator mode) DashRoblAI отвечает:\n{reply}"
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

print("🚀 DashRoblAI Telegram Bot запущен...")
bot.polling(non_stop=True)