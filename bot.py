# Использую библиотеку pyTelegramBotAPI (установила с помощью pip3)
# Познакомилась с документацией на https://github.com/eternnoir/pyTelegramBotAPI
import telebot

# Types дает кнопочки
from telebot import types
# В этом файле я спрятала свой токен, который получила от BotFather
from secret import TOKEN

# Подключаюсь к созданному боту
bot = telebot.TeleBot(TOKEN, parse_mode=None)


# Прописываю стартовое сообщение и возможные опции в виде кнопочек
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Нахожу куда отправлять ответное сообщение
    chat_id = message.chat.id
    # Место для хранения кнопочек по одной в ряд
    # Нашла здесь https://github.com/eternnoir/pyTelegramBotAPI#reply-markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    # Создаю сами кнопочки
    itembtn1 = types.KeyboardButton("Узнать расписание")
    itembtn2 = types.KeyboardButton("Узнать стоимость")
    itembtn3 = types.KeyboardButton("Как добраться")
    # Добавляю их в выделенную выше структуру
    markup.add(itembtn1, itembtn2, itembtn3)
    # Отправляю стартовое сообщение и прикрепляю структуру с кнопочками
    bot.send_message(chat_id, "Здраствуйте, чем я могу Вам помочь?", reply_markup=markup)


# Обрабатываю "Узнать расписание"
@bot.message_handler(regexp="Узнать расписание")
def send_timetable(message):
    # Снова нахожу куда отправлять ответ
    chat_id = message.chat.id
    # Отправляю в этот чат ответ
    bot.send_message(chat_id, """
На ЦСКА мы работаем по средам и пятницам с 19:00 до 20:00
На Электрозаводской по вторникам и четвергам с 18:00 до 19:00
""")


# Пример из документации (чтобы показать, что бот работает на недоделанных кнопочках)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Отвечаю на сообщение и отвечаю текстом самого запроса
    bot.reply_to(message, message.text)


# Запускаю бота на обработку поступающих запросов
bot.polling()