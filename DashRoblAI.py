import os
import telebot
import time
from openai import OpenAI

# ====== Настройки окружения ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
CREATOR_ID = int(os.getenv("CREATOR_ID", "7602570185"))  # твой Telegram ID

if not TELEGRAM_TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)
if not OPENAI_KEY:
    print("Ошибка: OPENAI_KEY не найден!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

creator_mode = False

# ====== Ответ GPT-5 ======
def openai_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-5",  # GPT-5 — основная модель
            messages=[{"role": "user", "content": message}],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Ошибка API OpenAI:", e)
        return "⚠️ Сервис временно недоступен или GPT-5 не отвечает."

# ====== Команды ======
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет 👋, я DashRoblAI! Готов помочь тебе. 🤖")

@bot.message_handler(commands=['help'])
def help_message(message):
    text = (
        "🤖 Команды DashRoblAI:\n\n"
        "/start — начать разговор\n"
        "/help — список команд\n"
        "/info — информация о DashRoblAI\n"
        "/ask <вопрос> — задать вопрос ИИ\n"
        "/image <описание> — создать изображение\n"
        "/say <текст> — сказать от имени ИИ (только для создателя)\n"
        "/ping — проверить статус\n"
        "/creator_mode on/off — включить или выключить Creator Mode\n"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['info'])
def info_message(message):
    info = (
        "Меня зовут DashRoblAI 🤖\n"
        "Я Искусственный интеллект, созданный человеком @DashRoblYT.\n"
        "Я могу помогать, отвечать на любые вопросы и генерировать контент.\n"
        "Сейчас я нахожусь в стадии *Альфа-тестирования*, поэтому возможны ошибки — "
        "разработчик постоянно обновляет мой интеллект. 💡"
    )
    bot.reply_to(message, info, parse_mode="Markdown")

@bot.message_handler(commands=['ping'])
def ping_command(message):
    bot.reply_to(message, "🏓 Pong! DashRoblAI работает стабильно.")

@bot.message_handler(commands=['say'])
def say_command(message):
    global creator_mode
    if message.from_user.id == CREATOR_ID:
        text = message.text.replace("/say", "").strip()
        if text:
            prefix = "💻 (Creator mode) DashRoblAI: " if creator_mode else "🤖 DashRoblAI: "
            bot.reply_to(message, prefix + text)
        else:
            bot.reply_to(message, "Использование: /say <текст>")
    else:
        bot.reply_to(message, "⛔ Команда доступна только разработчику.")

@bot.message_handler(commands=['creator_mode'])
def creator_mode_command(message):
    global creator_mode
    if message.from_user.id == CREATOR_ID:
        if "on" in message.text.lower():
            creator_mode = True
            bot.reply_to(message, "💻 Creator Mode включён.")
        elif "off" in message.text.lower():
            creator_mode = False
            bot.reply_to(message, "💻 Creator Mode выключен.")
        else:
            bot.reply_to(message, f"Текущее состояние: {'ВКЛ' if creator_mode else 'ВЫКЛ'}.\nИспользуй /creator_mode on или off.")
    else:
        bot.reply_to(message, "⛔ Эта команда только для @DashRoblYT.")

@bot.message_handler(commands=['ask'])
def ask_command(message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        bot.reply_to(message, "❓ Использование: /ask <вопрос>")
        return
    answer = openai_response(question)
    bot.reply_to(message, answer)

# ====== Реакция на упоминание в группах/каналах ======
@bot.message_handler(func=lambda m: m.text and "@DashRoblAI" in m.text)
def mention_reply(message):
    user_text = message.text.replace("@DashRoblAI", "").strip()
    if not user_text:
        return
    answer = openai_response(user_text)
    bot.reply_to(message, answer, reply_to_message_id=message.message_id)

# ====== Все остальные сообщения ======
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.chat.type == "private":  # Только в личке
        answer = openai_response(message.text)
        bot.reply_to(message, answer)
    else:
        pass  # В группах реагирует только при упоминании

# ====== Запуск ======
print("DashRoblAI Telegram Bot запущен (GPT-5)...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Бот упал, перезапуск через 5 секунд:", e)
        time.sleep(5)