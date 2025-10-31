import telebot
import os
import sys
from telebot import types

# ======== Настройки ========
TOKEN = os.getenv("TELEGRAM_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID", "0"))  # твой Telegram ID
bot_name = "DashRoblAI"
creator_mode = False

if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не найден!")
    sys.exit(1)

bot = telebot.TeleBot(TOKEN)
print(f"{bot_name} запущен ✅")

# ======== Команды ========

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет 👋, я {bot_name}! Готов помочь тебе. 🤖")

@bot.message_handler(commands=['creator_mode'])
def creator_mode_toggle(message):
    global creator_mode
    if message.from_user.id == CREATOR_ID:
        creator_mode = not creator_mode
        status = "активирован 🔓" if creator_mode else "выключен 🔒"
        bot.send_message(message.chat.id, f"Режим разработчика {status}")
    else:
        bot.send_message(message.chat.id, "❌ У вас нет доступа к этой команде!")

@bot.message_handler(commands=['help'])
def help_command(message):
    commands = [
        "/start — запустить бота",
        "/creator_mode — включить или выключить режим разработчика",
        "/clear — очистить чат (в режиме разработчика)",
        "/info — узнать, кто я"
    ]
    bot.send_message(message.chat.id, "📜 Доступные команды:\n" + "\n".join(commands))

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, f"🤖 Моё имя: {bot_name}\nСоздатель: 👑 {CREATOR_ID}")

@bot.message_handler(commands=['clear'])
def clear_chat(message):
    if message.from_user.id == CREATOR_ID:
        bot.send_message(message.chat.id, "🧹 Чат очищен (виртуально, конечно)")
    else:
        bot.send_message(message.chat.id, "❌ У вас нет прав для этой команды!")

# ======== Обработка сообщений ========
@bot.message_handler(func=lambda message: True)
def chat(message):
    global creator_mode
    if creator_mode and message.from_user.id == CREATOR_ID:
        bot.send_message(message.chat.id, f"💻 (Creator mode) {bot_name} отвечает: Я получил твоё сообщение.")
    else:
        bot.send_message(message.chat.id, f"{bot_name} думает... 🤔")

bot.infinity_polling()