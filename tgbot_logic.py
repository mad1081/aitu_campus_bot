import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

schedule = {
    "monday": ["9:00 - Математика", "11:00 - Физика", "14:00 - Программирование"],
    "tuesday": ["10:00 - Английский", "12:00 - История"],
    "wednesday": ["9:00 - Алгебра", "11:00 - Химия", "13:00 - Спорт"],
    "thursday": ["10:00 - Философия", "12:00 - Анализ данных"],
    "friday": ["9:00 - Проект", "11:00 - Лабораторная", "13:00 - Встреча команды"]
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    for d in days:
        markup.add(types.KeyboardButton(d))
    markup.add(types.KeyboardButton("Сегодня 📅"))
    bot.send_message(message.chat.id, "Привет, братанчик! 👋\nВыбери день, чтобы я показал расписание:", reply_markup=markup)

@bot.message_handler(commands=['logic'])
def registration_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(""))


@bot.message_handler(content_types=['text'])
def send_schedule(message):
    text = message.text.lower()

    if "сегодня" in text:
        import datetime
        weekday = datetime.datetime.today().strftime("%A").lower()
        if weekday in schedule:
            lessons = "\n".join(schedule[weekday])
            bot.send_message(message.chat.id, f"📅 Сегодня {message.text}:\n\n{lessons}")
        else:
            bot.send_message(message.chat.id, "Сегодня выходной 😎")
        return

    day_map = {
        "понедельник": "monday",
        "вторник": "tuesday",
        "среда": "wednesday",
        "четверг": "thursday",
        "пятница": "friday"
    }

    if text in day_map:
        day = day_map[text]
        lessons = "\n".join(schedule.get(day, ["Пар нет 😎"]))
        bot.send_message(message.chat.id, f"📘 Расписание на {message.text}:\n\n{lessons}")
    else:
        bot.send_message(message.chat.id, "Не понял, брат 😅\nВыбери день недели на клавиатуре!")

print("Бот запущен...")
bot.infinity_polling()