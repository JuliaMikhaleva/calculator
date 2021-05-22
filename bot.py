# Использую библиотеку pyTelegramBotAPI (установила с помощью pip3)
# Познакомилась с документацией на https://github.com/eternnoir/pyTelegramBotAPI
import telebot

# Types дает кнопочки
from telebot import types
# В этом файле я спрятала свой токен, который получила от BotFather
from secret import TOKEN

# Подключаюсь к созданному боту
bot = telebot.TeleBot(TOKEN, parse_mode=None)
# Здесь буду хранить выбранный пользователем филиал
my_clients = dict()


# Прописываю стартовое сообщение и возможные опции в виде кнопочек
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Нахожу куда отправлять ответное сообщение
    chat_id = message.chat.id
    # Нахожу пользователя
    user_id = message.from_user.id
    # Место для хранения кнопочек по одной в ряд
    # Нашла здесь https://github.com/eternnoir/pyTelegramBotAPI#reply-markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
    # Создаю сами кнопочки
    # Если пользователь уже успел выбрать филиал то
    if user_id in my_clients:
        department = my_clients[user_id]
        itembtns = [
            types.KeyboardButton("Ваш филиал: " + str(department)),
            types.KeyboardButton("Узнать расписание"),
            types.KeyboardButton("Узнать стоимость"),
            types.KeyboardButton("Как добраться"),
        ]
    # Иначе направить на выбор филиала
    else:
        itembtns = [
            types.KeyboardButton("Выбрать филиал")
        ]
    # Добавляю их в выделенную выше структуру
    markup.add(*itembtns)
    # Отправляю стартовое сообщение и прикрепляю структуру с кнопочками
    bot.send_message(chat_id, "Здраствуйте, чем я могу Вам помочь?", reply_markup=markup)


# Выбор филиала
@bot.message_handler(regexp="Выбрать филиал")
def send_choose_department(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    itembtns = [
        types.KeyboardButton("Филиал ЦСКА"),
        types.KeyboardButton("Филиал Электрозаводская"),
    ]
    markup.add(*itembtns)
    bot.send_message(chat_id, "Выберите интересующий вас филиал", reply_markup=markup)


# Привязываю выбранный филиал к пользователю
@bot.message_handler(regexp="Филиал ")
def send_set_department(message):
    # Снова нахожу куда отправлять ответ
    chat_id = message.chat.id
    user_id = message.from_user.id
    department = None
    if message.text == "Филиал ЦСКА":
        department = "ЦСКА"
    if message.text == "Филиал Электрозаводская":
        department = "Электрозаводская"
    if department is not None:
        my_clients[user_id] = department
        bot.send_message(chat_id, "Выбор зафиксирован")
    else:
        bot.send_message(chat_id, "Ошибка")


# Обрабатываю "Узнать расписание"
@bot.message_handler(regexp="Узнать расписание")
def send_timetable(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    department = my_clients.get(user_id)
    message = "Ошибка"
    if department == "ЦСКА":
        message = "На ЦСКА занятия проходят по средам и пятницам с 19:00 до 20:00"
    if department == "Электрозаводская":
        message = "На Электрозаводской занятия проходят по вторникам и четвергам с 18:00 до 19:00"
    # Отправляю в этот чат ответ
    bot.send_message(chat_id, message)


# Пример из документации (чтобы показать, что бот работает на недоделанных кнопочках)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Отвечаю на сообщение и отвечаю текстом самого запроса
    bot.reply_to(message, message.text)


# Запускаю бота на обработку поступающих запросов
bot.polling()
