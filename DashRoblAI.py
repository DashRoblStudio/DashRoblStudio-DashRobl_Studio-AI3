import os
import telebot
import openai
import time

# ====== Переменные окружения ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
CREATOR_ID = int(os.getenv("CREATOR_ID", "7602570185")  # твой Telegram ID по умолчанию

# ====== Проверка токенов ======
if not TELEGRAM_TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не найден!")
    exit(1)
if not OPENAI_KEY:
    print("Ошибка: OPENAI_KEY не найден!")
    exit(1)

openai.api_key = OPENAI_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ====== Флаг Creator Mode ======
creator_mode = False

# ====== Функция для OpenAI ======
def openai_response(message, is_creator=False):
    try:
        prompt = f"[CREATOR MODE] {message}" if is_creator else message
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Ошибка API OpenAI:", e)
        return "Сервис временно недоступен"

# ====== Команда /creator ======
@bot.message_handler(commands=['creator'])
def handle_creator(message):
    global creator_mode
    if message.from_user.id != CREATOR_ID:
        bot.reply_to(message, "Извини, у тебя нет доступа ❌")
        return

    args = message.text.split()
    if len(args) == 1:
        bot.reply_to(message, f"Creator Mode: {'Вкл ✅' if creator_mode else 'Выкл ❌'}\nИспользуй /creator on или /creator off")
        return

    cmd = args[1].lower()
    if cmd == "on":
        creator_mode = True
        bot.reply_to(message, "Creator Mode включен ✅")
    elif cmd == "off":
        creator_mode = False
        bot.reply_to(message, "Creator Mode выключен ❌")
    elif cmd == "status":
        bot.reply_to(message, f"Creator Mode: {'Вкл ✅' if creator_mode else 'Выкл ❌'}")
    else:
        bot.reply_to(message, "Неизвестная команда. Используй on/off/status")

# ====== Обработка сообщений ======
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    is_creator = creator_mode and message.from_user.id == CREATOR_ID
    text = message.text.lower()

    # ====== Фиксированный ответ на вопрос "кто ты" ======
    if "кто ты" in text or "ты кто" in text or "кто ты такой" in text:
        answer = ("Меня зовут DashRoblAI. Я Искусственный интеллект, созданный человеком @DashRoblYT. "
                  "Я могу помогать отвечать на любые вопросы, и пока я в стадии 'Альфа Тестирование', "
                  "могут быть ошибки, потому что разработчик делает новое обновление ИИ 'DashRoblAI'.")
    else:
        # ====== Все остальные вопросы через OpenAI ======
        answer = openai_response(message.text, is_creator=is_creator)

    bot.reply_to(message, answer)

# ====== Запуск бота ======
print("DashRoblAI Telegram Bot на OpenAI запущен...")
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Бот упал, перезапуск через 5 секунд:", e)
        time.sleep(5)
